<template>
  <div :id="plot_id"></div>
</template>

<script>
import Plotly from "plotly.js-dist";
import plotlysettings from "@/plotsettings.js";
import _ from "lodash";
import misc from "@/misc.js";

export default {
  name: "BasicPlot",
  data: function() {
    return {
      xlim: [0, 5],
      ylim: null,
      plot_id: null
    };
  },
  methods: {
    update_body(body) {
      return { content: body, xlim: this.xlim, ylim: this.ylim };
    },
    update_ylim(res) {
      if (!this.ylim) {
        let ylim = [Math.min.apply(null, res.y), Math.max.apply(null, res.y)];
        var dy = ylim[1] - ylim[0];
        ylim[0] = ylim[0] - 0.015 * dy;
        ylim[1] = ylim[1] + 0.015 * dy;
        this.ylim = ylim;
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

        let layout = {
          ...plotlysettings.layout
        };

        if (!this.dataplot) {
          layout.xaxis.range = this.xlim;
          if (this.ylim) {
            layout.yaxis.range = this.ylim;
          }
        }
        Plotly.newPlot(
          this.plot_id,
          this.dataplot ? res : [res],
          layout,
          plotlysettings.settings
        );

        if (!this.dataplot) {
          var plot = document.getElementById(this.plot_id);
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
        }
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

        let layout = {
          ...plotlysettings.layout
        };
        layout.xaxis.range = this.xlim;
        if (this.ylim) {
          layout.yaxis.range = this.ylim;
        }

        Plotly.react(this.plot_id, this.dataplot ? res : [res], layout);
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
    this.plot_id = "plot" + misc.uuid4(); // wack method, but it works!
    this.$nextTick(() => {
      this.update();
    });
  },
  props: {
    url: String,
    body: Object,
    dataplot: Boolean
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
