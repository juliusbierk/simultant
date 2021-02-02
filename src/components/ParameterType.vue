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

  <span v-if="tie_to_detached || false">
    <span style="font-size:20px; position: relative; top:3px; color: #8aa2ae"
      >&#8620;</span
    >
  </span>

  <span v-if="false">
    <span style="margin-left:5px">
      <button class="button info defaultcursor rounded">
        asdsadadasdas
      </button>
    </span>

    <span style="margin-left:5px">
      <button class="button defaultcursor">
        Detach
      </button>
    </span>
  </span>

  <span v-if="tie_to_detached">
    <!--    <span-->
    <!--      style="margin-left:5px"-->
    <!--      v-for="(content, id) in parameter_ui.detached_info"-->
    <!--      :key="id"-->
    <!--    >-->
    <!--      <button-->
    <!--        class="button info defaultcursor rounded"-->
    <!--        @click="-->
    <!--          $emit('detach', id);-->
    <!--          tie_to_detached = false;-->
    <!--        "-->
    <!--      >-->
    <!--        {{ content.name }}-->
    <!--      </button>-->
    <!--    </span>-->

    <span style="margin-left:5px">
      <button class="button defaultcursor" @click="tie_to_detached = false">
        Cancel
      </button>
    </span>
  </span>
  <span v-else>
    <span v-if="type === 'model' && view_in === 'model_section'">
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
      <span v-show="n_detached > 0"
        ><button class="button defaultcursor" @click="tie_to_detached = true">
          Tie to Detached
        </button></span
      >
    </span>

    <span v-if="type === 'data'">
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
      <span v-if="view_in === 'data_section'" v-show="n_detached > 0"
        ><button class="button defaultcursor" @click="tie_to_detached = true">
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
  data: function() {
    return {
      tie_to_detached: false
    };
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
      }

      if (this.view_in === "data_section") {
        if (this.type === "data") {
          return "This dataset has its own instance of this parameter.";
        }
      }

      return "ERROR";
    },
    n_detached() {
      return 0;
    }
  },
  props: {
    name: String,
    type: String,
    view_in: String,
  },
  emits: ["tieToData", "tieToModel", "detach"]
};
</script>

<style scoped>
.rightmargin {
  margin-right: 5px;
}
</style>
