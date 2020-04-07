import Vue from 'vue'
import Vuex from 'vuex'
import userAutentication from './modules/userAutentication'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    userAutentication

  }
})