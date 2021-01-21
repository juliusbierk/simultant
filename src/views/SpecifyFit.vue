<template>
  <div style="padding:10px" class="grid">
    <div class="row">
      <div class="cell">
        <div class="window" v-bind:class="{ minimized: !choose_fit_open }">
          <div class="window-caption">
            <span class="title">Fits</span>

            <div class="buttons">
              <span
                v-show="choose_fit_open"
                @click="choose_fit_open = false"
                class="btn-min btn-corner-hover defaultcursor"
              ></span>
              <span
                v-show="!choose_fit_open"
                @click="choose_fit_open = true"
                class="btn-max btn-corner-hover defaultcursor"
              ></span>
            </div>
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

          <div style="min-height: 500px;" class="window-content p-2">
            <div class="row">
              <div class="cell-6 offset-1">
                <label for="group_select"><small>Data Group</small></label>
                <select id="group_select" data-role="select">
                  <option value="mini">Mini</option>
                  <option value="site">Site</option>
                  <option value="portal">Portal</option>
                </select>
              </div>
              <div class="cell-3">
                <div class="row flex-justify-center">
                  <button
                    style="position: relative; top:22px"
                    class="button primary defaultcursor"
                  >
                    Add to Fit
                  </button>
                </div>
              </div>
            </div>

            <div class="row">
              <div class="cell-9 offset-1">
                <label for="dataset_select"><small>Datasets</small></label>
                <select id="dataset_select" data-role="select" multiple>
                  <option value="1" selected>Amazon</option>
                  <option value="2" selected>Apple</option>
                  <option value="3" selected>Blogger</option>
                  <option value="4" selected>Evernote</option>
                  <option value="5" selected>GitHub</option>
                </select>
              </div>
            </div>

            <div class="row">
              asdasd
            </div>
          </div>
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
      py: "http://127.0.0.1:7555",
      choose_fit_open: true
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
