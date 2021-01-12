import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import Metro from "metro4";

createApp(App, {
    mounted: function () {
        Metro.init();
    }
    })
  .use(store)
  .use(router)
  .mount("#app");
