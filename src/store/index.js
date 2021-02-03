import { createStore } from "vuex";

export default createStore({
  state: {
    models: {},
    fit: {
      data: {},
      models: {},
      parameters: {}
    },
    ui_specify: {
      choose_fit_open: false,
      data_selection_open: true,
      model_selection_open: true
    }
  },
  mutations: {
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
          if (models[key].length === 0) {
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
