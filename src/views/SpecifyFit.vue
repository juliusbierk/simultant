<template>
  <div style="padding:10px" class="grid"></div>
</template>

<script>
import BasicPlot from "@/components/BasicPlot.vue";

export default {
  name: "Data",
  data: function() {
    return {
      py: "http://127.0.0.1:7555"
    };
  },
  components: {
    BasicPlot
  },
  methods: {},
  mounted: function() {}
};
</script>

<style>
.btn-corner-hover:hover {
  background-color: #7f8ca1;
}
</style>
