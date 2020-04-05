import sendUserAutentication from '../../services/sendUserAutentication'

const state = {
  result: {},
}

const getters = {

  result: state => {
    return state.result
  }

}

const actions = {
  registerUser({ commit }, result) {
    sendUserAutentication.postRegisterUser(result)
    .then((response) => {
      commit('updateResult', response);
    })
  },

  signIn({commit}, result) {
    sendUserAutentication.signUser(result)
        .then((response) => {
          commit('updateResult', response);
        })
  }
}

const mutations = {

  updateResult(state, result) {
    state.result= result
  },


}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}