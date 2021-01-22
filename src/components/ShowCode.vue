<template>
  <div :id="code_id"></div>
</template>

<script>
import CodeMirror from "codemirror";
import "codemirror/mode/python/python.js";
import { v4 as uuidv4 } from "uuid";

export default {
  name: "ShowCode",
  data: function() {
    return {
      code_id: null
    };
  },
  methods: {},
  mounted: function() {
    this.code_id = "code" + uuidv4(); // wack method, but it works!
    this.$nextTick(() => {
      CodeMirror(document.querySelector("#" + this.code_id), {
        lineNumbers: true,
        mode: "python",
        tabSize: 4,
        indentUnit: 4,
        value: this.code,
        readOnly: true
      });
    });
  },
  props: {
    code: String
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
