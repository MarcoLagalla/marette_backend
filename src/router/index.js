// Imports
import Vue from 'vue'
import Router from 'vue-router'
import store from "@/store"
import RestMenu from "../components/base/RestMenu";
import restaurant from "../views/pages/restaurant";
import RestMenuMobile from "../components/base/RestMenuMobile";
import ManageRest from "../views/pages/manageRest";

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
  next("/");
};*/

const downloadProfileData = (to, from, next) => {
  if (store.getters['userAuthentication/isAuthenticated']) {
    store.dispatch("userProfile/getUserData", getID()).then(()=> {
      next();
    }).catch(()=>{
       next("/");
     })

    return;
  }
  next("/");
};

const ifBusiness = (to, from, next) => {
  if (store.getters['userProfile/isBusiness']) {
    next();
    return;
  }
  next("/");
};

const ifOwner = (to, from, next) => {
  if (store.getters['userProfile/isBusiness'] && store.getters['userProfile/restaurants'].includes(Number(to.params.id))){
     store.dispatch("restaurantData/getRestaurantData", to.params.id).then(()=>{
        if (store.getters['restaurantData/slug'] === to.params.name)
          next();
        else
          next("/404");
     }).catch(()=>{
       next("/404");
     })
    return;
  }
  next("/");
};

const ifExist = (to, from, next) => {
  store.dispatch("restaurantData/getRestaurantData", to.params.id).then(()=>{
    if (store.getters['restaurantData/slug'] === to.params.name)
      next();
    else
      next("/404");
  }).catch(()=>{
    next("/404");
  })
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
          //meta: { src: require('@/assets/about.jpg') },
        },
        {
          path: 'termini',
          name: 'TerminiECondizioni',
          component: () => import('@/views/pages/TerminiECondizioni.vue'),
          //meta: { src: require('@/assets/about.jpg') },
        },

        {
          path: 'registrationBusiness',
          name: 'RegBusiness',
          component: () => import('@/views/pages/registrationBusiness.vue'),
        },
        {
          path: 'newRestaurant',
          name: 'NewRestaurant',
          component: () => import('@/views/pages/newRestaurant.vue'),
          beforeEnter: ifBusiness
        },
        {
          path: 'profile',
          name: 'profile',
          component: () => import('@/views/pages/profile.vue'),
          beforeEnter:  downloadProfileData,
        },
        {
          path: 'profile/manage/:id/:name',
          name: 'ManageRestData',
          component: () => import('@/views/pages/manageRestData.vue'),
          beforeEnter:  ifOwner,
        },
        {
          path: 'profile/:id/:name',
          name: 'ManageRest',
          components: {
            default: ManageRest,
            restMenu: RestMenu,
            restMenuMobile: RestMenuMobile
          },
          beforeEnter: ifOwner,
        },
        {
          path: 'resetpass',
          name: 'resetpass',
          component: () => import('@/views/pages/resetPass.vue'),
          beforeEnter: ifNotAuthenticated,
        },
        {
          path: 'activate/:id/:token',
          name: 'ValidateEmail',
          component: () => import('@/views/pages/validateEmail.vue'),
        },
        {
          path: ':id/:name',
          name: 'RestaurantHome',
          components: {
            default: restaurant,
            restMenu: RestMenu,
            restMenuMobile: RestMenuMobile
          },
          beforeEnter: ifExist,
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

function getID() {
 var result = document.cookie.match(new RegExp('user_private' + '=([^;]+)'));
 result && (result = JSON.parse(result[1]));
 return result ? result.id : '';
}


export default router
