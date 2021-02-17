<template>
  <div style="margin:10px"></div>

  <div class="row">
    <div class="cell-5 offset-1">
      <h1>Simultant</h1>
      <h2>: Simultaneous Curve Fitting</h2>
    </div>
  </div>

  <div v-if="!$store.state.backend_running">
    <div class="row flex-justify-center">
      <div data-role="activity" data-type="cycle" data-style="color"></div>
    </div>

    <div class="row flex-justify-center">
      Starting backend
    </div>
  </div>
  <div v-else>
    <div class="row">
      <div class="cell-4 offset-1">
        <div class="remark secondary">
          <h3>Models</h3>
          Define your mathematical functions for fitting using standard Python
          code. Function can be defined directly as expressions or indirectly as
          ordinary differential equation to be solved. All code will be
          automatically differentiated to enable fast fitting.
        </div>
      </div>

      <div class="cell-4 offset-1">
        <div class="remark secondary">
          <h3>Data</h3>
          Import data as comma-separated or tab-separated data.
          Data will be grouped by your file uploads, or can be grouped by specifying
          dataset names.
        </div>
      </div>
    </div>

    <div class="row">
      <div class="cell-4 offset-1">
        <div class="remark secondary">
          <h3>Fit Topology</h3>
          Specify a fit by applying models models datasets.
          Parameters can be shared between all datasets, be specific to each datasets,
          or shared in any manner across datasets and/or models.
        </div>
      </div>

      <div class="cell-4 offset-1">
        <div class="remark secondary">
          <h3>Run Fit</h3>
          Specify good initial guesses for fit parameters and run fit.
          Make sure you mark which parameters are constants and should not
          be fitted.
        </div>
      </div>
    </div>

    <div class="row">
      <div class="cell-9 offset-1">
        <div class="remark warning">
          Please cite <em>xxx</em> if using results produced by this application in a publication.
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import store from "@/store";
import config from "@/config.js";

export default {
  store,
  methods: {
    check_backend() {
      fetch(config.py + "/", {
        method: "GET"
      }).then(async result => {
        const r = await result.json();
        if (r["running"]) {
          this.$store.commit("set_backend_running");
        }
      });
    },
    check_backend_loop() {
      if (!this.$store.state.backend_running) {
        this.check_backend();
        setTimeout(this.check_backend_loop, 100);
      }
    }
  },
  mounted() {
    this.check_backend_loop();
  }
};
</script>

<style scoped>
h1,
h2 {
  display: inline-block;
}
</style>
