// Imports
import Vue from 'vue'
import Router from 'vue-router'
import store from "@/store"

Vue.use(Router)

const ifNotAuthenticated = (to, from, next) => {
  if (!store.getters['userAuthentication/isAuthenticated']) {
    next();
    return;
  }
  next("/");
};

const ifAuthenticated = (to, from, next) => {
  if (store.getters['userAuthentication/isAuthenticated']) {
    next();
    return;
  }
  next("/");
};

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  scrollBehavior: (to, from, savedPosition) => {
    if (to.hash) return { selector: to.hash }
    if (savedPosition) return savedPosition

    return { x: 0, y: 0 }
  },
  routes: [
/*  {
      path: '/rest1',
      component: () => import('@/layouts/rest1/Index.vue'),
      children: [
        {
          path: '',
          name: 'Rest1',
          component: () => import('@/views/pages/rest1.vue'),
        },
      ],
    },*/
    {
      path: '/',
      component: () => import('@/layouts/home/Index.vue'),
      children: [
        {
          path: '',
          name: 'Home',
          component: () => import('@/views/pages/home.vue'),
        },
        {
          path: 'rest1',
          name: 'Rest1',
          component: () => import('@/views/pages/rest1.vue'),
        },
        {
          path: 'about',
          name: 'About',
          component: () => import('@/views/pages/about.vue'),
          //meta: { src: require('@/assets/about.jpg') },
        },

        {
          path: 'registrationBusiness',
          name: 'RegBusiness',
          component: () => import('@/views/pages/registrationBusiness.vue'),
          beforeEnter: ifNotAuthenticated,
        },
        {
          path: 'newRestaurant',
          name: 'NewRestaurant',
          component: () => import('@/views/pages/newRestaurant.vue'),
          beforeEnter: ifAuthenticated, //TODO: solo se è business
        },
        {
          path: 'profile',
          name: 'profile',
          component: () => import('@/views/pages/profile.vue'),
          beforeEnter: ifAuthenticated,
        },
        {
          path: 'profile/:id',
          name: 'ManageRest',
          component: () => import('@/views/pages/manageRest.vue'),
          beforeEnter: ifAuthenticated, //TODO: solo se è business
        },
        {
          path: 'resetpass',
          name: 'resetpass',
          component: () => import('@/views/pages/resetPass.vue'),
          beforeEnter: ifNotAuthenticated,
        },

        {
          path: '*',
          name: 'FourOhFour',
          component: () => import('@/views/pages/404.vue'),
        },
      ],
    },


  ],
})

export default router
