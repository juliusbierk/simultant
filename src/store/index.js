import { createStore } from "vuex";
import misc from "@/misc.js";
import config from "@/config.js";
import _ from "lodash";

function stop_running_fit(state) {
  state.fit_running = false;
  fetch(config.py + "/interrupt_fit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    }
  });
}

export default createStore({
  state: {
    models: {},
    fit: {
      r2: null,
      data: {},
      models: {},
      parameters: {}
    },
    ui_specify: {
      choose_fit_open: false,
      data_selection_open: true,
      model_selection_open: true
    },
    fit_running: false,
    backend_running: true
  },
  mutations: {
    set_backend_not_running(state) {
      state.backend_running = false;
    },
    set_backend_running(state) {
      state.backend_running = true;
    },
    clear_fit(state) {
      state.fit = {
        data: {},
        models: {},
        parameters: {}
      };
      state.ui_specify = {
        choose_fit_open: false,
        data_selection_open: true,
        model_selection_open: true
      };
      stop_running_fit(state);
    },
    set_fit_running(state, value) {
      state.fit_running = value;
    },
    set_models(state, value) {
      state.models = value;
    },
    set_choose_fit_open(state, value) {
      state.ui_specify.choose_fit_open = value;
    },
    set_data_selection_open(state, value) {
      state.ui_specify.data_selection_open = value;
    },
    set_model_selection_open(state, value) {
      state.ui_specify.model_selection_open = value;
    },
    set_fit_data(state, payload) {
      if (payload.id in state.fit.data) {
        state.fit.data[payload.id] = {
          ...state.fit.data[payload.id],
          ...payload.value
        };
      } else {
        state.fit.data[payload.id] = payload.value;
      }
      stop_running_fit(state);
    },
    toggle_fit_in_use(state, pid) {
      state.fit.data[pid].in_use = !state.fit.data[pid].in_use;
    },
    set_fit_models(state, payload) {
      if (payload.id in state.fit.models) {
        state.fit.models[payload.id] = {
          ...state.fit.models[payload.id],
          ...payload.value
        };
      } else {
        state.fit.models[payload.id] = payload.value;
      }
      stop_running_fit(state);
    },
    set_fit_parameters(state, payload) {
      if (payload.id in state.fit.parameters) {
        state.fit.parameters[payload.id] = {
          ...state.fit.parameters[payload.id],
          ...payload.value
        };
      } else {
        state.fit.parameters[payload.id] = payload.value;
      }
      stop_running_fit(state);
    },
    set_fit_data_parameter(state, payload) {
      state.fit.data[payload.data_id].parameters[payload.parameter_name] =
        payload.parameter_id;
      stop_running_fit(state);
    },
    delete_fit_data(state, id) {
      delete state.fit.data[id];
      stop_running_fit(state);
    },
    delete_fit_detached_parameter(state, id) {
      delete state.fit.parameters[id];
      stop_running_fit(state);
    },
    delete_fit_models(state, id) {
      for (const d in state.fit.data) {
        if (state.fit.data[d].model === id) {
          state.fit.data[d].model = null;
        }
      }
      delete state.fit.models[id];
      stop_running_fit(state);
    },
    delete_fit_parameters(state, id) {
      delete state.fit.parameters[id];
      stop_running_fit(state);
    },
    fit_add_model(state, payload) {
      const model_id = misc.model_uuid();

      state.fit.models[model_id] = {
        name: payload.model_selected,
        print_name: payload.model_selected, // change if model is already in fit.models.
        show_code: false
      };

      const model_parameters = {};
      let mp;
      const kwargs = state.models[payload.model_selected].kwargs;
      const consts = state.models[payload.model_selected].consts;
      for (const p in kwargs) {
        mp = misc.parameter_uuid();

        state.fit.parameters[mp] = {
          name: p,
          value: kwargs[p],
          fit: null,
          const: consts[p],
          type: "model"
        };

        model_parameters[p] = mp;
      }

      for (const d in state.fit.data) {
        if (!state.fit.data[d].model) {
          state.fit.data[d].model = model_id;
          state.fit.data[d].parameters = _.cloneDeep(model_parameters);
        }
      }

      stop_running_fit(state);
    },
    fit_apply_model(state, payload) {
      const data_id = payload.data_id;
      const model_id = payload.model_id;
      const model_name = state.fit.models[model_id].name;
      const kwargs = state.models[model_name].kwargs;
      const consts = state.models[model_name].consts;

      let first_use = true;
      let model_parameters = {};
      let mp, pid;

      for (const d in state.fit.data) {
        if (state.fit.data[d].model === model_id) {
          for (const p in kwargs) {
            pid = state.fit.data[d].parameters[p];

            if (state.fit.parameters[pid].type === "data") {
              mp = misc.parameter_uuid();
              state.fit.parameters[mp] = {
                name: p,
                value: kwargs[p],
                fit: null,
                const: consts[p],
                type: "data"
              };

              model_parameters[p] = mp;
            } else {
              model_parameters[p] = pid;
            }
          }
          first_use = false;
          break;
        }
      }

      if (first_use) {
        for (const p in kwargs) {
          mp = misc.parameter_uuid();

          state.fit.parameters[mp] = {
            name: p,
            value: kwargs[p],
            fit: null,
            const: consts[p],
            type: "model"
          };

          model_parameters[p] = mp;
        }
      }

      state.fit.data[data_id].parameters = model_parameters;
      state.fit.data[data_id].model = model_id;
    },
    fit_tie_to_data(state, p_in) {
      let p, newp, pobj;
      for (const d in state.fit.data) {
        for (const pname in state.fit.data[d].parameters) {
          p = state.fit.data[d].parameters[pname];
          if (p === p_in) {
            newp = misc.parameter_uuid();
            pobj = _.cloneDeep(state.fit.parameters[p_in]);
            pobj.type = "data";

            state.fit.parameters[newp] = pobj;
            state.fit.data[d].parameters[pname] = newp;
          }
        }
      }
      delete state.fit.parameters[p_in];
      stop_running_fit(state);
    },
    fit_tie_to_model(state, payload) {
      const model_id = payload.model_id;
      const parameter_name = payload.parameter_name;

      const newp = misc.parameter_uuid();
      const model_name = state.fit.models[model_id].name;

      state.fit.parameters[newp] = {
        name: parameter_name,
        value: state.models[model_name].kwargs[parameter_name],
        const: state.models[model_name].consts[parameter_name],
        fit: null,
        type: "model"
      };

      let p;

      for (const d in state.fit.data) {
        if (state.fit.data[d].model === model_id) {
          p = state.fit.data[d].parameters[parameter_name];

          state.fit.data[d].parameters[parameter_name] = newp;

          if (
            p in state.fit.parameters &&
            state.fit.parameters[p].type !== "detached"
          ) {
            delete state.fit.parameters[p];
          }
        }
      }
      stop_running_fit(state);
    },
    fit_attach(state, payload) {
      const p_id = payload.p_id;
      const detached_id = payload.detached_id;

      let p;
      for (const d in state.fit.data) {
        for (const pname in state.fit.data[d].parameters) {
          p = state.fit.data[d].parameters[pname];
          if (p === p_id) {
            state.fit.data[d].parameters[pname] = detached_id;
          }
        }
      }
      state.fit.parameters[detached_id].value =
        state.fit.parameters[p_id].value;
      delete state.fit.parameters[p_id];
      stop_running_fit(state);
    },
    fit_detach_to_data(state, payload) {
      const data_id = payload.data_id;
      const parameter_name = payload.parameter_name;
      const newp = misc.parameter_uuid();

      state.fit.parameters[newp] = {
        name: parameter_name,
        value:
          state.fit.parameters[
            state.fit.data[data_id].parameters[parameter_name]
          ].value,
        fit: null,
        const:
          state.fit.parameters[
            state.fit.data[data_id].parameters[parameter_name]
          ].const,
        type: "data"
      };

      state.fit.data[data_id].parameters[parameter_name] = newp;
      stop_running_fit(state);
    },
    fit_set_initial_value(state, payload) {
      state.fit.parameters[payload.pid].value = payload.value;
    },
    fit_set_fit_value(state, payload) {
      state.fit.parameters[payload.pid].fit = payload.value;
    },
    fit_set_r2_value(state, payload) {
      state.fit.r2 = payload;
    },
    fit_toggle_parameter_value_type(state, pid) {
      state.fit.parameters[pid].const = !state.fit.parameters[pid].const;
    }
  },
  getters: {
    detached_parameters: state => {
      const detached = {};
      for (const p in state.fit.parameters) {
        if (state.fit.parameters[p].type === "detached") {
          detached[p] = state.fit.parameters[p].name;
        }
      }
      return detached;
    },
    model_parameters: state => {
      // First we calculate which parameters are used in each model (a model being one assigned to a dataset)
      const models = {};

      let parameter_id, parameter_name_in_model, model_id, key, parameter_type;

      for (const d in state.fit.data) {
        if (state.fit.data[d].parameters) {
          for (const p in state.fit.data[d].parameters) {
            parameter_id = state.fit.data[d].parameters[p];
            parameter_name_in_model = p;
            model_id = state.fit.data[d].model;

            key = [model_id, parameter_name_in_model];
            if (key in models) {
              if (!models[key].contains(parameter_id)) {
                models[key].push(parameter_id);
              }
            } else {
              models[key] = [parameter_id];
            }
          }
        }
      }

      // Then for each parameter we assign its type based on how it is used in each model
      const parameters = {};
      for (const m in state.fit.models) {
        parameters[m] = {};
        for (const pname in state.models[state.fit.models[m].name].kwargs) {
          key = [m, pname];

          if (models[key] === undefined) {
            parameters[m][pname] = { type: "unused", pid: null };
          } else if (models[key].length === 0) {
            console.log("assertion error!");
          } else if (models[key].length === 1) {
            parameter_id = models[key][0];
            parameter_type = state.fit.parameters[parameter_id].type;
            parameters[m][pname] = {
              type:
                parameter_type === "detached"
                  ? "model-detached"
                  : parameter_type,
              pid: parameter_id
            };
          } else {
            // Now the parameter must be data and/or detached combination.

            // Check if it is data or detached some are detached:
            let all_data = true;
            for (const parameter_id of models[key]) {
              if (state.fit.parameters[parameter_id].type !== "data") {
                all_data = false;
                break;
              }
            }

            if (all_data) {
              parameters[m][pname] = {
                type: "data",
                pid: null
              };
            } else {
              parameters[m][pname] = {
                type: "detached",
                pid: null
              };
            }
          }
        }
      }

      return parameters;
    }
  },
  actions: {},
  modules: {}
});
