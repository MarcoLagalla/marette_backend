import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './plugins'
import vuetify from './plugins/vuetify';
import api from '@/services/api'

Vue.config.productionTip = false

const token = localStorage.getItem('user-token')

if (token) {
  api.defaults.headers.common['Authorization'] = 'Token ' + token
}

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
