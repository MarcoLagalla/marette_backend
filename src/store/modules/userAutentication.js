import sendUserAutentication from '../../services/sendUserAutentication'
const state = {
  token: localStorage.getItem('user-token') || '',
  status: '',
  errors: []
}

const getters = {
  isAuthenticated: state => !!state.token,
  status: state => state.status,
  errors: state => state.errors

}

const actions = {

  signIn: ({commit}, user) => {
    return new Promise((resolve, reject) => { // The Promise used for router redirect in login
      commit('AUTH_REQUEST')
          sendUserAutentication.signUser(user)
        .then(resp => {
          const token = resp.data.token
          localStorage.setItem('user-token', token) // store the token in localstorage
          commit('AUTH_SUCCESS', token)

          resolve(resp)
        })
      .catch(err => {
        commit('AUTH_ERROR', err.response)
        localStorage.removeItem('user-token') // if the request fails, remove any possible user token if possible

        reject(err)
      })
    })
  },
  registerUser: ({commit}, user) => {
    return new Promise((resolve, reject) => { // The Promise used for router redirect in login
      commit('AUTH_REQUEST')
          sendUserAutentication.postRegisterUser(user)
        .then(resp => {
          const token = resp.data.token
          localStorage.setItem('user-token', token) // store the token in localstorage
          commit('AUTH_SUCCESS', token)

          resolve(resp)
        })
      .catch(err => {
        commit('AUTH_ERROR', err.response)
        localStorage.removeItem('user-token') // if the request fails, remove any possible user token if possible

        reject(err)
      })
    })
  },

  LogOut: ({commit}) => {
    return new Promise((resolve) => {
      commit('AUTH_LOGOUT')
      localStorage.removeItem('user-token') // clear your user's token from localstorage
      resolve()
    })
  }
}

const mutations = {

  AUTH_REQUEST: (state) => {
    state.status = 'loading'
  },
  AUTH_SUCCESS: (state, token) => {
    state.status = 'success'
    state.token = token
  },
  AUTH_ERROR: (state, error) => {
    state.status = 'error'
    state.errors = error.data
  },


}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}