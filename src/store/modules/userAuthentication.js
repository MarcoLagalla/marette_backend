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
          setCookies(data)
          commit('AUTH_SUCCESS', data)

          dispatch("userProfile/getUserData", data.id,  { root: true });

          resolve(resp)
        })
      .catch(err => {
        commit('AUTH_ERROR', err.response)
        deleteCookies();

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
          setCookies(data);
          commit('AUTH_SUCCESS', data)

          dispatch("userProfile/getUserData", data.id,  { root: true });

          resolve(resp)
        })
      .catch(err => {
        commit('AUTH_ERROR', err.response)
        deleteCookies();
        reject(err)
      })
    })
  },

  registerBusiness: ({commit, dispatch}, user) => {
    return new Promise((resolve, reject) => { // The Promise used for router redirect in login
      commit('AUTH_REQUEST')
          sendUserAuthentication.postRegisterBusiness(user)
        .then(resp => {
          const data = resp.data
          setCookies(data.token);
          commit('AUTH_SUCCESS', data)

          dispatch("userProfile/getUserData", data.id,  { root: true });

          resolve(resp)
        })
      .catch(err => {
        commit('AUTH_ERROR', err.response)
        deleteCookies();
        reject(err.response.data)
      })
    })
  },

  logout: ({commit, dispatch}) => {
    return new Promise((resolve, reject) => {
      sendUserAuthentication.logout().then( function(){
          commit('AUTH_LOGOUT')
          deleteCookies();
          dispatch("userProfile/logout", null,  { root: true });
          resolve()
        })
      .catch(err => {
        commit('AUTH_LOGOUT')
        deleteCookies();
        dispatch("userProfile/logout", null,  { root: true });
        commit('AUTH_ERROR', err.response)

        reject(err)
      })

    })
  },

  AskPasswordreset: ({commit}, data) => {
    return new Promise((resolve, reject) => {
      commit('AUTH_REQUEST')

      sendUserAuthentication.AskPasswordreset(data)
          .then(resp => {
            commit('ASK_PSW_RESET_SUCCESS', resp.data)
            resolve(resp.data.password)

          })
          .catch(err => {

            commit('ASK_PSW_RESET_ERROR', err.response)
            reject(err)

          })
    })
  },

  ConfirmPasswordreset: ({commit}, data) => {
    return new Promise((resolve, reject) => {
      commit('USER_REQUEST')

      sendUserAuthentication.ConfirmPasswordreset( data)
          .then(resp => {

            commit('PSW_CHANGE_SUCCESS', resp.data.password)
            resolve(resp.data.password)

          })
          .catch(err => {

            commit('PSW_CHANGE_ERROR', err.response)
            reject(err)

          })
    })
  },

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
    state.id = "";
  },

  ASK_PSW_RESET_SUCCESS: (state) => {
    state.status = 'success'
  },

  ASK_PSW_RESET_ERROR: (state, error) => {
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

function setCookies( data) {
  var d = new Date();
  var exdays = 364;
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  var expires = "expires="+ d.toUTCString();
  document.cookie = "user-token=" + data.token + ";" + expires + ";path=/";//TODO: flaggare il cookie come sicuro solo quando avremo https
  document.cookie = "user-id=" + data.id + ";" + expires + ";path=/";
}

function deleteCookies() {
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

