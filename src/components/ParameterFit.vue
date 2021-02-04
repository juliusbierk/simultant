<template>
  <span
    class="rightmargin"
    v-if="
      view_in === 'model_section' ||
        (view_in === 'data_section' && type !== 'model')
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

  <span
    v-if="
      view_in !== 'detached_section' &&
        (type === 'detached' ||
          type === 'model-detached' ||
          (type === 'data' && view_in === 'model_section'))
    "
  >
    <span style="font-size:20px; position: relative; top:3px; color: #8aa2ae"
      >&#8620;</span
    >
  </span>

  <span
    v-if="
      (type === 'detached' && view_in === 'data_section') ||
        (type === 'model-detached' && view_in === 'model_section')
    "
  >
    <span style="margin-left:5px">
      <button class="button info defaultcursor rounded">
        {{ detached_parameters[id] }}
      </button>
    </span>
  </span>

  <span v-if="type === 'detached' && view_in === 'model_section'">
    <span style="margin-left:5px">
      <button class="button defaultcursor rounded">
        Mixed data/detached parameter
      </button>
    </span>
  </span>

  <span
    style="margin-left:5px"
    v-if="type === 'data' && view_in === 'model_section'"
  >
    <span
      ><button class="button defaultcursor rounded">
        Data
      </button></span
    >
  </span>

  <span v-if="view_in === 'detached_section'">
    <button
      data-role="hint"
      data-hint-text="This is a detached parameter, which can be shared between models and/or datasets."
      data-hint-hide="0"
      data-cls-hint="bg-lightCyan fg-white"
      class="button info defaultcursor rounded outline "
    >
      {{ name }}
    </button>
  </span>

  <span v-if="is_real_parameter">
    INPUT
  </span>
</template>

<script>
export default {
  name: "ParameterFit",
  data: function() {
    return {};
  },
  computed: {
    parameter_hint_text() {
      if (this.view_in === "model_section") {
        if (this.type === "model") {
          return "All datasets that use this model share this parameter.";
        }
        if (this.type === "data") {
          return "Each dataset that use this model has its own instance of this parameter.";
        }
        if (this.type === "detached") {
          return "This parameter is used in different ways for different datasets.";
        }
        if (this.type === "model-detached") {
          return "All instances of this parameter has been tied to a single detached parameter.";
        }
      }

      if (this.view_in === "data_section") {
        if (this.type === "data") {
          return "This dataset has its own instance of this parameter.";
        }
        if (this.type === "detached") {
          return "The value of this parameter has been tied to a detached parameter.";
        }
      }

      return "ERROR";
    },
    n_detached() {
      return Object.keys(this.detached_parameters).length;
    },
    is_real_parameter() {
      if (this.type === "detached" && this.view_in === "detached_section") {
        return true;
      }
      if (this.type === "data" && this.view_in === "data_section") {
        return true;
      }
      if (this.type === "model" && this.view_in === "model_section") {
        return true;
      }
      return false;
    }
  },
  props: {
    name: String,
    id: String,
    type: String,
    view_in: String,
    detached_parameters: Object
  }
};
</script>

<style scoped>
.rightmargin {
  margin-right: 5px;
}
</style>
