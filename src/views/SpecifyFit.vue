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

          <div class="cell-12">
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
                          Parameters: {{ content.parameters }}
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

          <div class="cell-12">
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
                        <div class="cell-7"></div>
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
                            :type="
                              parameter_ui.parameter_type[
                                parameter_ui.model_to_parameters[[id, pname]][0]
                              ]
                            "
                            :id="
                              parameter_ui.model_to_parameters[[id, pname]][0]
                            "
                            @tieToData="
                              tie_to_data(
                                parameter_ui.model_to_parameters[[id, pname]][0]
                              )
                            "
                            view_in="model_section"
                          ></ParameterType>
                        </div>
                      </div>

                      <div
                        class="row"
                        v-for="p in parameter_ui.model_to_parameters[id]"
                        :key="p"
                      >
                        <div class="cell-3 offset-1">
                          {{ p }}
                        </div>

                        <div class="cell-8">
                          type={{ parameter_ui.parameter_type[p] }}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="card"></div>
          {{ parameter_ui }}

          <div class="card"></div>

          {{ fit }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import BasicPlot from "@/components/BasicPlot.vue";
import ParameterType from "@/components/ParameterType.vue";
import { v4 as uuidv4 } from "uuid";
import { reactive } from "vue";
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
      fit: {
        data: {},
        models: {},
        parameters: {}
      }
    };
  },
  components: {
    BasicPlot,
    ParameterType
  },
  computed: {
    parameter_ui() {
      // This function converts this.fit (which uniquely defines the fit)
      // into useful data structures that can be used in the UI.

      const parameters_type = {};
      const model_to_parameters = {};
      const data_to_parameters = {};

      // First we calculate which parameters are used in each model (a model being one assigned to a dataset)
      const models = {};
      for (const p in this.fit.parameters) {
        models[p] = [];
      }

      let parameter_id, parameter_name_in_model, model_id;

      for (const d in this.fit.data) {
        if (this.fit.data[d].parameters) {
          for (const p in this.fit.data[d].parameters) {
            parameter_id = this.fit.data[d].parameters[p];
            parameter_name_in_model = p;
            model_id = this.fit.data[d].model;
            models[parameter_id].push([model_id, parameter_name_in_model]);
          }
        }
      }

      // Count the number of times specific model is used.
      let m;
      const model_use_times = {};
      for (const d in this.fit.data) {
        m = this.fit.data[d].model;
        model_use_times[m] = model_use_times[m] ? model_use_times[m] + 1 : 1;
      }

      // Finally run through each parameter to determine its type
      let count, keys, mp;
      for (const p in this.fit.parameters) {
        // This will implicitely convert an array [parameter_id, parameter_name_in_model] to a string, but that is ok.
        count = _.countBy(models[p]);

        keys = Object.keys(count);
        for (const key of keys) {
          if (model_to_parameters[key]) {
            model_to_parameters[key].push(p);
          } else {
            model_to_parameters[key] = [p];
          }
        }

        if (keys.length === 1) {
          mp = keys[0];
          if (count[mp] === 1) {
            parameters_type[p] = "local";
          } else {
            m = mp.split(",")[0];
            if (model_use_times[m] === count[mp]) {
              parameters_type[p] = "global";
            } else {
              parameters_type[p] = "grouped";
            }
          }
        } else {
          parameters_type[p] = "shared";
        }
      }

      return {
        parameter_type: parameters_type,
        model_to_parameters: model_to_parameters,
        data_to_parameters: data_to_parameters
      };
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
    tie_to_data(p_in) {
      let p, newp;
      for (const d in this.fit.data) {
        if (this.fit.data[d].parameters) {
          for (const pname in this.fit.data[d].parameters) {
            p = this.fit.data[d].parameters[pname];
            if (p === p_in) {
              newp = parameter_uuid();
              this.fit.parameters[newp] = _.cloneDeep(
                this.fit.parameters[p_in]
              );
              this.fit.data[d].parameters[pname] = newp;
            }
          }
        }
      }
      delete this.fit.parameters[p_in];
    },
    add_model() {
      const first_add = Object.keys(this.fit["models"]).length === 0;
      const model_id = model_uuid();
      this.fit["models"][model_id] = reactive({
        // is reactive needed here?
        name: this.model_selected,
        print_name: this.model_selected // change if model is already in fit.models.
      });

      const model_parameters = {};
      let mp;
      for (const p of this.models[this.model_selected].args) {
        mp = parameter_uuid();
        this.fit["parameters"][mp] = {
          name: p.name,
          value: p.value,
          const: false
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
</style>
