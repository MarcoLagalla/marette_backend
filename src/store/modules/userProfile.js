/* eslint-disable no-unused-vars */
import getUserProfile from "../../services/getUserProfile"
import sendUserAuthentication from "../../services/sendUserAuthentication";


const state = {
  id: '',
  username: '',
  email: '',
  first_name: "",
  last_name: "",
  birth_date: "",
  phone: "",
  is_superuser: false,
  status: ''
}

const getters = {
  isSuperuser: state => state.is_superuser,
  id: state => state.id,
  username: state => state.username,

}

const actions = {
  getUserData: ({commit, dispatch}, id) => {
    commit('USER_REQUEST')
    getUserProfile.getUserProfile(id)
    .then(resp => {
      const data = resp.data
      data.id = id
      commit('USER_SUCCESS', data)
    })
    .catch(err => {
      dispatch("userAuthentication/logout", null,  { root: true });
      commit('USER_ERROR');
    })
  },

  logout: ({commit}) => {
    commit('USER_PROF_LOGOUT')
  }

}

const mutations = {
  USER_REQUEST: (state) => {
    state.status = 'loading'
  },

  USER_SUCCESS: (state, data) => {
    state.status = 'success'
    state.username = data.username
    state.id = data.id
    state.email = data.email
    state.first_name = data.first_name
    state.last_name = data.last_name
    state.birth_date = data.birth_date
    state.cellphone_number = data.phone
    state.is_superuser = data.is_superuser
  },

  USER_PROF_LOGOUT: (state) => {
    state.status = ''
    state.username =  ''
    state.id =  ''
    state.email =  ''
    state.first_name =  ''
    state.last_name =  ''
    state.birth_date = ''
    state.cellphone_number =  ''
    state.is_superuser =  ''
  },

  USER_ERROR: (state) => {
    state.status = 'error'
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
