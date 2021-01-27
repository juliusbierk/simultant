<template>
  <span
    class="rightmargin"
    v-if="
      view_in === 'model_section' ||
        (view_in === 'data_section' && type !== 'global')
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

  <span v-if="tie_to_detached || is_tied_to_whom[0]">
    <span style="font-size:20px; position: relative; top:3px; color: #8aa2ae"
      >&#8620;</span
    >
  </span>

  <span v-if="is_tied_to_whom[0]">
    <span style="margin-left:5px">
      <button class="button info defaultcursor rounded">
        {{ parameter_ui.detached_info[is_tied_to_whom[1]].name }}
      </button>
    </span>

    <span style="margin-left:5px">
      <button class="button defaultcursor">
        Detach
      </button>
    </span>
  </span>

  <span v-if="tie_to_detached">
    <span
      style="margin-left:5px"
      v-for="(content, id) in parameter_ui.detached_info"
      :key="id"
    >
      <button
        class="button info defaultcursor rounded"
        @click="
          $emit('detach', id);
          tie_to_detached = false;
        "
      >
        {{ content.name }}
      </button>
    </span>

    <span style="margin-left:5px">
      <button class="button defaultcursor" @click="tie_to_detached = false">
        Cancel
      </button>
    </span>
  </span>
  <span v-else>
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
      <span v-show="n_detached > 0"
        ><button class="button defaultcursor" @click="tie_to_detached = true">
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
    },
    n_detached() {
      return Object.keys(this.parameter_ui.detached_info).length;
    },
    is_tied_to_whom() {
      let pars;
      if (!(this.type === "global" || this.type === "local")) {
        if (this.view_in === "model_section") {
          pars = this.parameter_ui.model_to_parameters[
            [this.model_or_data_id, this.name]
          ];
          if (pars && pars.length === 1) {
            return [true, pars[0]];
          }
        } else {
          return [
            true,
            this.parameter_ui.data_to_parameters[
              [this.model_or_data_id, this.name]
            ]
          ];
        }
      }
      return [false, null];
    }
  },
  props: {
    name: String,
    type: String,
    id: String,
    view_in: String,
    parameter_ui: Object,
    model_or_data_id: String
  },
  emits: ["tieToData", "tieToModel", "detach"]
};
</script>

<style scoped>
.rightmargin {
  margin-right: 5px;
}
</style>
