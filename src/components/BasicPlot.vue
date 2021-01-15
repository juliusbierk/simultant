<template>
  <div id="plot"></div>
</template>

<script>
import Plotly from "plotly.js-dist";
import plotlysettings from "@/plotsettings.js";
import _ from "lodash";

export default {
  name: "BasicPlot",
  methods: {
    update() {
      fetch(this.url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(this.body)
      }).then(async result => {
        var res = await result.json();
        res.mode = "lines";
        Plotly.newPlot(
          "plot",
          [res],
          plotlysettings.layout,
          plotlysettings.settings
        );
      });
    },
  },
    created() {
      this.debounced_update = _.debounce(() => {this.update()}, 1000);
    },
  watch: {
    body: function() {
      this.debounced_update();
    }
  },
  mounted: function() {
    this.update();
  },
  props: {
    url: String,
    body: Object
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
