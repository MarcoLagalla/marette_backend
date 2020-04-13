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

/*const ifAuthenticated = (to, from, next) => {
  if (store.getters['userAuthentication/isAuthenticated']) {
    next();
    return;
  }
  next("/login");
};*/

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  scrollBehavior: (to, from, savedPosition) => {
    if (to.hash) return { selector: to.hash }
    if (savedPosition) return savedPosition

    return { x: 0, y: 0 }
  },
  routes: [
  {
      path: '/rest1',
      component: () => import('@/layouts/rest1/Index.vue'),
      children: [
        {
          path: '',
          name: 'Rest1',
          component: () => import('@/views/pages/rest1.vue'),
        },
      ],
    },
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
          path: 'about',
          name: 'About',
          component: () => import('@/views/pages/about.vue'),
          meta: { src: require('@/assets/about.jpg') },
        },
        {
          path: 'contact-us',
          name: 'Contact',
          component: () => import('@/views/pages/contact-us.vue'),
          meta: { src: require('@/assets/contact.jpg') },
        },
        {
          path: 'registration',
          name: 'Registration',
          component: () => import('@/views/pages/registration.vue'),
          beforeEnter: ifNotAuthenticated,
          //meta: { src: require('@/assets/.jpg') },
        },
        {
          path: 'login',
          name: 'Login',
          component: () => import('@/views/pages/login.vue'),
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
