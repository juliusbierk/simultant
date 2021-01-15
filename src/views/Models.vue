<template>
  <div style="padding:10px" class="grid">
    <div class="row">
      <div class="cell">
        <div class="window">
          <div class="window-caption">
            <!--            <span class="icon mif-windows"></span>-->
            <span class="title">Existing Models</span>

            <div class="buttons">
              <span
                ><button
                  v-show="!add_model"
                  style="margin-right:20px"
                  class="button secondary small defaultcursor"
                  @click="toggle_add_model"
                >
                  + Create New Model
                </button></span
              >
            </div>
          </div>
          <div class="window-content p-2">
            ...
          </div>
        </div>
      </div>

      <div class="cell" v-show="add_model">
        <div class="window">
          <div class="window-caption">
            <!--            <span class="icon mif-windows"></span>-->
            <span class="title">Create New Model</span>
            <div class="buttons">
              <span
                class="btn-close defaultcursor"
                @click="toggle_add_model"
              ></span>
            </div>
          </div>
          <div class="window-content p-2">
            <form data-role="validator" data-interactive-check="true">
              <input
                type="text"
                data-role="input"
                data-prepend="Name: "
                v-model="name"
                @change="update_name"
                v-on:keyup="update_name"
                data-validate="pattern=(^[a-zA-Z_][\sa-zA-Z0-9_]*$)"
              />
              <span class="invalid_feedback">
                Not a valid model name.
              </span>
            </form>
            <p></p>

            <ul data-role="tabs" data-tabs-type="group" data-expand="true">
              <li><a href="#" @click="change_to_expr">Expression</a></li>
              <li>
                <a href="#" @click="change_to_ode"
                  >Ordinary Differential Equation</a
                >
              </li>
            </ul>

            <form
              v-show="!expr_mode"
              data-role="validator"
              data-interactive-check="true"
            >
              <div class="row">
                <div
                  class="cell-6"
                  data-role="hint"
                  data-hint-text="The dimension of the ODE"
                  hintHide="0"
                  data-cls-hint="bg-lightCyan fg-white"
                >
                  <input
                    @change="delayed_check_model"
                    type="text"
                    data-role="input"
                    data-prepend="Dimension (y):"
                    data-validate="pattern=(^[1-9_][0-9_]*$)"
                    v-model="ode_dim"
                  />
                  <span class="invalid_feedback">
                    Must be an integer > 0.
                  </span>
                </div>

                <div
                  class="cell-6"
                  data-role="hint"
                  data-hint-text="The index of y containing the fit function"
                  hintHide="0"
                  data-cls-hint="bg-lightCyan fg-white"
                >
                  <input
                    @change="delayed_check_model"
                    type="text"
                    data-role="input"
                    data-prepend="Function index (y):"
                    :data-validate="'min=0 max=' + (ode_dim - 1).toString()"
                    v-model="ode_dim_select"
                  />
                  <span class="invalid_feedback">
                    Select a dimension index (0 - {{ ode_dim - 1 }}).
                  </span>
                </div>
              </div>
            </form>

            <p></p>

            <div id="code"></div>

            <p></p>

            <div class="grid">
              <div v-if="code_error" class="row">
                <div class="offset-1 cell-10">
                  <div
                    class="remark alert"
                    style="margin-top:0; margin-bottom:0"
                  >
                    <b>Code error:</b> {{ code_error }}
                  </div>
                </div>
              </div>
              <div v-else class="row">
                <div class="offset-1 cell-10">
                  <div
                    class="remark success"
                    style="margin-top:0; margin-bottom:0"
                  >
                    <b>Code status:</b> Running.
                  </div>
                </div>
              </div>

              <div v-if="parameters" class="row">
                <div class="offset-1 cell-10">
                  <div
                    class="remark primary"
                    style="margin-top:0; margin-bottom:0"
                  >
                    <b>Parameters:</b>

                    <button
                      v-for="p in parameters"
                      v-bind:key="p.name"
                      style="margin-left:5px; margin-top:3px; margin-bottom:3px"
                      data-role="hint"
                      hintHide="0"
                      :data-hint-text="'Default value: ' + p.value.toString()"
                      data-cls-hint="bg-lightCyan fg-white"
                      class="defaultcursor button secondary small rounded outline"
                    >
                      {{ p.name }}
                    </button>
                  </div>
                </div>
              </div>

              <div v-if="running_code" class="row">
                <div class="offset-1 cell-10">
                  <div
                    data-role="progress"
                    data-type="line"
                    data-small="true"
                  ></div>
                </div>
              </div>

              <p></p>

              <div class="row">
                <div class="cell-5 offset-1">
                  <button
                    @click="reset"
                    class="defaultcursor button"
                    style="margin-right:10px"
                  >
                    Reset
                  </button>
                </div>

                <div class="cell-4 offset-1">
                  <div class="d-flex flex-row-r">
                    <button
                      v-if="!running_code && !code_error"
                      class="defaultcursor button success"
                      style="margin-right:10px"
                    >
                      Add Model
                    </button>

                    <button
                      v-if="!running_code && !code_error"
                      class="defaultcursor button secondary"
                      style="margin-right:10px"
                      @click="make_main_plot"
                    >
                      Plot
                    </button>
                  </div>
                </div>
              </div>

              <p></p>

              <div class="row">
                 <div class="cell-11">
                   <div id="add_plot"></div>
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
// @ is an alias to /src
// import HelloWorld from "@/components/HelloWorld.vue";

import CodeMirror from "codemirror";
import "codemirror/mode/python/python.js";
import _ from "lodash";
import Plotly from "plotly.js-dist";
import plotlysettings from "@/plotsettings.js";

export default {
  name: "Home",
  data: function() {
    return {
      py: "http://127.0.0.1:7555",
      name: "New Model",
      expr_mode: true,
      code: null,
      ode_code: null,
      orig_code: "def New_Model(x, a=1, b=1):\n    return a + b * x\n",
      orig_ode_code:
        "def New_Model(x, y, a=1, b=1):\n    return a * y[1], -b * y[0]\n",
      cmcode: null,
      marker: null,
      add_model: false,
      parameters: null,
      code_error: null,
      running_code: false,
      ode_dim: 2,
      ode_dim_select: 0,
    };
  },
  computed: {
    name_underscore: function() {
      return this.name.split(" ").join("_");
    }
  },
  components: {
    // HelloWorld
  },
  methods: {
    reset() {
      this.code = this.orig_code;
      this.ode_code = this.orig_ode_code;
      this.expr_mode = true;
      this.ode_dim = 2;
      this.ode_dim_select = 0;
      this.name = "New Model";

      window.cmcode.setValue(this.code);

      this.marker = window.cmcode.markText(
        { line: 0, ch: 0 },
        { line: 0, ch: 16 },
        { readOnly: true }
      );

      this.check_model();
    },
    toggle_add_model() {
      this.add_model = !this.add_model;
      setTimeout(() => {
        window.cmcode.refresh();
      }, 5);
    },
    change_to_expr() {
      if (!this.expr_mode) {
        this.expr_mode = true;
        window.cmcode.setValue(this.code);
        this.update_name();
      }
    },
    change_to_ode() {
      if (this.expr_mode) {
        this.expr_mode = false;
        window.cmcode.setValue(this.ode_code);
        this.update_name();
      }
    },
    update_name() {
      this.marker.clear();
      var i2 = window.cmcode.getValue().indexOf("(x,");
      var s = "def " + this.name_underscore + "(x,";
      window.cmcode.replaceRange(
        s,
        { line: 0, ch: 0 },
        { line: 0, ch: i2 + 3 }
      );
      this.marker = window.cmcode.markText(
        { line: 0, ch: 0 },
        { line: 0, ch: s.length + (this.expr_mode ? 0 : 3) },
        { readOnly: true }
      );
    },
    check_model() {
      var c = this.expr_mode ? this.code : this.ode_code;
      fetch(this.py + "/check_code", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          code: c,
          expr_mode: this.expr_mode,
          name_underscore: this.name_underscore,
          name: this.name,
          ode_dim: parseInt(this.ode_dim),
          ode_dim_select: parseInt(this.ode_dim_select)
        })
      }).then(async result => {
        var res = await result.json();
        this.running_code = false;
        this.parameters = res.args;
        this.code_error = res.error;
      });
    },
    make_main_plot() {
      var c = this.expr_mode ? this.code : this.ode_code;
      var body = {
          code: c,
          expr_mode: this.expr_mode,
          name_underscore: this.name_underscore,
          name: this.name,
          ode_dim: parseInt(this.ode_dim),
          ode_dim_select: parseInt(this.ode_dim_select)
        };
      var url = this.py + '/plot_code';

      fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
      }).then(async result => {
        var res = await result.json();
        res.mode = "lines";
        Plotly.newPlot("add_plot", [res], plotlysettings.layout, plotlysettings.settings);
      });
    },
    delayed_check_model() {
      this.running_code = true;

      setTimeout(() => {
        this.check_model();
      }, 1000);
    }
  },
  mounted: function() {
    function betterTab(cm) {
      if (cm.somethingSelected()) {
        cm.indentSelection("add");
      } else {
        cm.replaceSelection(
          cm.getOption("indentWithTabs")
            ? "\t"
            : Array(cm.getOption("indentUnit") + 1).join(" "),
          "end",
          "+input"
        );
      }
    }

    this.code = this.orig_code;
    this.ode_code = this.orig_ode_code;

    // For some reason assigning CodeMirror to vue data breaks codemirror, so we assign to window:
    window.cmcode = CodeMirror(document.querySelector("#code"), {
      lineNumbers: true,
      mode: "python",
      tabSize: 4,
      indentUnit: 4,
      value: this.code,
      extraKeys: { Tab: betterTab }
    });

    this.marker = window.cmcode.markText(
      { line: 0, ch: 0 },
      { line: 0, ch: 16 },
      { readOnly: true }
    );

    this.check_model();

    var throttled_check_model = _.debounce(this.check_model, 1000);
    window.cmcode.on("change", cm => {
      if (this.expr_mode) {
        this.code = cm.getValue();
      } else {
        this.ode_code = cm.getValue();
      }
      this.running_code = true;
      throttled_check_model();
    });

    window.cmcode.on("paste", (cm, t) => {
      console.log("We are not handling pasting very well yet.");
    });
  }
};
</script>

<style></style>
