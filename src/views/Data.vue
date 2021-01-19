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
            <div v-show="!file_chosen" class="row flex-justify-center">
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

            <div class="row">
              <div class="cell-8 offset-2">
                <b>{{ filename }}:</b>
                <table class="table">
                  <thead>
                    <tr>
                      <th v-for="s in header" v-bind:key="s" v-html="s"></th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="i in data.length" v-bind:key="i">
                      <td
                        v-for="j in data[i - 1].length"
                        v-bind:key="j"
                        v-html="data[i-1][j-1]"
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
      file_chosen: false,
      header: ["x", "y_1", "y_2", "y_3"],
      data: [
        ["0", "1.3", "1.1", "1.5"],
        ["1", "2.1", "2.5", "2.3"],
        ["2", "3.3", "3.6", "3.1"]
      ],
        filename: "Example data"
    };
  },
  methods: {
    upload(e) {
      var files = e.target.files;
      if (files) {
        // this.file_chosen = true;

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
</style>
