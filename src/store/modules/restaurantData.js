/* eslint-disable no-unused-vars */
import manageProduct from "../../services/manageProduct";
import manageRestaurant from "../../services/manageRestaurant";

const state = {
    ID: 1,
    productList: [],
    restData: {},
    status: '',
    components: [
        'Home',
        'Vetrina',
        'Menu',
        'Galleria',
        'Info'
    ],

    FOOD_CATEGORY_CHOICES : [
        'Altro',
        'Antipasto',
        'Contorno',
        'Dessert',
        'Caffetteria',
        'Panetteria',
        'Panini e Piadine',
        'Pizza',
        'Primo',
        'Secondo',
        'Snack'
    ],

    DISCOUNT_TYPE_CHOICE: [
        'Fisso',
        'Percentuale'
    ],

}

const getters = {
    food_category_choice: state => state.food_category_choice,
    discount_type_choice: state => state.discount_type_choice,
    productList: state => state.productList,
    components: state => state.components,
    restData: state => state.restData,
}

const actions = {
    addComponent: ({commit}, componentName) =>{
        commit('REST_ADD_COMPONENT', componentName)
    },
    removeComponent: ({commit}, componentName) =>{
        commit('REST_RMV_COMPONENT', componentName)
    },
    getRestaurantData: ({commit}, restaurantID) => {
        return new Promise((resolve, reject) => {
            commit('REST_DATA_REQUEST', restaurantID)
            manageRestaurant.getRestaurantData(restaurantID)
            .then(respRes => {
                const dataRes = respRes.data

                commit('REST_DATA_SUCCESS', dataRes)

                commit('REST_MENU_REQUEST', restaurantID)

                manageProduct.getProductList(restaurantID)
                .then(respMenu => {
                    const dataMenu = respMenu.data

                    commit('REST_MENU_SUCCESS', dataMenu)
                    resolve()
                })
                .catch(err => {
                    commit('REST_MENU_ERROR', err.response)
                    reject(err.response)
                })
            })
            .catch(err => {
                commit('REST_DATA_ERROR', err.response)
                reject(err.response)
            })
        })
    },

}

const mutations = {
    REST_RMV_COMPONENT: (state, componentName) =>{
        state.components.splice(state.components.indexOf(componentName), 1);
    },

    REST_ADD_COMPONENT: (state, componentName) =>{
        state.components.push(componentName);
    },

    REST_DATA_REQUEST: (state, ID) => {
        state.status = 'loading'
        state.ID = ID
    },

    REST_DATA_SUCCESS: (state, data) =>{
        state.restData = data
    },

    REST_MENU_REQUEST: (state) => {
        state.status = 'loading'
    },

    REST_MENU_SUCCESS: (state, data) => {
        state.status = 'success'
        state.productList = data
    },

    REST_MENU_ERROR: (state, error) => {
        state.status = 'error'
        state.error = error
    },

    REST_DATA_ERROR: (state, error) => {
        state.status = 'error'
        state.error = error
    },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}