import messageService from '../../services/userAutentication'

const state = {
  user: []
}

const getters = {
  user: state => {
    return state.user
  }
}

const actions = {
  registerUser({ commit }, user) {
    messageService.postRegisterUser(user)
    .then(() => {
      commit('registerUser', user)
    })
  }
}

const mutations = {
  registerUser(state, user) {
    state.messages.push(user)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}