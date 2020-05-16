/* eslint-disable no-unused-vars */
import manageUserProfile from "../../services/manageUserProfile"
import sendUserAuthentication from "../../services/sendUserAuthentication";


const state = {
  user:{

  },

  user_private : getUserPrivateCookie() || {
        id: '',
        is_superuser: false,
        type:"",
        restaurants:[],
  },

  errors: [],
  status: '',


}

const getters = {
 /* isSuperuser: state => state.is_superuser,
  id: state => state.id,
  username: state => state.username,*/

  isBusiness: state => state.user_private.type==='business',
  user: state => state.user,
  errors: state=> state.errors,
  user_private: state => state.user_private,
  restaurants: state => state.user_private.restaurants
}

const actions = {


  getUserData: ({commit, dispatch}, id) => {
    commit('USER_REQUEST')
    manageUserProfile.getUserProfile(id)
        .then(resp => {
          const data = resp.data
          data.id = id
          setCookiesUserPrivate(data)
          commit('USER_SUCCESS', data)
        })
        .catch(err => {
          dispatch("userAuthentication/logout", null, {root: true});
          commit('USER_ERROR');
        })
  },

  logout: ({commit}) => {
    deleteUserPrivateCookies()
    commit('USER_PROF_LOGOUT')
  },

  addRestaurant: ({commit}, restID) => {
    commit('USER_ADD_REST', restID)
  },

  changePassword: ({commit}, data) => {
    return new Promise((resolve, reject) => {
      commit('USER_REQUEST')

      manageUserProfile.changePassword(state.user_private.id, data)
          .then(resp => {

            commit('PSW_CHANGE_SUCCESS', resp.data.password)
            updateTokenCookie(resp.data.token)
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
    state.user_private.type = data.type
    state.user_private.id = data.id
    state.user_private.is_superuser = data.is_superuser

    state.user.Username = data.username
    state.user.Email = data.email
    state.user.Nome = data.first_name
    state.user.Cognome = data.last_name
    state.user.Anno_di_Nascita = data.birth_date
    state.user.Numero_di_Telefono = data.phone

    if (state.user_private.type === 'business')
    {
      state.user.Codice_Fiscale = data.cf
      state.user.Indirizzo = data.address + ', ' + data.city + ', ' + data.cap
      state.user_private.restaurants = data.restaurants
    }

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
    state.user = { }
    state.user_private = { }

  },

  USER_ERROR: (state) => {
    state.status = 'error'
  },

  USER_ADD_REST: (state, restId) => {
    state.user_private.restaurants.push(restId)
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
function updateTokenCookie( token ) {
  var d = new Date();
  var exdays = 364;
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  var expires = "expires="+ d.toUTCString();
  if (process.env.NODE_ENV === 'production') {
    document.cookie = "user-token=" + token + ";" + expires + "; SameSite=Lax ; Secure ;path=/";
  }
  else
    document.cookie = "user-token=" + token + ";" + expires + "; SameSite=Lax ;path=/";
}

function setCookiesUserPrivate( data) {
  var user_private = {}
    user_private['type']=data.type
    user_private['id'] = data.id
    user_private['is_superuser'] = data.is_superuser
    if (data.type === 'business')
       user_private['restaurants'] = data.restaurants
  var d = new Date();
  var exdays = 364;
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  var expires = "expires="+ d.toUTCString();
  if (process.env.NODE_ENV === 'production') {
    document.cookie = "user_private=" + JSON.stringify(user_private) + ";" + expires + "; SameSite=Lax ; Secure ;path=/";
  }
  else
    document.cookie = "user_private=" + JSON.stringify(user_private) + ";" + expires + "; SameSite=Lax ;path=/";
}

function deleteUserPrivateCookies() {
  if (process.env.NODE_ENV === 'production') {
    document.cookie = "user_private=; expires=Thu, 01 Jan 1970 00:00:00 UTC ; SameSite=Lax ; Secure ; path=/;";
  }
  else
    document.cookie = "user_private=; expires=Thu, 01 Jan 1970 00:00:00 UTC ; SameSite=Lax ; path=/;";
}


function getUserPrivateCookie() {
 var result = document.cookie.match(new RegExp('user_private' + '=([^;]+)'));
 result && (result = JSON.parse(result[1]));
 return result;
}