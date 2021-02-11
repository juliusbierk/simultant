<template>
  <div class="row">
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

    <span v-if="is_real_parameter">
      <input
        type="checkbox"
        data-role="switch"
        class="defaultcursor"
        :checked="!is_const"
        @change="update_prepend"
        data-cls-switch="blueSwitch"
        data-cls-check="blueSwitch"
      />
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

    <span v-if="view_in === 'detached_section'" class="rightmargin">
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
      <form data-role="validator" data-interactive-check="true">
        <input
          :id="input_id"
          type="text"
          :value="initial_value"
          @change="$emit('initialValueChange', $event.target.value)"
          data-role="input"
          :data-prepend="prepend_text"
          data-clear-button="false"
          data-validate="number"
        />

        <span class="invalid_feedback">
          Not a valid initial condition.
        </span>
      </form>
    </span>

    <span v-if="is_real_parameter && fit" style="margin-left:5px">
      <input
        type="text"
        data-role="input"
        data-prepend="Fit:"
        data-clear-button="false"
        :value="fit.toPrecision(precision)"
        readonly
        style="background-color: #e1ebf2;"
      />
    </span>
  </div>
</template>

<script>
import { v4 as uuidv4 } from "uuid";

export default {
  name: "ParameterFit",
  data: function() {
    return {
      precision: 5,
      prepend_const: "Constant value:",
      prepend_fit: "Fit initial guess:",
      input_id: "a_" + uuidv4().replace(/-/g, "")
    };
  },
  methods: {
    update_prepend() {
      this.$emit("changeValueType");
      this.$nextTick(() => {
        // m4q manipulation:
        window
          .$("#" + this.input_id)
          .siblings()
          .filter(".prepend")
          .html(this.prepend_text);
      });
    }
  },
  computed: {
    prepend_text() {
      return this.is_const ? this.prepend_const : this.prepend_fit;
    },
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
    detached_parameters: Object,
    initial_value: Number,
    fit: Number,
    is_const: Boolean
  },
  emits: ["initialValueChange", "changeValueType"]
};
</script>

<style>
.rightmargin {
  margin-right: 5px;
}

.blueSwitch .check {
  border: 2px #d9e6f2 solid !important;
  cursor: default !important;
}

.blueSwitch .check::after {
  background: #5ebdec !important;
  cursor: default !important;
  border: 2px #d9e6f2 solid;
}
.blueSwitch input[type="checkbox"]:checked ~ .check {
  background: #5ebdec !important;
  cursor: default !important;
}
.blueSwitch input[type="checkbox"]:checked ~ .check::after {
  border-color: #ffffff !important;
  background: #ffffff !important;
  cursor: default !important;
}
</style>
