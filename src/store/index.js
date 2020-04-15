import Vue from 'vue'
import Vuex from 'vuex'

import userAuthentication from './modules/userAuthentication'
import userProfile from "./modules/userProfile"
import restaurant from "./modules/restaurant";

Vue.use(Vuex)

export default new Vuex.Store({

  modules: {
    userProfile,
    userAuthentication,
    restaurant
  },

  /*state: {
    articles: require('@/data/articles.json'),
    drawer: false,
    items: [
      {
        text: 'Home',
        to: '/'
      },

      {
        text:'SIGN UP',
        to: '/register'
      }
    ]
  },
  getters: {
    categories: state => {
      const categories = []

      for (const article of state.articles) {
        if (
          !article.category ||
          categories.find(category => category.text === article.category)
        ) continue

        const text = article.category

        categories.push({
          text,
          to: `/category/${text}`
        })
      }

      return categories.sort().slice(0, 4)
    },
    links: (state, getters) => {
      return state.items.concat(getters.categories)
    }
  },
  mutations: {
    setDrawer: (state, payload) => (state.drawer = payload),
    toggleDrawer: state => (state.drawer = !state.drawer)
  },
  actions: {

  }*/
})
