<template>
  <div id="plot"></div>
</template>

<script>
import Plotly from "plotly.js-dist";
import plotlysettings from "@/plotsettings.js";
import _ from "lodash";

export default {
  name: "BasicPlot",
  data: function() {
    return {
      xlim: [0, 5],
      ylim: null
    };
  },
  methods: {
    update_body(body) {
      let nbody = {
        ...body
      };
      nbody.xlim = this.xlim;
      nbody.ylim = this.ylim;
      return nbody;
    },
    update_ylim(res) {
      if (!this.ylim) {
        this.ylim = [Math.min.apply(null, res.y), Math.max.apply(null, res.y)];
      }
    },
    update() {
      fetch(this.url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(this.update_body(this.body))
      }).then(async result => {
        var res = await result.json();
        this.update_ylim(res);
        res.mode = "lines";

        let layout = {
          ...plotlysettings.layout
        };
        layout.xaxis.range = this.xlim;
        if (this.ylim) {
          layout.yaxis.range = this.ylim;
        }

        Plotly.newPlot("plot", [res], layout, plotlysettings.settings);

        var plot = document.getElementById("plot");
        plot.on("plotly_relayout", e => {
          let update = false;

          if (e["xaxis.range[0]"]) {
            this.xlim = [e["xaxis.range[0]"], e["xaxis.range[1]"]];
            update = true;
          }
          if (e["yaxis.range[0]"]) {
            this.ylim = [e["yaxis.range[0]"], e["yaxis.range[1]"]];
            update = true;
          }

          if (update) {
            this.debounced_react();
          }
        });
      });
    },
    react() {
      fetch(this.url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(this.update_body(this.body))
      }).then(async result => {
        var res = await result.json();
        this.update_ylim(res);
        res.mode = "lines";

        let layout = {
          ...plotlysettings.layout
        };
        layout.xaxis.range = this.xlim;
        if (this.ylim) {
          layout.yaxis.range = this.ylim;
        }

        Plotly.react("plot", [res], layout);
      });
    },
    reset_scale() {
      this.xlim = [0, 5];
      this.ylim = null;
    }
  },
  created() {
    this.debounced_react = _.debounce(() => {
      this.react();
    }, 250);
  },
  watch: {
    body: function() {
      this.update();
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
