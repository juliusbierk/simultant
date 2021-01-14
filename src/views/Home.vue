<template>
  <div style="padding:10px" class="grid">
    <div class="row">
      <div class="cell">
        <div class="window">
          <div class="window-caption">
            <!--            <span class="icon mif-windows"></span>-->
            <span class="title">Existing Models</span>
          </div>
          <div class="window-content p-2">
            Window content
          </div>
        </div>
      </div>

      <div class="cell">
        <div class="window">
          <div class="window-caption">
            <!--            <span class="icon mif-windows"></span>-->
            <span class="title">Create New Model</span>
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

            <p></p>

            <div id="code"></div>
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

export default {
  name: "Home",
  data: function() {
    return {
      name: "New Model",
      expr_mode: true,
      code: "def New_Model(x, a, b):\n    return a + b * x\n",
      ode_code: "def New_Model(x, y, a, b):\n    return a * y[1], -b * y[0]\n",
      cmcode: null,
      marker: null
    };
  },
  computed: {
    name_underscore: function() {
      return this.name.replaceAll(" ", "_");
    }
  },
  components: {
    // HelloWorld
  },
  methods: {
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

    // For some reason assigning CodeMirror to vue data breaks codemirror, so we assign to window:
    window.cmcode = CodeMirror(document.querySelector("#code"), {
      lineNumbers: true,
      mode: "python",
      tabSize: 4,
      indentUnit: 4,
      value: this.expr_mode ? this.code : this.ode_code,
      extraKeys: { Tab: betterTab }
    });

    this.marker = window.cmcode.markText(
      { line: 0, ch: 0 },
      { line: 0, ch: 16 },
      { readOnly: true }
    );
    window.cmcode.on("change", cm => {
      if (this.expr_mode) {
        this.code = cm.getValue();
      } else {
        this.ode_code = cm.getValue();
      }
    });

    window.cmcode.on("paste", (cm, t) => {
      console.log("We are not handling pasting very well yet.");
    });
  }
};
</script>

<style></style>
