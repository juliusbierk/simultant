<template>
  <div style="padding:10px" class="grid">
    <div class="row" v-if="!Object.keys(db_data).length">
      <div class="cell-6 offset-3">
        <div class="remark alert">
          No data has been imported.
        </div>
      </div>
    </div>

    <div class="row" v-if="Object.keys(db_data).length">
      <div :class="{ 'cell-12': choose_fit_open, 'cell-2': !choose_fit_open }">
        <div class="window" v-bind:class="{ minimized: !choose_fit_open }">
          <div class="window-caption">
            <span class="title">Fits</span>

            <div class="buttons">
              <span
                v-show="choose_fit_open"
                @click="choose_fit_open = false"
                class="btn-min btn-corner-hover defaultcursor"
              ></span>
              <span
                v-show="!choose_fit_open"
                @click="choose_fit_open = true"
                class="btn-max btn-corner-hover defaultcursor"
              ></span>
            </div>
          </div>

          <div class="window-content p-2"></div>
        </div>
      </div>

      <div class="cell-3" v-show="!choose_fit_open && !data_selection_open">
        <div class="window" v-bind:class="{ minimized: !data_selection_open }">
          <div class="window-caption">
            <span class="title">Data Selection</span>

            <div class="buttons">
              <span
                v-show="data_selection_open"
                @click="data_selection_open = false"
                class="btn-min btn-corner-hover defaultcursor"
              ></span>
              <span
                v-show="!data_selection_open"
                @click="data_selection_open = true"
                class="btn-max btn-corner-hover defaultcursor"
              ></span>
            </div>
          </div>
        </div>
      </div>

      <div
        :class="{
          'cell-3': true,
          'offset-4': data_selection_open,
          'offset-1': !data_selection_open
        }"
        v-show="!choose_fit_open && !model_selection_open"
      >
        <div class="window" v-bind:class="{ minimized: !model_selection_open }">
          <div class="window-caption">
            <span class="title">Model Selection</span>

            <div class="buttons">
              <span
                v-show="model_selection_open"
                @click="model_selection_open = false"
                class="btn-min btn-corner-hover defaultcursor"
              ></span>
              <span
                v-show="!model_selection_open"
                @click="model_selection_open = true"
                class="btn-max btn-corner-hover defaultcursor"
              ></span>
            </div>
          </div>
        </div>
      </div>

      <div
        v-show="!choose_fit_open"
        :class="{
          'cell-1': true,
          'offset-9': model_selection_open && data_selection_open,
          'offset-6': model_selection_open && !data_selection_open,
          'offset-2':
            (!model_selection_open && data_selection_open) ||
            (!model_selection_open && !data_selection_open)
        }"
      >
        <button
          style="font-size:30px; margin-right:2px"
          class="button defaultcursor"
        >
          &#9100;
        </button>
        <button style="font-size:30px" class="button defaultcursor">
          <span class="flip">&#9100;</span>
        </button>
      </div>
    </div>

    <div class="row" v-if="Object.keys(db_data).length">
      <div class="cell-6">
        <div class="row">
          <div class="cell-12" v-show="choose_fit_open || data_selection_open">
            <div
              class="window"
              v-bind:class="{ minimized: !data_selection_open }"
            >
              <div class="window-caption">
                <span class="title">Data Selection</span>

                <div class="buttons">
                  <span
                    v-show="data_selection_open"
                    @click="data_selection_open = false"
                    class="btn-min btn-corner-hover defaultcursor"
                  ></span>
                  <span
                    v-show="!data_selection_open"
                    @click="data_selection_open = true"
                    class="btn-max btn-corner-hover defaultcursor"
                  ></span>
                </div>
              </div>

              <div style="min-height: 300px;" class="window-content p-2">
                <div class="row">
                  <div
                    class="cell-6 offset-1"
                    :key="data_selection_render_index"
                  >
                    <label for="group_select"><small>Data Group</small></label>
                    <select
                      id="group_select"
                      data-role="select"
                      @change="update_selection_datasets"
                    >
                      <option
                        style="display:none"
                        disabled
                        selected
                        value
                      ></option>
                      <option
                        v-for="(content, parent) in db_data"
                        :value="parent"
                        v-bind:key="parent"
                      >
                        {{ parent }}</option
                      >
                    </select>
                  </div>
                </div>

                <div class="row">
                  <div
                    class="cell-9 offset-1"
                    v-if="selected_data_group"
                    :key="selected_data_group"
                  >
                    <label for="dataset_select"><small>Datasets</small></label>
                    <select
                      id="dataset_select"
                      data-role="select"
                      v-model="selected_dataset_ids"
                      multiple
                    >
                      <option
                        v-for="content in db_data[selected_data_group]"
                        v-bind:key="content.id"
                        :value="content.id"
                        >{{ content.name }}</option
                      >
                      >
                    </select>
                  </div>
                </div>
                <div class="row">
                  <div class="cell-3 offset-8" v-show="selected_data_group">
                    <div class="row">
                      <button
                        style="position: relative; top:22px"
                        class="button primary defaultcursor"
                        @click="add_datasets"
                      >
                        Add to Fit
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="cell-12" v-show="Object.keys(fit.data).length > 0">
            <div class="window">
              <div class="window-caption">
                <!--            <span class="icon mif-windows"></span>-->
                <span class="title">Data</span>
              </div>

              <div class="window-content p-2">
                <div v-for="(content, id) in fit.data" :key="id">
                  <div class="card">
                    <div class="card-header">
                      <div class="row">
                        <div class="cell-6">
                          <a
                            style="font-size:20px"
                            class="btn-close defaultcursor"
                            >&#10005;</a
                          >
                          {{ content.parent }} : {{ content.name }}
                        </div>
                        <div class="cell-6" v-if="fit.models[content.model]">
                          Applied Model:
                          {{ fit.models[content.model].print_name }}
                        </div>
                      </div>
                    </div>

                    <div class="card-content">
                      <div class="row">
                        <div class="cell-11 offset-1">
                          <div
                            style="margin-bottom:3px; margin-top:3px"
                            v-for="(pid, pname) in content.parameters"
                            :key="pid"
                          >
                            <ParameterType
                              :name="pname"
                              :id="pid"
                              :type="fit.parameters[pid].type"
                              @tieToModel="tie_to_model(content.model, pname)"
                              view_in="data_section"
                              @attach="attach(pid, $event)"
                              @detach="detach_to_data(id, pname)"
                              :detached_parameters="detached_parameters"
                            ></ParameterType>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="cell-6">
        <div class="row">
          <div class="cell-12" v-show="choose_fit_open || model_selection_open">
            <div
              class="window"
              v-bind:class="{ minimized: !model_selection_open }"
            >
              <div class="window-caption">
                <span class="title">Model Selection</span>

                <div class="buttons">
                  <span
                    v-show="model_selection_open"
                    @click="model_selection_open = false"
                    class="btn-min btn-corner-hover defaultcursor"
                  ></span>
                  <span
                    v-show="!model_selection_open"
                    @click="model_selection_open = true"
                    class="btn-max btn-corner-hover defaultcursor"
                  ></span>
                </div>
              </div>

              <div style="min-height: 300px;" class="window-content p-2">
                <div class="row">
                  <div
                    class="cell-6 offset-1"
                    :key="model_selection_render_index"
                  >
                    <label for="model_select"><small>Model</small></label>
                    <select
                      id="model_select"
                      data-role="select"
                      v-model="model_selected"
                    >
                      <option
                        style="display:none"
                        disabled
                        selected
                        value
                      ></option>
                      <option
                        v-for="(content, name) in models"
                        :value="name"
                        :key="name"
                      >
                        {{ name }}</option
                      >
                    </select>
                  </div>
                </div>

                <div class="row" v-show="model_selected">
                  <div
                    class="cell-5 offset-1"
                    v-show="Object.keys(fit.data).length > 0"
                  >
                    <input
                      id="apply_to_all_checkbox"
                      v-model="apply_to_all"
                      type="checkbox"
                      data-role="checkbox"
                      checked
                    />
                    <label
                      style="position: relative; bottom:5px"
                      for="apply_to_all_checkbox"
                      ><small>Apply to all datasets</small></label
                    >
                  </div>

                  <div class="cell-3 offset-1">
                    <button
                      class="button primary defaultcursor"
                      @click="add_model"
                    >
                      Add to Fit
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="cell-12" v-show="Object.keys(fit.models).length > 0">
            <div class="window">
              <div class="window-caption">
                <!--            <span class="icon mif-windows"></span>-->
                <span class="title">Models</span>
              </div>

              <div class="window-content p-2">
                <div v-for="(content, id) in fit.models" :key="id">
                  <div class="card">
                    <div class="card-header">
                      <div class="row">
                        <div class="cell-5">
                          <a
                            style="font-size:20px"
                            class="btn-close defaultcursor"
                            >&#10005;</a
                          >
                          {{ content.print_name }}
                        </div>

                        <div class="offset-4">
                          <input
                            @click="content.show_code = !content.show_code"
                            type="checkbox"
                            data-role="switch"
                            data-caption="Code"
                          />
                        </div>
                      </div>
                    </div>

                    <div class="card-content">
                      <div
                        v-for="pname in Object.keys(
                          models[content.name].kwargs
                        )"
                        :key="pname"
                      >
                        <div
                          class="offset-1"
                          style="margin-bottom:3px; margin-top:3px"
                        >
                          <ParameterType
                            :name="pname"
                            :type="model_parameters[id][pname].type"
                            @tieToData="
                              tie_to_data(model_parameters[id][pname].pid)
                            "
                            @tieToModel="tie_to_model(id, pname)"
                            @attach="
                              attach(model_parameters[id][pname].pid, $event)
                            "
                            @detach="tie_to_model(id, pname)"
                            :id="model_parameters[id][pname].pid"
                            view_in="model_section"
                            :detached_parameters="detached_parameters"
                          ></ParameterType>
                        </div>
                      </div>
                    </div>

                    <div v-if="content.show_code" class="card-footer p-2">
                      <ShowCode :code="models[content.name].code"></ShowCode>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div
            class="cell-12"
            v-show="
              Object.keys(fit.models).length > 1 ||
                (Object.keys(fit.models).length > 0 &&
                  Object.keys(fit.data).length > 1)
            "
          >
            <div class="window">
              <div class="window-caption">
                <!--            <span class="icon mif-windows"></span>-->
                <span class="title">Detached Parameters</span>
              </div>

              <div class="window-content p-2">
                <div class="row">
                  <div class="cell-8 offset-1">
                    <input
                      type="text"
                      data-role="input"
                      data-prepend="Parameter name: "
                      v-model="add_parameter_name"
                    />
                  </div>
                  <div class="cell-3">
                    <button
                      class="button defaultcursor"
                      @click="add_detached_parameter"
                    >
                      Add
                    </button>
                  </div>
                </div>

                <div
                  class="row"
                  v-for="(name, id) in detached_parameters"
                  :key="id"
                >
                  <div class="cell-8 offset-1">
                    <button
                      data-role="hint"
                      data-hint-text="This is a detached parameter, which can be shared between models and/or datasets."
                      data-hint-hide="0"
                      data-cls-hint="bg-lightCyan fg-white"
                      class="button info defaultcursor rounded outline "
                    >
                      {{ name }}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="card"></div>
          Numbers of parameters: {{ Object.keys(fit.parameters).length }}
          <br />
          Number of detached parameters:
          {{ Object.keys(detached_parameters).length }}

          <br />
          <br />

          {{ model_parameters }}

          <br />
          <br />
          <br />

          {{ fit }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import BasicPlot from "@/components/BasicPlot.vue";
import ParameterType from "@/components/ParameterType.vue";
import ShowCode from "@/components/ShowCode.vue";
import store from '@/store'
import { v4 as uuidv4 } from "uuid";
import _ from "lodash";

function parameter_uuid() {
  return "par_" + uuidv4();
}

function model_uuid() {
  return "model_" + uuidv4();
}

function data_uuid() {
  return "data_" + uuidv4();
}

export default {
  name: "Data",
  store,
  data: function() {
    return {
      py: "http://127.0.0.1:7555",
      choose_fit_open: false,
      data_selection_open: true,
      model_selection_open: true,
      db_data: {},
      models: {},
      selected_data_group: null,
      selected_dataset_ids: null,
      selected_dataset_names: null,
      model_selected: null,
      data_selection_render_index: 0,
      model_selection_render_index: 0,
      apply_to_all: true,
      add_parameter_name: "",
    };
  },
  components: {
    BasicPlot,
    ParameterType,
    ShowCode
  },
  computed: {
    detached_parameters() {
      const detached = {};
      for (const p in this.fit.parameters) {
        if (this.fit.parameters[p].type === "detached") {
          detached[p] = this.fit.parameters[p].name;
        }
      }
      return detached;
    },
    model_parameters() {
      // First we calculate which parameters are used in each model (a model being one assigned to a dataset)
      const models = {};

      let parameter_id, parameter_name_in_model, model_id, key, parameter_type;

      for (const d in this.fit.data) {
        if (this.fit.data[d].parameters) {
          for (const p in this.fit.data[d].parameters) {
            parameter_id = this.fit.data[d].parameters[p];
            parameter_name_in_model = p;
            model_id = this.fit.data[d].model;

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
      for (const m in this.fit.models) {
        parameters[m] = {};
        for (const pname in this.models[this.fit.models[m].name].kwargs) {
          key = [m, pname];
          if (models[key].length === 0) {
            console.log("assertion error!");
          } else if (models[key].length === 1) {
            parameter_id = models[key][0];
            parameter_type = this.fit.parameters[parameter_id].type;
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
              if (this.fit.parameters[parameter_id].type !== "data") {
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
  methods: {
    update_datasets() {
      fetch(this.py + "/data_list", {}).then(async result => {
        this.db_data = await result.json();
        this.data_selection_render_index += 1;
      });
    },
    update_model_list() {
      fetch(this.py + "/model_list", {}).then(async result => {
        this.models = await result.json();
        this.model_selection_render_index += 1;
      });
    },
    update_selection_datasets(e) {
      if (e.target.value) {
        this.selected_dataset_ids = [];
        this.selected_dataset_names = [];
        for (const x of this.db_data[e.target.value]) {
          this.selected_dataset_ids.push(x.id);
          this.selected_dataset_names.push(x.name);
        }
        this.selected_data_group = e.target.value;
      }
    },
    add_datasets() {
      const first_add = Object.keys(this.fit["data"]).length === 0;
      for (let i = 0; i < this.selected_dataset_ids.length; i++) {
        this.fit["data"][data_uuid()] = {
          id: this.selected_dataset_ids[i],
          name: this.selected_dataset_names[i],
          parent: this.selected_data_group,
          in_use: true,
          weight: "uniform",
          model: null,
          parameters: null
        };
      }

      // Clean up selection:
      this.selected_data_group = null;
      this.data_selection_render_index += 1; // This is a key that makes the element re-render
      if (first_add) {
        this.data_selection_open = false;
      }
    },
    add_model() {
      const first_add = Object.keys(this.fit["models"]).length === 0;
      const model_id = model_uuid();
      this.fit["models"][model_id] = {
        name: this.model_selected,
        print_name: this.model_selected, // change if model is already in fit.models.
        show_code: false
      };

      const model_parameters = {};
      let mp;
      for (const p of this.models[this.model_selected].args) {
        mp = parameter_uuid();
        this.fit["parameters"][mp] = {
          name: p.name,
          value: p.value,
          const: false,
          type: "model"
        };

        model_parameters[p.name] = mp;
      }

      if (this.apply_to_all) {
        for (const d in this.fit.data) {
          this.apply_model_to_dataset(model_id, d, model_parameters);
        }
      }

      // Clean up selection:
      this.model_selected = null;
      this.model_selection_render_index += 1; // This is a key that makes the element re-render
      if (first_add) {
        this.model_selection_open = false;
      }
    },
    apply_model_to_dataset(model_id, dataset_id, parameters) {
      this.fit.data[dataset_id].model = model_id;
      this.fit.data[dataset_id].parameters = _.cloneDeep(parameters);
    },
    add_detached_parameter() {
      if (this.add_parameter_name !== "") {
        const p = parameter_uuid();

        this.fit.parameters[p] = {
          name: this.add_parameter_name,
          value: 1,
          const: false,
          type: "detached"
        };
        this.add_parameter_name = "";
      }
    },
    tie_to_data(p_in) {
      let p, newp;
      for (const d in this.fit.data) {
        for (const pname in this.fit.data[d].parameters) {
          p = this.fit.data[d].parameters[pname];
          if (p === p_in) {
            newp = parameter_uuid();
            this.fit.parameters[newp] = _.cloneDeep(this.fit.parameters[p_in]);
            this.fit.parameters[newp].const = true;
            this.fit.parameters[newp].type = "data";
            this.fit.data[d].parameters[pname] = newp;
          }
        }
      }
      delete this.fit.parameters[p_in];
    },
    tie_to_model(model_id, parameter_name) {
      const newp = parameter_uuid();
      const model_name = this.fit.models[model_id].name;
      this.fit.parameters[newp] = {
        name: parameter_name,
        value: this.models[model_name].kwargs[parameter_name],
        const: false,
        type: "model"
      };

      let p;

      for (const d in this.fit.data) {
        if (this.fit.data[d].model === model_id) {
          p = this.fit.data[d].parameters[parameter_name];
          this.fit.data[d].parameters[parameter_name] = newp;

          if (
            p in this.fit.parameters &&
            this.fit.parameters[p].type !== "detached"
          ) {
            delete this.fit.parameters[p];
          }
        }
      }
    },
    attach(p_id, detached_id) {
      let p;
      for (const d in this.fit.data) {
        for (const pname in this.fit.data[d].parameters) {
          p = this.fit.data[d].parameters[pname];
          if (p === p_id) {
            this.fit.data[d].parameters[pname] = detached_id;
          }
        }
      }
      this.fit.parameters[detached_id].value = this.fit.parameters[p_id].value;
      delete this.fit.parameters[p_id];
    },
    detach_to_data(data_id, parameter_name) {
      const newp = parameter_uuid();
      this.fit.parameters[newp] = {
        name: parameter_name,
        value: this.fit.parameters[
          this.fit.data[data_id].parameters[parameter_name]
        ].value,
        const: true,
        type: "data"
      };
      this.fit.data[data_id].parameters[parameter_name] = newp;
    }
  },
  mounted: function() {
    this.update_datasets();
    this.update_model_list();
  }
};
</script>

<style>
.btn-corner-hover:hover {
  background-color: #7f8ca1;
}

li.disabled {
  display: none !important;
}

.flip {
  display: inline-block;
  -moz-transform: scale(-1, 1);
  -webkit-transform: scale(-1, 1);
  -o-transform: scale(-1, 1);
  -ms-transform: scale(-1, 1);
  transform: scale(-1, 1);
}
</style>
