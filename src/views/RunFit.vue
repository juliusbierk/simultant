<template>
  <div style="padding:10px" class="grid">
    <div class="row" v-if="loaded && Object.keys(fit.data).length === 0">
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
      <div class="cell-12">
        <div class="window">
          <div class="window-caption">
            <span class="title">Fit</span>
          </div>

          <div class="window-content p-2">
            <div class="row"></div>

            <div class="row">
              <div class="cell-8 offset-1">
                <div
                  v-show="fit_running"
                  data-role="progress"
                  data-type="line"
                  data-small="true"
                ></div>
              </div>

              <div class="cell-3">
                <button
                  class="button success defaultcursor"
                  @click="run_fit"
                  :disabled="fit_running"
                >
                  Fit
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row" v-if="Object.keys(fit.data).length > 0">
      <div class="cell-6">
        <div class="row">
          <div class="cell-12" v-show="Object.keys(fit.data).length > 0">
            <div class="window">
              <div class="window-caption">
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
                            <ParameterFit
                              :name="pname"
                              :id="pid"
                              :type="fit.parameters[pid].type"
                              :fit="fit.parameters[pid].fit"
                              view_in="data_section"
                              :detached_parameters="detached_parameters"
                              @initialValueChange="
                                initial_value_change(pid, $event)
                              "
                              :initial_value="fit.parameters[pid].value"
                              :is_const="fit.parameters[pid].const"
                              @changeValueType="change_value_type(pid)"
                            ></ParameterFit>
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
                          <ParameterFit
                            :name="pname"
                            :type="model_parameters[id][pname].type"
                            :id="model_parameters[id][pname].pid"
                            view_in="model_section"
                            :detached_parameters="detached_parameters"
                            @initialValueChange="
                              initial_value_change(
                                model_parameters[id][pname].pid,
                                $event
                              )
                            "
                            :initial_value="
                              model_parameters[id][pname].pid
                                ? fit.parameters[
                                    model_parameters[id][pname].pid
                                  ].value
                                : null
                            "
                            :fit="
                              model_parameters[id][pname].pid
                                ? fit.parameters[
                                    model_parameters[id][pname].pid
                                  ].fit
                                : null
                            "
                            :is_const="
                              model_parameters[id][pname].pid
                                ? fit.parameters[
                                    model_parameters[id][pname].pid
                                  ].const
                                : null
                            "
                            @changeValueType="change_value_type(model_parameters[id][pname].pid)"
                          ></ParameterFit>
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
                <span class="title">Detached Parameters</span>
              </div>

              <div class="window-content p-2">
                <div
                  class="row"
                  v-for="(name, id) in detached_parameters"
                  :key="id"
                >
                  <div class="offset-1">
                    <ParameterFit
                      :name="name"
                      type="detached"
                      :id="id"
                      :fit="fit.parameters[id].fit"
                      view_in="detached_section"
                      :detached_parameters="detached_parameters"
                      @initialValueChange="initial_value_change(id, $event)"
                      :initial_value="fit.parameters[id].value"
                      :is_const="fit.parameters[id].const"
                      @changeValueType="change_value_type(id)"
                    ></ParameterFit>
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
import ParameterFit from "@/components/ParameterFit.vue";
import ShowCode from "@/components/ShowCode.vue";
import store from "@/store";
import { mapState, mapGetters, mapMutations } from "vuex";

export default {
  name: "SpecifyFit",
  store,
  data: function() {
    return {
      py: "http://127.0.0.1:7555",
      loaded: false,
      fit_running: false
    };
  },
  components: {
    BasicPlot,
    ParameterFit,
    ShowCode
  },
  computed: {
    ...mapState({
      fit: "fit",
      models: "models"
    }),
    ...mapGetters(["detached_parameters", "model_parameters"])
  },
  methods: {
    ...mapMutations(["fit_set_initial_value", "fit_set_fit_value", "fit_toggle_parameter_value_type"]),
    initial_value_change(pid, string_value) {
      const value = parseFloat(string_value);
      this.fit_set_initial_value({ pid, value });
    },
    change_value_type(pid) {
      this.fit_toggle_parameter_value_type(pid);
    },
    run_fit() {
      fetch(this.py + "/run_fit", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(this.fit)
      }).then(async result => {
        const r = await result.json();
        if (r["status"] === "started") {
          this.fit_running = true;
          this.wait_for_fit();
        }
      });
    },
    wait_for_fit() {
      fetch(this.py + "/fit_result").then(async result => {
        const r = await result.json();
        if (r["status"] === "success") {
          this.fit_running = false;
          for (const pid in r["fit"]) {
            this.fit_set_fit_value({ pid, value: r["fit"][pid] });
          }
        } else {
          setTimeout(this.wait_for_fit, 100);
        }
      });
    }
  },
  mounted: function() {
    this.loaded = true;
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
