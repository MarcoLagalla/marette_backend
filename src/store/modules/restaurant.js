/* eslint-disable no-unused-vars */
import postRegisterRestaurant from  '../../services/manageRestaurant'

const state = {
    status: '',
    errors: [],
    id_restaurant: '',
    list: [],
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
    restaurantList: state => state.list,
    errors: state => state.errors,
    food_category_choice: state => state.food_category_choice,
    discount_type_choice: state => state.discount_type_choice,

}

const actions = {
    newRestaurant: ({commit, dispatch}, restaurant) => {
        return new Promise((resolve, reject) => { // The Promise used for router redirect in login
            commit('REG_REST_REQUEST')
            postRegisterRestaurant.postRegisterRestaurant(restaurant)
            .then(resp => {
                const data = resp.data
                commit('REG_REST_SUCCESS', data.id_restaurant)
                resolve(resp)
            })
            .catch(err => {
                commit('REG_REST_ERROR', err.response)
                reject(err.response.data)
            })
        })
    },

    getRestaurants: ({commit, dispatch}) => {
        return new Promise((resolve, reject) => { // The Promise used for router redirect in login
            postRegisterRestaurant.getRestaurantList()
            .then(resp => {
                const data = resp.data
                commit('REST_LIST_SUCCESS', data)
                resolve(resp)
            })
            .catch(err => {
                commit('REST_LIST_ERROR')
                reject(err)
            })
        })
    },
}

const mutations = {
    REG_REST_REQUEST: (state) => {
        state.status = 'loading'
    },
    REG_REST_SUCCESS: (state, id_restaurant) => {
        state.status = 'success'
        state.id_restaurant = id_restaurant
    },
    REG_REST_ERROR: (state, error) => {
        state.status = 'error'
        state.errors = error.data
    },
    REST_LIST_SUCCESS: (state, list) => {
        state.list = list
    },
    REST_LIST_ERROR: (state) => {
        state.status = 'error_list'
    },

}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
