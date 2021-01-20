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
                class="btn-min defaultcursor"
              ></span>
              <span
                v-show="!create_open"
                @click="create_open = true"
                class="btn-max defaultcursor"
              ></span>
            </div>
          </div>
          <div class="window-content p-2">

            <div class="row flex-justify-center">
              <div class="cell-6">
                <input
                  id="file"
                  type="file"
                  data-role="file"
                  data-mode="drop"
                  @change="upload"
                />
              </div>
            </div>

            <div v-if="!filename" class="row flex-justify-center">
              <div class="cell-5">
                Files must be in a .csv or .tsv format
                <button v-if="!show_example" @click="show_example = true;" style="margin-bottom:2px" class="defaultcursor button mini rounded">Show Example</button>
              </div>
            </div>

            <div v-if="filename" class="row">
              <div class="cell-6 offset-3">
                <label class="switch transition-on">
                  <input
                    type="checkbox"
                    data-role="switch"
                    v-model="has_header"
                    data-role-switch="true"
                    class=""
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
            </div>

            <div v-if="filename || show_example" class="row">
              <div class="cell-8 offset-2">
                <b v-show="filename">{{ filename }}:</b>
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
      multiple_x_axes: false,
        has_header: true,
        show_example: false,
    };
  },
  methods: {
    upload(e) {
      var files = e.target.files;
      if (files) {
        // For now just do one file:
        const formData = new FormData();
        for (const file of files) {
          formData.append(file.name, file);
        }

        fetch(this.py + "/upload_data", {
          method: "POST",
          body: formData
        })
          .then(async result => {
            const data = await result.json();
            this.header = data.example.header;
            this.data = data.example.data;
            this.filename = data.example.fname;
          })
          .catch(() => {
            alert("Could not process file. Are you sure this is a csv file?");
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
</style>
