<template>
  <span v-if="view_in === 'model_section'">
    <span class="rightmargin"
      ><button
        data-role="hint"
        :data-hint-text="parameter_hint_text"
        data-hint-hide="0"
        data-cls-hint="bg-lightCyan fg-white"
        class="button info large defaultcursor rounded outline "
      >
        {{ name }}
      </button></span
    >

    <span v-if="type === 'global'">
      <span
        ><button class="button info defaultcursor">Tied to Model</button></span
      >
      <span
        ><button class="button defaultcursor" @click="$emit('tieToData')">
          Tie to Data
        </button></span
      >
      <span><button class="button defaultcursor">Detach</button></span>
    </span>

    <span v-if="type === 'local'">
      <span><button class="button defaultcursor">Tie to Model</button></span>
      <span
        ><button class="button info defaultcursor">
          Tied to Data
        </button></span
      >
    </span>
  </span>
</template>

<script>
export default {
  name: "ParameterType",
  computed: {
    parameter_hint_text() {
      if (this.type === "global") {
        return "All datasets that use this model share this parameter.";
      }
      if (this.type === "local") {
        return "Each dataset that use this model has its own instance of this parameter.";
      }
      return "ERROR";
    }
  },
  props: {
    name: String,
    type: String,
    id: String,
    view_in: String
  },
  emits: ["tieToData"]
};
</script>

<style scoped>
.rightmargin {
  margin-right: 5px;
}
</style>
