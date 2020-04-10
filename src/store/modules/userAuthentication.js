import sendUserAuthentication from '../../services/sendUserAuthentication'
const state = {
  token: getToken() || '',//localStorage.getItem('user-token') || '',
  status: '',
  errors: [],
  username: ''
}

const getters = {
  isAuthenticated: state => !!state.token,
  status: state => state.status,
  errors: state => state.errors,
  username: state => state.username,

}

const actions = {

  signIn: ({commit}, user) => {
    return new Promise((resolve, reject) => { // The Promise used for router redirect in login
      commit('AUTH_REQUEST')
          sendUserAuthentication.signUser(user)
        .then(resp => {
          const data = resp.data
          setTokenCookie(data.token)
          data.username = user.username
          commit('AUTH_SUCCESS', data)

          resolve(resp)
        })
      .catch(err => {
        commit('AUTH_ERROR', err.response)
        deleteTokenCookie();

        reject(err)
      })
    })
  },
  registerUser: ({commit}, user) => {
    return new Promise((resolve, reject) => { // The Promise used for router redirect in login
      commit('AUTH_REQUEST')
          sendUserAuthentication.postRegisterUser(user)
        .then(resp => {
          const data = resp.data
          setTokenCookie(data.token);
          commit('AUTH_SUCCESS', data)

          resolve(resp)
        })
      .catch(err => {
        commit('AUTH_ERROR', err.response)
        deleteTokenCookie();
        reject(err)
      })
    })
  },

  logout: ({commit}) => {
    return new Promise((resolve, reject) => {
      sendUserAuthentication.logout().then( function(){
          commit('AUTH_LOGOUT')
          deleteTokenCookie();
          resolve()
        })
      .catch(err => {
        commit('AUTH_ERROR', err.response)

        reject(err)
      })

    })
  }
}

const mutations = {

  AUTH_REQUEST: (state) => {
    state.status = 'loading'
  },
  AUTH_SUCCESS: (state, data) => {
    state.status = 'success'
    state.token = data.token
    state.username = data.username
  },
  AUTH_ERROR: (state, error) => {
    state.status = 'error'
    state.errors = error.data
  },
  AUTH_LOGOUT: state => {
    state.token = "";
  }


}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}

function setTokenCookie( cvalue) {
  var d = new Date();
  var exdays = 364;
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  var expires = "expires="+ d.toUTCString();
  document.cookie = "user-token=" + cvalue + ";" + expires + ";path=/";
}

function deleteTokenCookie() {
  document.cookie = "user-token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
}

function getToken() {
  var name = "user-token=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}
