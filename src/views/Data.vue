<template>
  <div style="padding:10px" class="grid">
    <div class="row">
      <div class="cell">
        <div class="window" v-bind:class="{ minimized: !create_open }">
          <div class="window-caption">
            <span class="title">Import Data</span>

            <div class="buttons">
              <span
                v-show="create_open"
                @click="create_open = false"
                class="btn-min btn-corner-hover defaultcursor"
              ></span>
              <span
                v-show="!create_open"
                @click="create_open = true"
                class="btn-max btn-corner-hover defaultcursor"
              ></span>
            </div>
          </div>

          <div class="window-content p-2">
            <div class="row flex-justify-center">
              <div v-show="!filename" class="cell-6">
                <input
                  id="file"
                  type="file"
                  data-role="file"
                  data-mode="drop"
                  @change="upload_event"
                />
              </div>
            </div>

            <div v-if="!filename" class="row flex-justify-center">
              <div class="cell-5">
                <small>
                  Files must be in a<code style="margin-bottom:2px">.csv</code
                  >or<code style="margin-bottom:2px">.tsv</code>format.
                  <button
                    @click="show_example = !show_example"
                    style="margin-bottom:2px"
                    class="defaultcursor button mini rounded"
                  >
                    {{ show_example ? "Hide Example" : "Show Example" }}
                  </button>
                </small>
              </div>
            </div>

            <div v-if="filename || show_example" class="row">
              <div class="cell-8 offset-2">
                <small v-show="filename && filenames.length === 1"
                  >{{ filename }}:</small
                >
                <small v-show="filename && filenames.length !== 1"
                  >Processing {{ filenames }}, showing "{{ filename }}":</small
                >
                <table class="table">
                  <thead>
                    <tr>
                      <th
                        v-bind:class="{
                          'bg-lightTime': multiple_x_axes
                            ? i % 2 === 1
                            : i === 1
                        }"
                        v-for="i in header.length"
                        v-bind:key="i"
                        v-html="header[i - 1]"
                      ></th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="i in data.length" v-bind:key="i">
                      <td
                        v-bind:class="{
                          'bg-time': multiple_x_axes ? j % 2 === 1 : j === 1
                        }"
                        v-for="j in data[i - 1].length"
                        v-bind:key="j"
                        v-html="data[i - 1][j - 1]"
                      ></td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <div class="row flex-justify-center" v-if="show_example">
              <div class="cell-5">
                <div class="remark info">
                  Each column should contain a dataset. The first row can be
                  used for naming each dataset.
                  <p></p>
                  Entries can be empty, specifying that a value is unknown at
                  that point.
                  <p></p>
                  Specify one x-axis as the first column<button
                    @click="set_example_data"
                    v-show="interweaving_example"
                    style="margin-bottom:2px"
                    class="defaultcursor button mini rounded"
                  >
                    Show</button
                  >, or several by interweaving x- and y-axes<button
                    @click="set_example_interviewing_data"
                    v-show="!interweaving_example"
                    style="margin-bottom:2px"
                    class="defaultcursor button mini rounded"
                  >
                    Show</button
                  >.
                </div>
              </div>
            </div>

            <div class="row flex-justify-center" v-if="upload_error">
              <div class="cell-5">
                <div class="remark alert">
                  {{ upload_error }}
                </div>
              </div>
            </div>

            <div v-if="filename" class="row">
              <div class="cell-3 offset-2">
                <label class="switch transition-on">
                  <input
                    type="checkbox"
                    data-role="switch"
                    v-model="has_header"
                    data-role-switch="true"
                    class=""
                    @change="upload"
                  /><span class="check"></span>
                  <span class="caption">{{
                    has_header ? "First row is header" : "No header"
                  }}</span>
                </label>
              </div>

              <div class="cell-3">
                <label class="switch transition-on">
                  <input
                    type="checkbox"
                    data-role="switch"
                    v-model="multiple_x_axes"
                    data-role-switch="true"
                    class=""
                  /><span class="check"></span>
                  <span class="caption">{{
                    multiple_x_axes
                      ? "Every second column are x-axes"
                      : "First column is x-axis"
                  }}</span>
                </label>
              </div>

              <div class="cell-3 offset-1">
                <button
                  @click="reset"
                  class="defaultcursor button"
                  style="margin-right:10px"
                >
                  Reset
                </button>

                <button
                  class="defaultcursor button success"
                  style="margin-right:10px"
                  @click="submit_data"
                >
                  Add Data
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row" v-if="db_data && Object.keys(db_data).length">
      <div class="cell">
        <div class="window">
          <div class="window-caption">
            <span class="title">Datasets</span>
          </div>
          <div class="window-content p-2">
            <div class="row">
              <div
                class="cell-6"
                v-for="(content, parent) in db_data"
                v-bind:key="parent"
              >
                <div class="card">
                  <div class="card-header">
                    <div class="row">
                      <div class="cell-6">
                        {{ parent }}
                      </div>

                      <div class="offset-3">
                        <input
                          @click="content.show_plot = !content.show_plot"
                          type="checkbox"
                          data-role="switch"
                          data-caption="Plot"
                        />
                        <span style="margin-right:50px"></span>
                      </div>
                    </div>
                  </div>
                  <div class="card-content p-2">
                    <div v-show="!content.show_plot">
                      <button
                      v-for="p in content"
                      v-bind:key="p.id"
                      style="margin-left:5px; margin-top:3px; margin-bottom:3px"
                      data-role="hint"
                      hintHide="0"
                      :data-hint-text="p.info"
                      data-cls-hint="bg-lightCyan fg-white"
                      class="defaultcursor button secondary small rounded outline"
                    >
                      {{ p.name }}
                    </button>
                    </div>

                    <div v-if="content.show_plot">
                    <BasicPlot
                      :url="this.py + '/plot_data'"
                      :body="content"
                      :dataplot="true"
                    ></BasicPlot>
                    </div>

                  </div>
                  <!--                  <div class="card-footer p-2">-->
                  <!--                  </div>-->
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import BasicPlot from "@/components/BasicPlot.vue";

function get_upload_defaults() {
  return {
    create_open: true,
    header: null,
    data: null,
    filename: null,
    filenames: null,
    multiple_x_axes: false,
    has_header: null,
    show_example: false,
    target_files: null,
    commit_data: false,
    upload_error: null,
    interweaving_example: false
  };
}

export default {
  name: "Data",
  data: function() {
    return {
      py: "http://127.0.0.1:7555",
      db_data: {},
      ...get_upload_defaults()
    };
  },
  components: {
    BasicPlot
  },
  methods: {
    set_example_data() {
      this.header = ["x", "y_1", "y_2", "y_3"];
      this.data = [
        ["0", "1.3", "1.1", "1.5"],
        ["1", "2.1", "2.5", "2.3"],
        ["2", "3.3", "3.1", "3.1"],
        ["3", "4.4", "", "4.8"],
        ["4", "5.5", "", "6.1"]
      ];
      this.multiple_x_axes = false;
      this.interweaving_example = false;
    },
    set_example_interviewing_data() {
      this.header = ["x_1", "y_1", "x_2", "y_2"];
      this.data = [
        ["0", "1.3", "0", "1.5"],
        ["1", "2.1", "1", "2.3"],
        ["2", "3.3", "2", "3.1"],
        ["3", "3.3", "", ""],
        ["4", "3.3", "", ""]
      ];
      this.multiple_x_axes = true;
      this.interweaving_example = true;
    },
    submit_data() {
      this.commit_data = true;
      this.upload();
    },
    upload_event(e) {
      this.target_files = e.target.files;
      this.upload();
    },
    reset() {
      let sure_reset = confirm("Are you sure?");
      if (!sure_reset) {
        return;
      }
      this.do_reset();
    },
    do_reset() {
      Object.assign(this.$data, get_upload_defaults());
      this.set_example_data();
    },
    upload() {
      this.show_example = false;
      const files = this.target_files;
      if (files) {
        // For now just do one file:
        const formData = new FormData();
        for (const file of files) {
          formData.append("file_" + file.name, file);
        }

        formData.append("has_header", this.has_header);
        formData.append("commit_data", this.commit_data);
        formData.append("multiple_x_axes", this.multiple_x_axes);

        this.upload_error = null;

        fetch(this.py + "/upload_data", {
          method: "POST",
          body: formData
        })
          .then(async result => {
            const data = await result.json();
            if (this.commit_data) {
              if (data.success) {
                this.do_reset();
                this.update_datasets();
              } else {
                this.commit_data = false;
                this.upload_error = "Data could not be processed.";
                if (
                  typeof data.error === "string" ||
                  data.error instanceof String
                ) {
                  this.upload_error += " " + data.error;
                }
              }
            } else {
              this.header = data.example.header;
              this.data = data.example.data;
              this.has_header = data.example.has_header;
              this.filename = data.example.fname;
              this.filenames = data.filenames;
            }
          })
          .catch(() => {
            this.upload_error =
              "Could not process file. Please double check that it is a valid .csv or .tsv file.";
          });
      }
    },
    update_datasets() {
      fetch(this.py + "/data_list", {}).then(async result => {
        const res = await result.json();

        for (const name of Object.keys(res)) {
          if (this.db_data[name]) {
            res[name].show_plot = this.db_data[name].show_plot;
          } else {
            res[name].show_plot = false;
          }
        }
        this.db_data = res;
      });
    }
  },
  mounted: function() {
    this.set_example_data();
    this.update_datasets();
  }
};
</script>

<style>
.files {
  display: none;
}

.bg-lightTime {
  background-color: #f7f5f2 !important;
}

.bg-time {
  background-color: #f5f1eb !important;
}

.bg-darkTime {
  background-color: #f0e9df !important;
}

.btn-corner-hover:hover {
  background-color: #7f8ca1;
}
</style>
