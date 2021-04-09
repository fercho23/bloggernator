
import Vue from "vue"
import App from "./App.vue"
import router from "./router"

Vue.config.productionTip = false

import BootstrapVue from "bootstrap-vue";
// import VeeValidate from "vee-validate";

Vue.use(BootstrapVue);
// Vue.use(VeeValidate);

import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

import { library } from "@fortawesome/fontawesome-svg-core"
import { faFontAwesome } from "@fortawesome/free-brands-svg-icons"
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome"
import { fas } from "@fortawesome/free-solid-svg-icons";
Vue.component("font-awesome-icon", FontAwesomeIcon)

library.add(fas);
library.add(faFontAwesome)

new Vue({
  router,
  render: h => h(App),
}).$mount("#app")

