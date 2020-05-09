import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './plugins'
import vuetify from './plugins/vuetify';
import api from '@/services/api'

Vue.config.productionTip = false

var token = getToken();
var id = getID();

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


function getID() {
 var result = document.cookie.match(new RegExp('user_private' + '=([^;]+)'));
 result && (result = JSON.parse(result[1]));
 return result ? result.id : '';
}

function getToken() {
 var result = document.cookie.match(new RegExp('user-token' + '=([^;]+)'));
 result && (result = result[1]);
 return result ? result : '';
}