<template>
  <div style="padding:10px" class="grid">
    <div class="row">
      <div class="cell">
        <div class="window" v-bind:class="{ minimized: !create_open }">
          <div class="window-caption">
            <!--            <span class="icon mif-windows"></span>-->
            <span class="title">Upload New Data</span>

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
                    v-if="!show_example"
                    @click="show_example = true"
                    style="margin-bottom:2px"
                    class="defaultcursor button mini rounded"
                  >
                    Show Example
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

            <div class="row flex-justify-center" v-if="upload_error">
              <div class="cell-5">
                <div class="remark alert">
                  {{ upload_error }}
                </div>
              </div>
            </div>

            <div v-if="filename" class="row">
              <div class="cell-4 offset-3">
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
  </div>
</template>

<script>
export default {
  name: "Data",
  data: function() {
    return {
      py: "http://127.0.0.1:7555",
      create_open: true,
      header: ["x", "y_1", "y_2", "y_3"],
      data: [
        ["0", "1.3", "1.1", "1.5"],
        ["1", "2.1", "2.5", "2.3"],
        ["2", "3.3", "3.6", "3.1"]
      ],
      filename: null,
      filenames: null,
      multiple_x_axes: false,
      has_header: null,
      show_example: false,
      target_files: null,
      commit_data: false,
      upload_error: null
    };
  },
  methods: {
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
      this.$router.go();
    },
    upload() {
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
                this.$router.go();
              } else {
                this.upload_error =
                  "Data could not be processed. Please check that it is fully numerical.";
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
    }
  },
  mounted: function() {}
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
