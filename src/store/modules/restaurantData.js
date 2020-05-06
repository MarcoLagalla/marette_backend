/* eslint-disable no-unused-vars */
import manageProduct from "../../services/manageProduct";
import manageRestaurant from "../../services/manageRestaurant";

const state = {
    ID: 1,
    productList: {},
    restData: {},
    status: '',
    tags:{},
    discounts:{},

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


}

const getters = {
    food_category_choice: state => state.food_category_choice,
    discount_type_choice: state => state.discount_type_choice,
    productList: state => state.productList,
    components: state => state.restData.components,
    restData: state => state.restData,
    tags: state => state.tags,
    discounts: state => state.discounts
}

const actions = {
    activateComponent: ({commit}, componentName) =>{
         return new Promise((resolve, reject) => {
             var payload = {id: state.ID, component: componentName}
             manageRestaurant.activateComponent(payload)
                 .then(respRes => {
                    commit('REST_ADD_COMPONENT', componentName)
                 })
         })

    },
    deactivateComponent: ({commit}, componentName) =>{
         return new Promise((resolve, reject) => {
             var payload = {id: state.ID, component: componentName}
             manageRestaurant.deactivateComponent(payload)
                 .then(respRes => {
                    commit('REST_RMV_COMPONENT', componentName)
                 })
         })

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
                    commit('REST_MENU_SUCCESS', respMenu.data)
                    resolve(respRes.data.components)
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



    addProduct: ({commit}, product) => {
        return new Promise((resolve, reject) => {

            var payload = {}
            payload['id'] = state.ID
            payload['data'] = product
            console.log(product)

            manageProduct.addProduct(payload)
            .then(resp => {
                commit('REST_ADD_PROD_SUCCESS')
                resolve(resp)
            })
            .catch(err => {
                commit('REST_ADD_PROD_ERROR')
                reject(err)
            })
        })
    },

    getListTag: ({commit}) => {
        return new Promise((resolve, reject) => {

            manageProduct.listTags()
            .then(resp => {
                commit('LIST_TAGS_SUCCESS', resp.data)
                console.log(resp)
                resolve(resp.data)
            })
            .catch(err => {
                commit('LIST_TAGS_ERROR')
                reject(err)
            })
        })
    },

    getListDiscounts: ({commit}) => {
        return new Promise((resolve, reject) => {

            manageProduct.listDiscounts(state.ID)
                console.log(state.ID)
            .then(resp => {
                commit('LIST_DISCOUNTS_SUCCESS', resp.data)
                console.log(resp)
                resolve(resp.data)
            })
            .catch(err => {
                commit('LIST_DISCOUNTS_ERROR')
                reject(err)
            })
        })
    },




}

const mutations = {
    REST_ADD_PROD_SUCCESS: () =>{
    },

    REST_ADD_PROD_ERROR: () =>{
    },

    REST_RMV_COMPONENT: (state, componentName) =>{
        state.restData.components[componentName].show=false;
    },

    REST_ADD_COMPONENT: (state, componentName) =>{
        state.restData.components[componentName].show=true;
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

    LIST_TAGS_SUCCESS: (state, data) => {
        state.status = 'success'
        state.tags = data
    },

    LIST_TAGS_ERROR: (state, error) => {
        state.status = 'error'
        state.error = error
    },

    LIST_DISCOUNTS_SUCCESS: (state, data) => {
        state.status = 'success'
        state.tags = data
    },

    LIST_DISCOUNTS_ERROR: (state, error) => {
        state.status = 'error'
        state.error = error
    }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}


