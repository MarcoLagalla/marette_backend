import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './plugins'
import vuetify from './plugins/vuetify';
import api from '@/services/api'

Vue.config.productionTip = false

delSessionid()
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

function delSessionid() {
  var user = getCookie("sessionid");
  if (user !== "") {
    document.cookie = "sessionid=; expires=Thu, 01 Jan 1970 00:00:00 UTC; SameSite=Lax ; Secure ; path=/;";
  }
}

function getCookie(cname) {
  var name = cname + "=";
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