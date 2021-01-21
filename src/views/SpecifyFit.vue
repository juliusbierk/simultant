<template>
  <div style="padding:10px" class="grid">
    <div class="row">
      <div class="cell">
        <div class="window">
          <div class="window-caption">
            <span class="title">Fits</span>
          </div>

          <div class="window-content p-2"></div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="cell">
        <div class="window">
          <div class="window-caption">
            <!--            <span class="icon mif-windows"></span>-->
            <span class="title">Data</span>
          </div>

          <div class="window-content p-2"></div>
        </div>
      </div>
      <div class="cell">
        <div class="window">
          <div class="window-caption">
            <!--            <span class="icon mif-windows"></span>-->
            <span class="title">Models &amp; Parameters</span>
          </div>

          <div class="window-content p-2"></div>
        </div>
      </div>
    </div>
  </div>
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
