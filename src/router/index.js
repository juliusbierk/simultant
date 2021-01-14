import {
  createRouter,
  createWebHistory,
  createWebHashHistory
} from "vue-router";
import Home from "../views/Home.vue";
import Models from "../views/Models.vue";
import Data from "../views/Data.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home
  },
  {
    path: "/models",
    name: "Models",
    component: Models
  },
  {
    path: "/data",
    name: "Data",
    component: Data

    // Alternative (lazy) method:
    // // route level code-splitting
    // // this generates a separate chunk (about.[hash].js) for this route
    // // which is lazy-loaded when the route is visited.
    // component: () =>
    //   import(/* webpackChunkName: "about" */ "../views/About.vue")
  }
];

const router = createRouter({
  history: process.env.IS_ELECTRON
    ? createWebHashHistory()
    : createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
