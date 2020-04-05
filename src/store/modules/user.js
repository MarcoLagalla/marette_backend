import userAutentication from '@/services/userAutentication'

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
    userAutentication.postRegisterUser(user)
    .then(() => {
      commit('registerUser', user)
    })
  }
}

const mutations = {
  registerUser(state, user) {
    state.user.push(user)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}