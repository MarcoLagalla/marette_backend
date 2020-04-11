import sendUserAuthentication from '../../services/sendUserAuthentication'



const state = {
  token: getCookie("user-token") || '',
  status: '',
  errors: [],
  id: getCookie("user-id") || ''
}

const getters = {
  isAuthenticated: state => !!state.token,
  status: state => state.status,
  errors: state => state.errors,
  id: state => state.id,
}

const actions = {

  signIn: ({commit, dispatch}, user) => {
    return new Promise((resolve, reject) => { // The Promise used for router redirect in login
      commit('AUTH_REQUEST')
          sendUserAuthentication.signUser(user)
        .then(resp => {
          const data = resp.data
          setTokenCookie(data)
          commit('AUTH_SUCCESS', data)

          dispatch("userProfile/getUserData", data.id,  { root: true });

          resolve(resp)
        })
      .catch(err => {
        commit('AUTH_ERROR', err.response)
        deleteTokenCookie();

        reject(err)
      })
    })
  },
  registerUser: ({commit, dispatch}, user) => {
    return new Promise((resolve, reject) => { // The Promise used for router redirect in login
      commit('AUTH_REQUEST')
          sendUserAuthentication.postRegisterUser(user)
        .then(resp => {
          const data = resp.data
          setTokenCookie(data.token);
          commit('AUTH_SUCCESS', data)

          dispatch("userProfile/getUserData", data.id,  { root: true });

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
    state.id = data.id
    state.errors = []
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

function setTokenCookie( data) {
  var d = new Date();
  var exdays = 364;
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  var expires = "expires="+ d.toUTCString();
  document.cookie = "user-token=" + data.token + ";" + expires + ";path=/";
  document.cookie = "user-id=" + data.id + ";" + expires + ";path=/";
}

function deleteTokenCookie() {
  document.cookie = "user-token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
  document.cookie = "user-id=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
}

function getCookie(name) {
  name = name + "=";
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

