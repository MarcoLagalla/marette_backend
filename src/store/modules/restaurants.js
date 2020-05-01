/* eslint-disable no-unused-vars */
import manageRestaurant from "../../services/manageRestaurant";

const state = {
    status: '',
    errors: [],
    id_restaurant: '',
    list: [],
    userList: []
}

const getters = {
    restaurantList: state => state.list,
    errors: state => state.errors,
    userList: state => state.userList

}

const actions = {
    newRestaurant: ({commit}, restaurant) => {
        return new Promise((resolve, reject) => {
            commit('REG_REST_REQUEST')
            manageRestaurant.postRegisterRestaurant(restaurant)
            .then(resp => {
                const data = resp.data
                commit('REG_REST_SUCCESS', data.id_restaurant)
                resolve(resp.data)
            })
            .catch(err => {
                commit('REG_REST_ERROR', err.response)
                reject(err.response.data)
            })
        })
    },

    getRestaurants: ({commit}) => {
        return new Promise((resolve, reject) => {
            manageRestaurant.getRestaurantList()
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

    getUserRestaurants: ({commit, rootGetters}) => {
        return new Promise((resolve, reject) => {
            commit('REST_USR_LIST_REQUEST')
            var restaurants = rootGetters["userProfile/restaurants"];

            restaurants.forEach((restaurantID) =>{
                manageRestaurant.getRestaurantData(restaurantID).then(resp => {
                    const data = resp.data
                    commit('REST_USR_LIST_ADD', data)

                })
                .catch(err => {
                    commit('REST_USR_LIST_ERROR')
                    reject(err)
                })
            })
            resolve(state.userList)

        })
    },
}

const mutations = {
    REST_USR_LIST_REQUEST: (state) => {
        state.userList = []
    },

    REST_USR_LIST_ADD: (state, rest) => {
        state.userList.push(rest)
    },

    REST_USR_LIST_ERROR: (state, rest) => {
        state.userList.push(rest)
    },

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
