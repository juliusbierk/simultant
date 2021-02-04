<template>
  <div style="padding:10px" class="grid">
    <div class="row" v-if="Object.keys(fit.data).length === 0">
      <div class="cell-6 offset-3">
        <div class="remark alert">
          No fit has been loaded. Go to
          <button
            class="button defaultcursor"
            @click="$router.push('/specifyfit')"
          >
            Fit Topology
          </button>
          to specify fit.
        </div>
      </div>
    </div>

    <div class="row" v-if="Object.keys(fit.data).length > 0">
      <div class="cell-6">
        <div class="row">
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
                            <!--                            <ParameterType-->
                            <!--                              :name="pname"-->
                            <!--                              :id="pid"-->
                            <!--                              :type="fit.parameters[pid].type"-->
                            <!--                              @tieToModel="tie_to_model(content.model, pname)"-->
                            <!--                              view_in="data_section"-->
                            <!--                              @attach="attach(pid, $event)"-->
                            <!--                              @detach="detach_to_data(id, pname)"-->
                            <!--                              :detached_parameters="detached_parameters"-->
                            <!--                            ></ParameterType>-->
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
                          <!--                          <ParameterType-->
                          <!--                            :name="pname"-->
                          <!--                            :type="model_parameters[id][pname].type"-->
                          <!--                            @tieToData="-->
                          <!--                              tie_to_data(model_parameters[id][pname].pid)-->
                          <!--                            "-->
                          <!--                            @tieToModel="tie_to_model(id, pname)"-->
                          <!--                            @attach="-->
                          <!--                              attach(model_parameters[id][pname].pid, $event)-->
                          <!--                            "-->
                          <!--                            @detach="tie_to_model(id, pname)"-->
                          <!--                            :id="model_parameters[id][pname].pid"-->
                          <!--                            view_in="model_section"-->
                          <!--                            :detached_parameters="detached_parameters"-->
                          <!--                          ></ParameterType>-->
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
            <div
              class="window"
              v-show="Object.keys(detached_parameters).length > 0"
            >
              <div class="window-caption">
                <!--            <span class="icon mif-windows"></span>-->
                <span class="title">Detached Parameters</span>
              </div>

              <div class="window-content p-2">
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
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import BasicPlot from "@/components/BasicPlot.vue";
import ParameterType from "@/components/ParameterType.vue";
import ShowCode from "@/components/ShowCode.vue";
import store from "@/store";
import misc from "@/misc.js";
import { mapState, mapGetters, mapMutations } from "vuex";

export default {
  name: "SpecifyFit",
  store,
  data: function() {
    return {
      py: "http://127.0.0.1:7555",
      db_data: {},
      selected_data_group: null,
      selected_dataset_ids: null,
      selected_dataset_names: null,
      model_selected: null,
      data_selection_render_index: 0,
      model_selection_render_index: 0,
      apply_to_all: true,
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
      models: "models"
    }),
    ...mapGetters(["detached_parameters", "model_parameters"])
  },
  methods: {}
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
