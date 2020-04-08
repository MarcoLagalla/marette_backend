// Imports
import Vue from 'vue'
import Router from 'vue-router'
import store from "@/store"

Vue.use(Router)

const ifNotAuthenticated = (to, from, next) => {
  if (!store.getters['userAutentication/isAuthenticated']) {
    next();
    return;
  }
  next("/");
};

/*const ifAuthenticated = (to, from, next) => {
  if (store.getters['userAutentication/isAuthenticated']) {
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
      path: '/',
      component: () => import('@/layouts/home/Index.vue'),
      children: [
        {
          path: '',
          name: 'Home',
          component: () => import('@/views/home/Index.vue'),
        },
        {
          path: 'about',
          name: 'About',
          component: () => import('@/views/about/Index.vue'),
          meta: { src: require('@/assets/about.jpg') },
        },
        {
          path: 'contact-us',
          name: 'Contact',
          component: () => import('@/views/contact-us/Index.vue'),
          meta: { src: require('@/assets/contact.jpg') },
        },
        {
          path: 'pro',
          name: 'Pro',
          component: () => import('@/views/pro/Index.vue'),
          meta: { src: require('@/assets/pro.jpg') },
        },
        {
          path: 'registration',
          name: 'Registration',
          component: () => import('@/views/registration/Index.vue'),
          //meta: { src: require('@/assets/.jpg') },
        },
        {
          path: 'login',
          name: 'Login',
          component: () => import('@/views/login/Index.vue'),
          beforeEnter: ifNotAuthenticated,
        },
        {
          path: '*',
          name: 'FourOhFour',
          component: () => import('@/views/404/Index.vue'),
        },
      ],
    },

  ],
})

export default router
