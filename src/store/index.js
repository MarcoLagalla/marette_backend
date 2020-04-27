import Vue from 'vue'
import Vuex from 'vuex'

import userAuthentication from './modules/userAuthentication'
import userProfile from "./modules/userProfile"
import restaurants from "./modules/restaurants";
import restaurantData from "./modules/restaurantData";

Vue.use(Vuex)

export default new Vuex.Store({

  modules: {
    userProfile,
    userAuthentication,
    restaurants,
    restaurantData,
  },

})
