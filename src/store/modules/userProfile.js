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
        avatar: ''
  },

  errors: [],
  status: '',
  cart: {
    selected_items: [],
    selected_menus: [],
  }


}

const getters = {
 /* isSuperuser: state => state.is_superuser,
  id: state => state.id,
  username: state => state.username,*/

  isBusiness: state => state.user_private.type==='business',
  user: state => state.user,
  errors: state=> state.errors,
  user_private: state => state.user_private,
  avatar: state => state.user_private.avatar,
  restaurants: state => state.user_private.restaurants,
  cart: state => state.cart

}

const actions = {
  getUserData: ({commit, dispatch}, id) => {
    return new Promise((resolve, reject) => {
      commit('USER_REQUEST')
      manageUserProfile.getUserProfile(id)
        .then(resp => {
          const data = resp.data
          data.id = id
          setCookiesUserPrivate(data)
          commit('USER_SUCCESS', data)
          resolve(data)
        })
        .catch(err => {
          dispatch("userAuthentication/logout", null, {root: true});
          commit('USER_ERROR');
          reject(err)
        })
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
            reject(err.response.data)

          })
    })
  },

  validateEmail: ({commit}, payload) => {
    return new Promise((resolve, reject) => {
      sendUserAuthentication.ValidateEmail(payload)
      .then(resp => {

        commit('VALID_EMAIL_SUCCESS')
        resolve(resp.data)

      })
      .catch(err => {

        commit('VALID_EMAIL_ERROR')
        reject(err.response.data)

      })
    })
  },

  resendEmailValidation: ({commit}) => {
    return new Promise((resolve, reject) => {
      sendUserAuthentication.ResendValidateEmail(state.user_private.id)
      .then(resp => {

        commit('RESEND_EMAIL_SUCCESS')
        resolve(resp.data)

      })
      .catch(err => {

        commit('RESEND_EMAIL_ERROR')
        reject(err.response.data)

      })
    })
  },

  updateProfile: ({commit}, data) => {
    return new Promise((resolve, reject) => {
      if ( state.user_private.type==='business'){
        manageUserProfile.updateBusiness(state.user_private.id, data)
        .then(resp => {
          commit('USER_UPDATE', resp.data)
          resolve(resp.data)

        })
        .catch(err => {

          commit('BUSINESS_UPDATE_ERROR')
          reject(err.response.data)

        })
      }
      else{
        manageUserProfile.updateUser(state.user_private.id, data)
        .then(resp => {
          commit('USER_UPDATE', resp.data)
          resolve(resp.data)

        })
        .catch(err => {

          commit('USER_UPDATE_ERROR')
          reject(err.response.data)

        })
      }
    })
  },

  addProdCart: ({commit}, product) => {

    commit('ADD_PROD_CART', product)
  },

  deleteProdCart: ({commit}, item) => {
    commit('DEL_PROD_CART', item)
  },

  addMenuCart: ({commit}, menu) => {
    commit('ADD_MENU_CART', menu)
  },

  deleteMenuCart: ({commit}, item) => {
    commit('DEL_MENU_CART', item)
  },

  resetItemInCart: ({commit}) => {
      commit('RESET_CART')
  }

}

const mutations = {

  USER_UPDATE: (state, data) => {
    state.user_private.avatar = data.avatar
    state.user_private.email_activated = data.email_activated

    state.user.Username = data.username
    state.user.Email = data.email
    state.user.Nome = data.first_name
    state.user.Cognome = data.last_name
    state.user.Anno_di_Nascita = data.birth_date
    state.user.Numero_di_Telefono = data.phone


    if (state.user_private.type === 'business')
    {
      state.user.Codice_Fiscale = data.cf
      state.user.Indirizzo = data.address
      state.user.N_civ = data.n_civ
      state.user.Citta = data.city
      state.user.Cap = data.cap
    }
  },

  USER_UPDATE_ERROR: (state) => {
  },

  BUSINESS_UPDATE: (state) => {
  },

  BUSINESS_UPDATE_ERROR: (state) => {
  },

  RESEND_EMAIL_SUCCESS: () => {
  },

  RESEND_EMAIL_ERROR: () => {
  },

  VALID_EMAIL_SUCCESS: (state) => {
    state.user_private.email_activated = true
  },
  VALID_EMAIL_ERROR: (state) => {
    state.user_private.email_activated = false
  },

  USER_REQUEST: (state) => {
    state.status = 'loading'
  },

  USER_SUCCESS: (state, data) => {
    state.status = 'success'
    state.user_private.type = data.type
    state.user_private.id = data.id
    state.user_private.is_superuser = data.is_superuser
    state.user_private.avatar = data.avatar
    state.user_private.email_activated = data.email_activated

    state.user.Username = data.username
    state.user.Email = data.email
    state.user.Nome = data.first_name
    state.user.Cognome = data.last_name
    state.user.Anno_di_Nascita = data.birth_date
    state.user.Numero_di_Telefono = data.phone


    if (state.user_private.type === 'business')
    {
      state.user.Codice_Fiscale = data.cf
      state.user.Indirizzo = data.address
      state.user.N_civ = data.n_civ
      state.user.Citta = data.city
      state.user.Cap = data.cap
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

  ADD_PROD_CART: (state, prod) => {
      let adding_prod = false;
        if (state.cart.selected_items.length>0) {
            let arrayLength = state.cart.selected_items.length;
            for (let i = 0; i < arrayLength; i++) {
                if (prod.id === state.cart.selected_items[i].product.id){
                    state.cart.selected_items[i].quantity += 1;
                    adding_prod = true;
                    break;
                }
            }
        }
        if(!adding_prod) {
            let itemInCart = {
                'product': prod,
                'quantity': 1,
            };
            state.cart.selected_items.push(itemInCart);
        }
  },

  DEL_PROD_CART: (state, item) => {
        state.cart.selected_items[state.cart.selected_items.indexOf(item)].quantity -= 1;

        if (state.cart.selected_items[state.cart.selected_items.indexOf(item)].quantity === 0)
              state.cart.selected_items.splice(state.cart.selected_items.indexOf(item), 1);
  },

  ADD_MENU_CART: (state, menu) => {
        let adding_menus = false;
        if (state.cart.selected_menus.length>0) {
            let arrayLength = state.cart.selected_menus.length;
            for (let i = 0; i < arrayLength; i++) {
                if (menu.id === state.cart.selected_menus[i].menu.id){
                    state.cart.selected_menus[i].quantity += 1;
                    adding_menus = true;
                    break;
                }
            }
        }
        if(!adding_menus) {
            let itemInCart = {
                'menu': menu,
                'quantity': 1,
            };
            state.cart.selected_menus.push(itemInCart);
        }
  },

  DEL_MENU_CART: (state, item) => {
        state.cart.selected_menus[state.cart.selected_menus.indexOf(item)].quantity -= 1;

        if (state.cart.selected_menus[state.cart.selected_menus.indexOf(item)].quantity === 0)
              state.cart.selected_menus.splice(state.cart.selected_menus.indexOf(item), 1);
  },

  RESET_CART: (state) => {
      state.cart = {
          selected_items: [],
          selected_menus: [],
      }
  }



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
    user_private['email_activated'] = data.email_activated
    user_private['avatar'] = data.avatar
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