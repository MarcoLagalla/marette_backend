import sendUserAuthentication from '../../services/sendUserAuthentication'
const state = {
  token: localStorage.getItem('user-token') || '',
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
          localStorage.setItem('user-token', data.token) // store the token in localstorage
          setCookie('user-token', data.token, 365)
          data.username = user.username
          commit('AUTH_SUCCESS', data)

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
          sendUserAuthentication.postRegisterUser(user)
        .then(resp => {
          const data = resp.data
          localStorage.setItem('user-token', data.token) // store the token in localstorage
          commit('AUTH_SUCCESS', data)

          resolve(resp)
        })
      .catch(err => {
        commit('AUTH_ERROR', err.response)
        localStorage.removeItem('user-token') // if the request fails, remove any possible user token if possible

        reject(err)
      })
    })
  },

  logout: ({commit}) => {
    return new Promise((resolve, reject) => {
      sendUserAuthentication.logout().then( function(){
          commit('AUTH_LOGOUT')
          localStorage.removeItem('user-token') // clear your user's token from localstorage
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

function setCookie(cname, cvalue, exdays) {
  var d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  var expires = "expires="+ d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

/*function getToken() {
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
}*/
