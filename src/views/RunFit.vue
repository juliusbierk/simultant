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
            <div class="row">
              <div class="cell-10 offset-1">
                <div id="plot"></div>
              </div>
            </div>

            <div class="row text-center">
              <div class="cell-1 offset-2" v-if="!plot_running">
                <button class="button defaultcursor" v-show="fit_running">
                  <span class="ml-1">{{ iteration }}</span>
                  <span class="badge">iteration</span>
                </button>
              </div>

              <div
                class="cell-1 offset-2"
                style="position: relative; top:5px"
                v-if="plot_running"
              >
                <small>Plotting</small>
              </div>

              <div class="cell-3">
                <div
                  id="progress1"
                  v-show="fit_running || plot_running"
                  data-role="progress"
                  data-type="line"
                  data-small="true"
                  :style="{
                    position: 'relative',
                    top: '15px',
                    'background-color': interrupting_fit
                      ? '#ff7615 !important'
                      : undefined
                  }"
                ></div>

                <div v-show="!(fit_running || plot_running)">
                  Method:
                  <select v-model="method">
                    <option value="anagrad"
                      >Analytical Gradient Descent (L-BFGS-B)</option
                    >
                    <option value="nelder-mead"
                      >Gradient-free Nelder-Mead</option
                    >
                    >
                  </select>
                  {{ method }}
                </div>
              </div>

              <div class="cell-1">
                <button
                  class="button defaultcursor"
                  v-show="fit_running && loss"
                >
                  <span class="ml-1">{{
                    loss ? loss.toPrecision(6) : loss
                  }}</span>
                  <span class="badge">loss</span>
                </button>
              </div>

              <div class="cell-1">
                <button
                  class="button warning"
                  v-show="fit_running"
                  @click="interrupt_fit"
                  :disabled="interrupting_fit"
                >
                  Stop fit
                </button>
              </div>

              <div class="cell-4">
                <button
                  class="button defaultcursor"
                  @click="reset_fit_update_plot"
                  :disabled="fit_running || plot_running"
                >
                  Reset
                </button>

                <button
                  class="button defaultcursor"
                  @click="update_plot"
                  :disabled="fit_running || plot_running"
                >
                  Update Plot
                </button>

                <button
                  class="button success defaultcursor"
                  @click="run_fit"
                  :disabled="fit_running || plot_running"
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
                          <span style="position: relative; top: 5px">
                            <input
                              type="checkbox"
                              data-role="checkbox"
                              :checked="content.in_use"
                              @change="toggle_in_use(id)"
                            />
                          </span>
                          {{ content.parent }} : {{ content.name }}
                        </div>
                        <div class="cell-6" v-if="fit.models[content.model]">
                          Applied Model:
                          {{ fit.models[content.model].print_name }}
                        </div>
                      </div>
                    </div>

                    <div
                      class="card-content"
                      v-if="Object.keys(content.parameters).length > 0"
                    >
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
                            @changeValueType="
                              change_value_type(model_parameters[id][pname].pid)
                            "
                          ></ParameterFit>
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

          <div class="cell-12" v-show="this.is_fitted">
            <div class="window">
              <div class="window-caption">
                <span class="title">Download fit</span>
              </div>

              <div class="window-content p-2">
                <div class="cell-5 offset-5">
                  <button class="button defaultcursor" @click="download_fit">
                    Download
                  </button>
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
import Plotly from "plotly.js-dist";
import plotlysettings from "@/plotsettings.js";
import _ from "lodash";
import config from "@/config.js";

export default {
  name: "SpecifyFit",
  store,
  data: function() {
    return {
      py: config.py,
      loaded: false,
      plot_running: true,
      plot_created: false,
      interrupting_fit: false,
      iteration: 0,
      loss: null,
      is_mounted: true,
      is_fitted: false,
      method: "anagrad"
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
    ...mapState(["fit_running"]),
    ...mapGetters(["detached_parameters", "model_parameters"])
  },
  methods: {
    ...mapMutations([
      "fit_set_initial_value",
      "fit_set_fit_value",
      "fit_toggle_parameter_value_type",
      "set_fit_running"
    ]),
    initial_value_change(pid, string_value) {
      const value = parseFloat(string_value);
      this.fit_set_initial_value({ pid, value });
    },
    change_value_type(pid) {
      this.fit_toggle_parameter_value_type(pid);
    },
    toggle_in_use(pid) {
      alert(pid);
    },
    run_fit() {
      this.iteration = 0;
      this.loss = null;
      this.interrupting_fit = false;

      let method_fit = _.cloneDeep(this.fit);
      method_fit.method = this.method;

      fetch(this.py + "/run_fit", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(method_fit)
      }).then(async result => {
        const r = await result.json();
        if (r["status"] === "started") {
          this.set_fit_running(true);
          this.wait_for_fit();
        }
      });
    },
    interrupt_fit() {
      this.interrupting_fit = true;
      fetch(this.py + "/interrupt_fit", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        }
      });
    },
    reset_fit() {
      for (const pid in this.fit.parameters) {
        this.fit_set_fit_value({ pid, value: null });
      }
    },
    reset_fit_update_plot() {
      this.reset_fit();
      this.update_plot();
    },
    wait_for_fit() {
      fetch(this.py + "/fit_result").then(async result => {
        if (result.status !== 200) {
          alert("Could not run fit, got HTTP code " + result.status.toString());
        }

        const r = await result.json();
        if (r["status"] === "success") {
          this.set_fit_running(false);
          this.interrupting_fit = false;

          // First null all
          this.reset_fit();

          // Then fill out the non-consts:
          for (const pid in r["fit"]) {
            this.fit_set_fit_value({ pid, value: r["fit"][pid] });
          }

          this.update_plot();
        } else {
          if (r.info) {
            console.log(r.info);
            this.iteration = r.info.iteration;
            this.loss = r.info.loss;
          }

          if (this.loaded) {
            setTimeout(this.wait_for_fit, 100);
          }
        }
      });
    },
    download_fit() {
      fetch(this.py + "/download_fit", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(this.fit)
      })
        .then(response => response.blob())
        .then(blob => {
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.href = url;
          a.download = "fit.json";
          document.body.appendChild(a); // we need to append the element to the dom -> otherwise it will not work in firefox
          a.click();
          a.remove(); //afterwards we remove the element again
        });
    },
    update_plot() {
      if (!this.plot_created) {
        // fixing caching issue
        document.getElementById("plot").innerHTML = "";
      }

      this.plot_running = true;
      fetch(this.py + "/plot_fit", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(this.fit)
      }).then(async result => {
        let res = await result.json();
        this.is_fitted = res["is_fitted"];
        res = res["plots"];
        let layout = _.cloneDeep(plotlysettings.layout);

        if (this.plot_created) {
          Plotly.react("plot", res, layout, plotlysettings.settings);
        } else {
          Plotly.newPlot("plot", res, layout, plotlysettings.settings);
        }
        this.plot_created = true;
        this.plot_running = false;
      });
    }
  },
  mounted: function() {
    this.loaded = true;
    if (Object.keys(this.fit.data).length > 0) {
      this.update_plot();
    }
    if (this.fit_running) {
      this.wait_for_fit();
    }
  },
  beforeUnmount: function() {
    this.loaded = false;
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

#progress2.line::before {
  animation-delay: -0.8s;
}
</style>
