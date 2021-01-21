<template>
  <div style="padding:10px" class="grid">
    <div class="row" v-if="!Object.keys(db_data).length">
      <div class="cell-6 offset-3">
        <div class="remark alert">
          No data has been imported.
        </div>
      </div>
    </div>

    <div class="row" v-if="Object.keys(db_data).length">
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

    <div class="row" v-if="Object.keys(db_data).length">
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
                <select
                  id="group_select"
                  data-role="select"
                  @change="update_selection_datasets"
                >
                  <option style="display:none" disabled selected value></option>
                  <option
                    v-for="(content, parent) in db_data"
                    :value="parent"
                    v-bind:key="parent"
                  >
                    {{ parent }}</option
                  >
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
              <div
                class="cell-9 offset-1"
                v-if="selected_data_group"
                :key="selected_data_group"
              >
                <label for="dataset_select"><small>Datasets</small></label>
                <select
                  id="dataset_select"
                  data-role="select"
                  v-model="selected_dataset_ids"
                  multiple
                >
                  <option
                    v-for="content in db_data[selected_data_group]"
                    v-bind:key="content.id"
                    :value="content.id"
                    >{{ content.name }}</option
                  >
                  >
                </select>
              </div>
            </div>

            <div class="card"></div>

            <div class="row">
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
      choose_fit_open: true,
      db_data: {},
      selected_data_group: null,
      selected_dataset_ids: null
    };
  },
  components: {
    BasicPlot
  },
  methods: {
    update_datasets() {
      fetch(this.py + "/data_list", {}).then(async result => {
        this.db_data = await result.json();
      });
    },
    update_selection_datasets(e) {
      if (e.target.value) {
        this.selected_dataset_ids = [];
        for (const x of this.db_data[e.target.value]) {
          this.selected_dataset_ids.push(x.id);
        }
        this.selected_data_group = e.target.value;
      }
    }
  },
  mounted: function() {
    this.update_datasets();
  }
};
</script>

<style>
.btn-corner-hover:hover {
  background-color: #7f8ca1;
}

li.disabled {
  display: none !important;
}
</style>
