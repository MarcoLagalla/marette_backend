import userAutentication from '../../services/userAutentication'

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
    userAutentication.postRegisterUser(result)
    .then((response) => {
      commit('updateResult', response);
    })
  },

  signIn({commit}, result) {
    userAutentication.signUser(result)
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