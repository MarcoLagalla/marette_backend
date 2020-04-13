/* eslint-disable no-unused-vars */

import sendUserAuthentication from "../../services/sendUserAuthentication";

const state = {

}

const getters = {

}

const actions = {
    registerRestaurant: ({commit, dispatch}, restaurant) => {
    return new Promise((resolve, reject) => { // The Promise used for router redirect in login
      commit('AUTH_REQUEST')
          sendUserAuthentication.postRegisterRestaurant(restaurant)
        .then(resp => {
          const data = resp.data
          commit('AUTH_SUCCESS', data)

          resolve(resp)
        })
      .catch(err => {
        commit('AUTH_ERROR', err.response)
        reject(err)
      })
    })
  },

}

const mutations = {

}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
