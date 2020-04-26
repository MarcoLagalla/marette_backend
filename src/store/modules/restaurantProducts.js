/* eslint-disable no-unused-vars */
import manageProduct from "../../services/manageProduct";

const state = {
    ID: 1,
    productList: [],
    status: '',

    FOOD_CATEGORY_CHOICES : [
        'Altro',
        'Antipasto',
        'Primo',
        'Secondo',
        'Contorno',
        'Dessert',
        'Caffetteria',
        'Panetteria',
        'Panini e Piadine',
        'Pizza',
        'Secondo',
        'Snack',
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
}

const actions = {
    getRestaurantData: ({commit}, restaurantID) => {
        return new Promise((resolve, reject) => { // The Promise used for router redirect in login
            commit('PROD_REST_REQUEST', restaurantID)
            manageProduct.getProductList(restaurantID)
            .then(resp => {
                const data = resp.data
                /*var products = {}
                state.FOOD_CATEGORY_CHOICES.forEach((item, index) =>{products[item]=[]})
                data.forEach((product, index)=>{
                    products[product['category']].push(product)
                })*/
                commit('PROD_REST_SUCCESS', data)
                resolve(resp)
            })
            .catch(err => {
                commit('PROD_REST_ERROR', err.response)
                reject(err.response.data)
            })
        })
    },

}

const mutations = {
    PROD_REST_REQUEST: (state, ID) => {
        state.status = 'loading'
        state.ID = ID
    },

    PROD_REST_SUCCESS: (state, data) => {
        state.status = 'success'
        state.productList = data
    },

    PROD_REST_ERROR: (state, error) => {
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