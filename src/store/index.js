import Vue from 'vue'
import Vuex from 'vuex'

import userAuthentication from './modules/userAuthentication'
import userProfile from "./modules/userProfile"
import restaurants from "./modules/restaurants";

Vue.use(Vuex)

export default new Vuex.Store({

  modules: {
    userProfile,
    userAuthentication,
    restaurants
  },

})
