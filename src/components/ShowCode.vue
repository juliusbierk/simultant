<template>
  <div :id="code_id"></div>
</template>

<script>
import CodeMirror from "codemirror";
import "codemirror/mode/python/python.js";

export default {
  name: "ShowCode",
  data: function() {
    return {
      code_id: null
    };
  },
  methods: {
    uuidv4() {
      return "Axxxxxxxxxxxx4xxxyxxxxxxxxxxxxxxx".replace(/[xy]/g, function(c) {
        var r = (Math.random() * 16) | 0,
          v = c == "x" ? r : (r & 0x3) | 0x8;
        return v.toString(16);
      });
    }
  },
  mounted: function() {
    this.code_id = this.uuidv4(); // wack method, but it works!
    setTimeout(() => {
      CodeMirror(document.querySelector("#" + this.code_id), {
        lineNumbers: true,
        mode: "python",
        tabSize: 4,
        indentUnit: 4,
        value: this.code,
        readOnly: true
      });
    }, 5);
  },
  props: {
    code: String
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
