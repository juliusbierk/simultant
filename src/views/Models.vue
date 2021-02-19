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
                >
                  Import Model
                </button></span
              >

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
            <div class="row">
              <div
                v-for="(content, name) in models"
                v-bind:key="name"
                v-bind:class="{ 'cell-12': add_model, 'cell-6': !add_model }"
              >
                <div class="card">
                  <div class="card-header">
                    <div class="row">
                      <div class="cell-5">
                        <button
                          class="defaultcursor button light"
                          @click="edit_model(name)"
                        >
                          <span style="font-size: 18px;" class="ml-1"
                            >&#9998; {{ name }}</span
                          >
                          <span v-if="!content.expr_mode" class="badge"
                            >ODE</span
                          >
                        </button>
                      </div>

                      <div class="offset-2">
                        <input
                          @click="content.show_plot = !content.show_plot"
                          type="checkbox"
                          data-role="switch"
                          data-caption="Plot"
                        />
                        <span style="margin-right:50px"></span>
                        <input
                          @click="content.show_code = !content.show_code"
                          type="checkbox"
                          data-role="switch"
                          data-caption="Code"
                        />
                        <span style="margin-right:50px"></span>
                        <button
                          style="position:relative; bottom:5px"
                          class="button light"
                          @click="delete_model(name)"
                        >
                          &#9587;
                        </button>
                      </div>
                    </div>

                    <div class="row">
                      <div class="cell-5">
                        <span class="ml-1">
                          Parameters:
                          <button
                            v-for="p in content.args"
                            v-bind:key="p.name"
                            style="margin-left:5px; margin-top:3px; margin-bottom:3px"
                            data-role="hint"
                            data-hint-hide="0"
                            :data-hint-text="
                              'Default value: ' + p.value.toString()
                            "
                            data-cls-hint="bg-lightCyan fg-white"
                            class="defaultcursor button secondary small rounded outline"
                          >
                            {{ p.name }}
                          </button>
                        </span>
                      </div>
                    </div>
                  </div>
                  <div v-if="content.show_plot" class="card-content p-2">
                    <BasicPlot
                      :url="this.py + '/plot_code'"
                      :body="content"
                      :dataplot="false"
                    ></BasicPlot>
                  </div>
                  <div v-if="content.show_code" class="card-footer p-2">
                    <ShowCode
                      :code="
                        (content.expr_mode
                          ? ''
                          : '# Output dimension = ' +
                            content.ode_dim_select.toString() +
                            '\n') + content.code
                      "
                    ></ShowCode>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="cell" v-show="add_model">
        <div class="window">
          <div class="window-caption">
            <!--            <span class="icon mif-windows"></span>-->
            <span class="title">{{
              is_editing_model ? "Edit Model" : "Create New Model"
            }}</span>
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
                v-on:keyup="update_name_not_edit"
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
                  data-hint-hide="0"
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
                  v-show="!has_transform_function"
                  class="cell-6"
                  data-role="hint"
                  data-hint-text="The index of y containing the fit function"
                  data-hint-hide="0"
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

                <div
                  v-show="has_transform_function"
                  class="cell-6"
                  data-role="hint"
                  data-hint-text="This is not needed when using a _transform function."
                  data-hint-hide="0"
                  data-cls-hint="bg-lightCyan fg-white"
                >
                  <input
                    type="text"
                    data-role="input"
                    data-prepend="Function index (y):"
                    v-model="ode_dim_select"
                    disabled
                  />
                  <span class="invalid_feedback">
                    Select a dimension index (0 - {{ ode_dim - 1 }}).
                  </span>
                </div>
              </div>
            </form>

            <p></p>

            <div id="code"></div>

            <div class="row" v-if="!expr_mode">
              <div class="offset-1 cell-10">
                <span v-show="!show_advanced_options">
                  <button
                    class="button small light"
                    @click="show_advanced_options = true"
                  >
                    Advanced options
                  </button>
                </span>

                <span v-show="show_advanced_options">
                  <button
                    style="margin-right:3px"
                    class="button small light"
                    @click="show_advanced_options = false"
                  >
                    Hide advanced options
                  </button>
                  <button
                    style="margin-right:3px"
                    class="button small"
                    @click="add_transform_ode_code"
                  >
                    Add transform code
                  </button>
                  <button
                    style="margin-right:3px"
                    class="button small"
                    @click="add_event_transform_ode_code"
                  >
                    Add transform code with event-state
                  </button>
                </span>
              </div>
            </div>

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

              <div v-if="show_bound_info" class="row">
                <div class="offset-1 cell-10">
                  <div
                    class="remark warning"
                    style="margin-top:0; margin-bottom:0"
                  >
                    <b>Bounds:</b> Parameters default to being positive. Write
                    e.g. <kbd>a: R[lower:upper]</kbd> to bound parameter
                    <kbd>a</kbd> in the function definition. To bound with just
                    one limit use e.g. <kbd>a: R[0:]</kbd> to bound between 0
                    and &infin;. And use <kbd>a: R[:]</kbd> to make a parameter
                    unbounded. (If you use multiple models in a fit that share
                    detached parameters, the bounds will be taken from an
                    arbitrary function.)
                    <button
                      style="margin-right: 3px"
                      class="button light small"
                      @click="bounds_example"
                    >
                      Add Example Code
                    </button>
                    <button
                      class="button light small"
                      @click="show_bound_info = false"
                    >
                      Hide bounds information
                    </button>
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
                      data-hint-hide="0"
                      :data-hint-text="parameter_info_text(p)"
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

                  <button
                    class="defaultcursor button"
                    style="margin-right:10px"
                    @click="show_bound_info = !show_bound_info"
                  >
                    {{ show_bound_info ? "Hide bounds information" : "Bounds" }}
                  </button>
                </div>

                <div class="cell-4 offset-1">
                  <div class="d-flex flex-row-r">
                    <button
                      v-if="!running_code && !code_error"
                      class="defaultcursor button success"
                      style="margin-right:10px"
                      @click="submit_model"
                    >
                      {{ is_editing_model ? "Commit Model" : "Add Model" }}
                    </button>

                    <button
                      v-if="!running_code && !code_error"
                      class="defaultcursor button secondary"
                      style="margin-right:10px"
                      @click="show_plot = !show_plot"
                    >
                      {{ show_plot ? "Hide Plot" : "Show Plot" }}
                    </button>
                  </div>
                </div>
              </div>

              <p></p>

              <div class="row" v-if="show_plot && !running_code && !code_error">
                <div class="cell-11">
                  <BasicPlot
                    ref="add_plot"
                    :url="this.py + '/plot_code'"
                    :body="plot_body"
                    :dataplot="false"
                  ></BasicPlot>
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

import BasicPlot from "@/components/BasicPlot.vue";
import ShowCode from "@/components/ShowCode.vue";
import CodeMirror from "codemirror";
import "codemirror/mode/python/python.js";
import _ from "lodash";
import { mapMutations } from "vuex";
import config from "@/config.js";

export default {
  name: "Models",
  data: function() {
    return {
      py: config.py,
      name: "New Model",
      expr_mode: true,
      code: null,
      ode_code: null,
      orig_code: "def New_Model(x, *, a=1, b=1):\n    return a * tanh(b * x)\n",
      orig_ode_code:
        "def New_Model(x, y, *, y0=[1, 1], a=1, b=1):\n    return a * y[1], -b * y[0]\n",
      transform_code:
        "\n\ndef _transform(x, y, **kw):\n" +
        "    # This function is called after the ODE is solved\n" +
        "    # and should transform to the fit function.\n" +
        "    # `kw` will contain all parameters.\n" +
        "    return y[]\n",
      event_code:
        "\n\ndef _transform(x, y, x_event, y_event, **kw):\n" +
        "    # This function is called after the ODE is solved\n" +
        "    # and should transform to the fit function.\n" +
        "    # `kw` will contain all parameters.\n" +
        "    # x_event and y_event are the (first) values when the\n" +
        "    # `event` function evaluates to zero.\n" +
        "    return y[]\n\n" +
        "def _event(x, y, **kwargs):\n" +
        "    # Defines an event time. This can be used to define e.g.\n" +
        "    # a specific value-crossing or a steady state\n" +
        "    return y[0]\n\n" +
        "_event.direction = 0   # -1 = pos -> neg, 1 = neg -> pos, 0 = any zero-crossing \n" +
        "_event.X_factor = 25   # how much longer than the largest x to wait for event to happen \n",
      bounds_example_code:
        "\n\ndef bounds_example(x, *, a: R[:]=0, \n" +
        "                         b: R[1:2], \n" +
        "                         c):\n" +
        "    return a * x**b + c\n",
      bounds_example_ode_code:
        "\n\ndef bounds_example(x, y, *, y0: R[:], \n" +
        "                            a: R[0:10]=1, \n" +
        "                            b: R[1:2], \n" +
        "                            c):\n" +
        "    return a * y**b + c\n",
      cmcode: null,
      last_code_check: null,
      marker: null,
      add_model: false,
      parameters: null,
      code_error: null,
      running_code: false,
      ode_dim: 2,
      ode_dim_select: 0,
      show_plot: false,
      plot_body: null,
      models: {},
      show_advanced_options: false,
      is_editing_model: false,
      show_bound_info: false
    };
  },
  computed: {
    name_underscore: function() {
      return this.name.split(" ").join("_");
    },
    has_transform_function: function() {
      if (this.ode_code) {
        return this.ode_code.includes("def _transform");
      } else {
        return true;
      }
    },
    using_bounds: function() {
      if (!this.expr_mode && this.ode_code) {
        return (
          this.ode_code.includes(":R[") ||
          this.ode_code.includes(": R[") ||
          this.ode_code.includes(":  R[")
        );
      } else if (this.expr_mode && this.code) {
        return (
          this.code.includes(":R[") ||
          this.code.includes(": R[") ||
          this.code.includes(":  R[")
        );
      } else {
        return false;
      }
    }
  },
  components: {
    BasicPlot,
    ShowCode
  },
  methods: {
    ...mapMutations(["clear_fit"]),
    parameter_info_text(p) {
      let r = "Default = " + p.value.toString();
      if (p.lower == null && p.upper == null) {
        r += ", unbounded";
      } else if (p.lower == null) {
        r += ", smaller than " + p.upper.toString();
      } else if (p.upper == null) {
        if (p.lower === 0) {
          r += ", positive parameter";
        } else {
          r += ", larger than " + p.lower.toString();
        }
      } else {
        r +=
          ", in interval [" +
          p.lower.toString() +
          ", " +
          p.upper.toString() +
          "]";
      }
      return r;
    },
    add_transform_ode_code() {
      this.ode_code =
        this.ode_code +
        this.transform_code.replace(
          "[]",
          "[" + this.ode_dim_select.toString() + "]"
        );
      window.cmcode.setValue(this.ode_code);
      this.show_advanced_options = false;
    },
    add_event_transform_ode_code() {
      this.ode_code =
        this.ode_code +
        this.event_code.replace(
          "[]",
          "[" + this.ode_dim_select.toString() + "]"
        );
      window.cmcode.setValue(this.ode_code);
      this.show_advanced_options = false;
    },
    bounds_example() {
      if (this.expr_mode) {
        this.code = this.code + this.bounds_example_code;
        window.cmcode.setValue(this.code);
      } else {
        this.ode_code = this.ode_code + this.bounds_example_ode_code;
        window.cmcode.setValue(this.ode_code);
      }
    },
    edit_model(model_name) {
      this.is_editing_model = true;
      this.expr_mode = !this.models[model_name].expr_mode; // weird, but we change after
      this.name = this.models[model_name].name;

      if (this.models[model_name].expr_mode) {
        this.code = this.models[model_name].code;
        this.change_to_expr();
      } else {
        this.ode_code = this.models[model_name].code;
        this.ode_dim = this.models[model_name].ode_dim;
        this.ode_dim_select = this.models[model_name].ode_dim_select;
        this.change_to_ode();
      }

      this.add_model = true;
      setTimeout(() => {
        window.cmcode.refresh();
      }, 5);
    },
    update_model_list() {
      fetch(this.py + "/model_list", {}).then(async result => {
        var res = await result.json();
        for (const name of Object.keys(res)) {
          if (this.models[name]) {
            res[name].show_plot = this.models[name].show_plot;
            res[name].show_code = this.models[name].show_code;
          } else {
            res[name].show_plot = false;
            res[name].show_code = false;
          }
        }
        this.models = res;
        if (Object.keys(res).length === 0) {
          this.toggle_add_model();
        }
      });
    },
    delete_model(name) {
      if (!confirm("Delete model?")) {
        return;
      }
      fetch(this.py + "/delete_model", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ name })
      }).then(async result => {
        await result.json();
        this.clear_fit();
        this.update_model_list();
      });
    },
    submit_model() {
      var c = this.expr_mode ? this.code : this.ode_code;
      var body = {
        code: c,
        expr_mode: this.expr_mode,
        name_underscore: this.name_underscore,
        name: this.name,
        ode_dim: parseInt(this.ode_dim),
        ode_dim_select: parseInt(this.ode_dim_select)
      };

      fetch(this.py + "/model_exist_check", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
      }).then(async result => {
        var res = await result.json();
        if (res["exists"] && !this.is_editing_model) {
          if (!confirm("Model exists. Overwrite?")) {
            return;
          }
        }

        fetch(this.py + "/add_model", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(body)
        }).then(async result => {
          let success = false;
          var res = await result.json();
          if (res.success) {
            success = true;
          }
          if (!success) {
            alert("Could not add model");
            return;
          }

          this.clear_fit();
          this.toggle_add_model();
          this.update_model_list();
        });
      });
    },
    reset() {
      let sure_reset = confirm("Reset model?");
      if (!sure_reset) {
        return;
      }
      if (this.$refs.add_plot) {
        this.$refs.add_plot.reset_scale();
      }

      this.code = this.orig_code;
      this.ode_code = this.orig_ode_code;
      this.expr_mode = true;
      this.ode_dim = 2;
      this.ode_dim_select = 0;
      this.name = "New Model";

      window.cmcode.setValue(this.code);

      this.marker = window.cmcode.markText(
        { line: 0, ch: 0 },
        { line: 0, ch: 19 },
        { readOnly: true }
      );

      this.check_model();
    },
    toggle_add_model() {
      this.add_model = !this.add_model;
      setTimeout(() => {
        window.cmcode.refresh();
      }, 5);
      this.is_editing_model = false;
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
    update_name_not_edit() {
      this.is_editing_model = false;
      this.update_name();
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
        { line: 0, ch: s.length + (this.expr_mode ? 3 : 9) },
        { readOnly: true }
      );
    },
    check_model() {
      var c = this.expr_mode ? this.code : this.ode_code;
      var body = {
        code: c,
        expr_mode: this.expr_mode,
        name_underscore: this.name_underscore,
        name: this.name,
        ode_dim: parseInt(this.ode_dim),
        ode_dim_select: parseInt(this.ode_dim_select)
      };

      fetch(this.py + "/check_code", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
      }).then(async result => {
        var res = await result.json();
        this.running_code = false;
        this.parameters = res.args;
        this.code_error = res.error;
      });

      // Plot
      this.plot_body = body;
    },
    delayed_check_model() {
      this.running_code = true;

      setTimeout(() => {
        this.check_model();
      }, 1000);
    }
  },
  mounted: function() {
    this.update_model_list();

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
    document.getElementById("code").innerHTML = "";
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
      { line: 0, ch: 19 },
      { readOnly: true }
    );

    this.check_model();

    var throttled_check_model = _.debounce(this.check_model, 1000);
    window.cmcode.on("change", cm => {
      if (this.expr_mode) {
        this.code = cm.getValue();
        if (this.last_code_check === this.code) {
          return;
        }
        this.last_code_check = this.code;
      } else {
        this.ode_code = cm.getValue();
        if (this.last_code_check === this.ode_code) {
          return;
        }
        this.last_code_check = this.ode_code;
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
