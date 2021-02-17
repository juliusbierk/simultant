<template>
  <div style="margin:50px"></div>

  <div v-if="!$store.state.backend_running">
    <div class="row flex-justify-center">
      <div data-role="activity" data-type="cycle" data-style="color"></div>
    </div>

    <div class="row flex-justify-center">
      Starting backend
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
      this.check_backend();
      if (!this.$store.state.backend_running) {
        setTimeout(this.check_backend_loop, 100);
      }
    }
  },
  mounted() {
    this.check_backend_loop();
  }
};
</script>
