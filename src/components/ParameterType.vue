<template>
  <span
    class="rightmargin"
    v-if="
      view_in === 'model_section' ||
        (view_in === 'data_section' && type === 'local')
    "
  >
    <button
      data-role="hint"
      :data-hint-text="parameter_hint_text"
      data-hint-hide="0"
      data-cls-hint="bg-lightCyan fg-white"
      class="button info defaultcursor rounded outline "
    >
      {{ name }}
    </button>
  </span>

  <span>
    <span v-if="type === 'global' && view_in === 'model_section'">
      <span
        ><button class="button info defaultcursor">
          Model Parameter
        </button></span
      >
      <span
        ><button class="button defaultcursor" @click="$emit('tieToData')">
          Tie to Data
        </button></span
      >
      <span
        ><button class="button defaultcursor" @click="$emit('detach')">
          Tie to Detached
        </button></span
      >
    </span>

    <span v-if="type === 'local'">
      <span
        ><button class="button defaultcursor" @click="$emit('tieToModel')">
          Tie to Model
        </button></span
      >
      <span
        ><button class="button info defaultcursor">
          Data Parameter
        </button></span
      >
      <span v-if="view_in === 'data_section'"
        ><button class="button defaultcursor" @click="$emit('detach')">
          Tie to Detached
        </button></span
      >
    </span>
  </span>

  <span v-if="view_in === 'data_section'"> </span>
</template>

<script>
export default {
  name: "ParameterType",
  computed: {
    parameter_hint_text() {
      if (this.view_in === "model_section") {
        if (this.type === "global") {
          return "All datasets that use this model share this parameter.";
        }
        if (this.type === "local") {
          return "Each dataset that use this model has its own instance of this parameter.";
        }
      }

      if (this.view_in === "data_section") {
        if (this.type === "local") {
          return "This dataset has its own instance of this parameter.";
        }
      }

      return "ERROR";
    }
  },
  props: {
    name: String,
    type: String,
    id: String,
    view_in: String,
    detached_info: Object
  },
  emits: ["tieToData", "tieToModel", "detach"]
};
</script>

<style scoped>
.rightmargin {
  margin-right: 5px;
}
</style>
