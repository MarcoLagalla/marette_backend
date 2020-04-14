import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './plugins'
import vuetify from './plugins/vuetify';
import api from '@/services/api'

Vue.config.productionTip = false
var token = getCookie("user-token");
var id = getCookie("user-id");
if (token && id) { //voglio caricarli solo se li ho entrambi
  api.defaults.headers.common['Authorization'] = 'Token ' + token;
  store.dispatch("userProfile/getUserData", id);
}

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')

function getCookie(name) {
  name = name + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}