import Vue from 'vue'
import Router from 'vue-router'
import Registration from "./components/Registration";
import PageContentHome from "./components/PageContentHome";

Vue.use(Router)

export default new Router({
  routes: [
      {
      path: '/',
      name: 'home',
      component: PageContentHome
    },
      {
      path: '/registration',
      name: 'registration',
      component: Registration
    }
  ],
  mode: 'history'
})
