import Vue from 'vue'
import Router from 'vue-router'
import Registration from "./components/Registration";
import Login from "./components/Login";
import PageContentHome from "./components/PageContentHome";

Vue.use(Router)

const ifNotAuthenticated = (to, from, next) => {
  if (!store.getters.isAuthenticated) {
    next();
    return;
  }
  next("/");
};

const ifAuthenticated = (to, from, next) => {
  if (store.getters.isAuthenticated) {
    next();
    return;
  }
  next("/login");
};

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
          component: Registration,
          beforeEnter: ifNotAuthenticated
      },
      {
          path: '/login',
          name: 'login',
          component: Login,
          beforeEnter: ifNotAuthenticated
      },
  ],
  mode: 'history'
})
