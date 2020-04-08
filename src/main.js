import Vue from 'vue'
import App from '@/App.vue'

import store from '@/store' 
import router from '@/router'
import api from '@/services/api'

const token = localStorage.getItem('user-token')

if (token) {
  api.defaults.headers.common['Authorization'] = 'Token ' + token
}

new Vue({
    el: '#app',
    store,
    router,
    components: { App },
    template: '<App/>',
    render: h => h(App)
})

