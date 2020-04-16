/* eslint-disable no-unused-vars */
import manageUserProfile from "../../services/manageUserProfile"
import sendUserAuthentication from "../../services/sendUserAuthentication";


const state = {
  user:{

    id: '',
    username: '',
    email: '',
    first_name: "",
    last_name: "",
    birth_date: "",
    phone: "",
    is_superuser: false,

  },

  errors: [],
  status: '',

}

const getters = {
 /* isSuperuser: state => state.is_superuser,
  id: state => state.id,
  username: state => state.username,*/

  user: state => state.user,
  errors: state=> state.errors,
}

const actions = {


  getUserData: ({commit, dispatch}, id) => {
    commit('USER_REQUEST')
    manageUserProfile.getUserProfile(id)
        .then(resp => {
          const data = resp.data
          data.id = id
          commit('USER_SUCCESS', data)
        })
        .catch(err => {
          dispatch("userAuthentication/logout", null, {root: true});
          commit('USER_ERROR');
        })
  },

  logout: ({commit}) => {
    commit('USER_PROF_LOGOUT')
  },

  changePassword: ({commit}, data) => {
    return new Promise((resolve, reject) => {
      commit('USER_REQUEST')

      manageUserProfile.changePassword(state.user.id, data)
          .then(resp => {

            commit('PSW_CHANGE_SUCCESS', resp.data.password)
            updateCookie(resp.data)
            resolve(resp.data.password)

          })
          .catch(err => {

            commit('PSW_CHANGE_ERROR', err.response)
            reject(err)

          })
    })
  }
}

const mutations = {
  USER_REQUEST: (state) => {
    state.status = 'loading'
  },

  USER_SUCCESS: (state, data) => {
    state.status = 'success'
    state.user.username = data.username
    state.user.id = data.id
    state.user.email = data.email
    state.user.first_name = data.first_name
    state.user.last_name = data.last_name
    state.user.birth_date = data.birth_date
    state.user.phone = data.phone
    state.user.is_superuser = data.is_superuser
  },

  PSW_CHANGE_SUCCESS: (state) => {
    state.status = 'success'
  },

  PSW_CHANGE_ERROR: (state, error) => {
    state.status = 'error'
    state.errors = error.data
  },

  USER_PROF_LOGOUT: (state) => {
    state.status = ''
    state.user.username =  ''
    state.user.id =  ''
    state.user.email =  ''
    state.user.first_name =  ''
    state.user.last_name =  ''
    state.user.birth_date = ''
    state.user.phone =  ''
    state.user.is_superuser =  ''
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
function updateCookie( data ) {
  var d = new Date();
  var exdays = 364;
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  var expires = "expires="+ d.toUTCString();
  document.cookie = "user-token=" + data.token + ";" + expires + ";path=/";//TODO: flaggare il cookie come sicuro solo quando avremo https
}