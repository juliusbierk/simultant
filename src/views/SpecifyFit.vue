<template>
  <div style="padding:10px" class="grid">
    <div class="row" v-if="loaded && !Object.keys(db_data).length">
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
            <span class="title">Fit</span>

            <div class="buttons">
              <span
                v-show="choose_fit_open"
                @click="set_choose_fit_open(false)"
                class="btn-min btn-corner-hover defaultcursor"
              ></span>
              <span
                v-show="!choose_fit_open"
                @click="set_choose_fit_open(true)"
                class="btn-max btn-corner-hover defaultcursor"
              ></span>
            </div>
          </div>

          <div class="window-content p-2">
            <button class="button alert" @click="clear_fit">Clear Fit</button>
          </div>
        </div>
      </div>

      <div class="cell-3" v-show="!choose_fit_open && !data_selection_open">
        <div class="window" v-bind:class="{ minimized: !data_selection_open }">
          <div class="window-caption">
            <span class="title">Data Selection</span>

            <div class="buttons">
              <span
                v-show="data_selection_open"
                @click="set_data_selection_open(false)"
                class="btn-min btn-corner-hover defaultcursor"
              ></span>
              <span
                v-show="!data_selection_open"
                @click="set_data_selection_open(true)"
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
                @click="set_model_selection_open(false)"
                class="btn-min btn-corner-hover defaultcursor"
              ></span>
              <span
                v-show="!model_selection_open"
                @click="set_model_selection_open(true)"
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
                    @click="set_data_selection_open(false)"
                    class="btn-min btn-corner-hover defaultcursor"
                  ></span>
                  <span
                    v-show="!data_selection_open"
                    @click="set_data_selection_open(true)"
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
                            @click="delete_data(id, content)"
                            style="font-size:20px"
                            class="btn-close defaultcursor"
                            >&#10005;</a
                          >
                          {{ content.parent }} : {{ content.name }}
                        </div>
                        <div
                          class="cell-6"
                          v-show="Object.keys(fit.models).length > 0"
                        >
                          <select
                            class="jselect"
                            :value="content.model"
                            @input="change_model(id, $event.target.value)"
                          >
                            <option
                              v-for="(m, id) in fit.models"
                              :key="id"
                              :value="id"
                              >{{ m.print_name }}</option
                            >
                          </select>
                        </div>
                      </div>
                    </div>

                    <div class="card-content">
                      <div class="row">
                        <div class="cell-7 offset-1">
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
                    @click="set_model_selection_open(false)"
                    class="btn-min btn-corner-hover defaultcursor"
                  ></span>
                  <span
                    v-show="!model_selection_open"
                    @click="set_model_selection_open(true)"
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
                  ></div>

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
                            @click="delete_model(id, content)"
                            style="font-size:20px"
                            class="btn-close defaultcursor"
                            >&#10005;</a
                          >
                          {{ content.print_name }}
                        </div>

                        <div class="offset-4">
                          <input
                            v-model="content.show_code"
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
                      <ShowCode
                        :code="
                          (models[content.name].expr_mode
                            ? ''
                            : '# Output dimension = ' +
                              models[content.name].ode_dim_select.toString() +
                              '\n') + models[content.name].code
                        "
                      ></ShowCode>
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
                  <div
                    v-if="parameter_n_used[id] > 0"
                    class="cell-1 offset-1"
                  ></div>
                  <div v-else class="cell-1 offset-1">
                    <a
                      @click="delete_detached_parameter(id, name)"
                      style="font-size:20px"
                      class="btn-close defaultcursor"
                      >&#10005;</a
                    >
                  </div>

                  <div class="cell-2">
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

                  <div v-if="parameter_n_used[id] > 0" class="cell-6">
                    <span style="text-align: right;" class="tally"
                      >Used in {{ parameter_n_used[id] }} data sets</span
                    >
                  </div>
                  <div v-else class="cell-6">
                    <span style="text-align: right;" class="tally"
                      >Not in use</span
                    >
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters, mapMutations } from "vuex";
import BasicPlot from "@/components/BasicPlot.vue";
import ParameterType from "@/components/ParameterType.vue";
import ShowCode from "@/components/ShowCode.vue";
import store from "@/store";
import misc from "@/misc.js";
import config from "@/config.js";

export default {
  name: "SpecifyFit",
  store,
  data: function() {
    return {
      loaded: false,
      py: config.py,
      db_data: {},
      selected_data_group: null,
      selected_dataset_ids: null,
      selected_dataset_names: null,
      model_selected: null,
      data_selection_render_index: 0,
      model_selection_render_index: 0,
      add_parameter_name: ""
    };
  },
  components: {
    BasicPlot,
    ParameterType,
    ShowCode
  },
  computed: {
    ...mapState({
      fit: "fit",
      models: "models",
      choose_fit_open: state => state.ui_specify.choose_fit_open,
      data_selection_open: state => state.ui_specify.data_selection_open,
      model_selection_open: state => state.ui_specify.model_selection_open
    }),
    ...mapGetters(["detached_parameters", "model_parameters"]),
    parameter_n_used() {
      const n_used = {};
      for (const d in this.fit.data) {
        for (const pname in this.fit.data[d].parameters) {
          const p = this.fit.data[d].parameters[pname];
          if (p in n_used) {
            n_used[p] += 1;
          } else {
            n_used[p] = 1;
          }
        }
      }
      return n_used;
    }
  },
  methods: {
    ...mapMutations([
      "set_models",
      "set_choose_fit_open",
      "set_data_selection_open",
      "set_model_selection_open",
      "set_fit_data",
      "delete_fit_data",
      "delete_fit_models",
      "set_fit_parameters",
      "delete_fit_parameters",
      "set_fit_data_parameter",
      "fit_add_model",
      "fit_tie_to_data",
      "fit_tie_to_model",
      "fit_attach",
      "fit_detach_to_data",
      "clear_fit",
      "fit_apply_model",
      "delete_fit_detached_parameter"
    ]),
    update_datasets() {
      fetch(this.py + "/data_list", {}).then(async result => {
        this.db_data = await result.json();
        this.data_selection_render_index += 1;
        this.loaded = true;
      });
    },
    update_model_list() {
      fetch(this.py + "/model_list", {}).then(async result => {
        const models = await result.json();
        this.set_models(models);
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

      let model_id = null;
      for (const m in this.fit.models) {
        model_id = m;
      }

      let data_id;
      for (let i = 0; i < this.selected_dataset_ids.length; i++) {
        data_id = misc.data_uuid();
        this.set_fit_data({
          id: data_id,
          value: {
            id: this.selected_dataset_ids[i],
            name: this.selected_dataset_names[i],
            parent: this.selected_data_group,
            in_use: true,
            weight: "uniform",
            model: null,
            parameters: null
          }
        });
        if (model_id) {
          this.fit_apply_model({ data_id, model_id });
        }
      }

      // Clean up selection:
      this.selected_data_group = null;
      this.data_selection_render_index += 1; // This is a key that makes the element re-render
      if (first_add) {
        this.set_data_selection_open(false);
      }
    },
    add_model() {
      const first_add = Object.keys(this.fit["models"]).length === 0;

      this.fit_add_model({
        model_selected: this.model_selected
      });

      // Clean up selection:
      this.model_selected = null;
      this.model_selection_render_index += 1; // This is a key that makes the element re-render
      if (first_add) {
        this.set_model_selection_open(false);
      }
    },
    add_detached_parameter() {
      if (this.add_parameter_name !== "") {
        const p = misc.parameter_uuid();

        this.set_fit_parameters({
          id: p,
          value: {
            name: this.add_parameter_name,
            value: 1,
            const: false,
            type: "detached"
          }
        });

        this.add_parameter_name = "";
      }
    },
    tie_to_data(p_in) {
      this.fit_tie_to_data(p_in);
    },
    tie_to_model(model_id, parameter_name) {
      this.fit_tie_to_model({ model_id, parameter_name });
    },
    attach(p_id, detached_id) {
      this.fit_attach({ p_id, detached_id });
    },
    detach_to_data(data_id, parameter_name) {
      this.fit_detach_to_data({ data_id, parameter_name });
    },
    change_model(data_id, model_id) {
      this.fit_apply_model({ data_id, model_id });
    },
    delete_data(data_id, content) {
      if (!confirm(`Delete data ${content.parent} : ${content.name}?`)) {
        return;
      }
      this.delete_fit_data(data_id);
    },
    delete_detached_parameter(p_id, name) {
      if (!confirm(`Delete detached parameter ${name}?`)) {
        return;
      }
      this.delete_fit_detached_parameter(p_id);
    },
    delete_model(model_id, content) {
      if (!confirm(`Delete model ${content.print_name}?`)) {
        return;
      }
      this.delete_fit_models(model_id);
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

.jselect {
  border-radius: 5px;
  border: 1px solid #ccc;
  padding: 6px;
}
</style>
