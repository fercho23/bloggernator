
import Vue from "vue";
import Router from "vue-router";

Vue.use(Router);

export default new Router({
  mode: "history",
  routes: [
    {
      path: "/",
      name: "home",
      component: () => import("./components/Home.vue"),
    },
    {
      path: "/post/list",
      name: "post-list",
      component: () => import("./components/Posts/PostList.vue"),
    },
    {
      path: "/post/:uuid",
      name: "post-details",
      component: () => import("./components/Posts/PostDetail.vue"),
    },
  ]
});