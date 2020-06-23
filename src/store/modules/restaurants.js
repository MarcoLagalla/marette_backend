/* eslint-disable no-unused-vars */
import manageRestaurant from "../../services/manageRestaurant";

const state = {
    status: '',
    errors: [],
    id_restaurant: '',
    list: [],
    userList: [],
    autocomplete: {},
}

const getters = {
    restaurantList: state => state.list,
    errors: state => state.errors,
    userList: state => state.userList,
    autocomplete: state => state.autocomplete,

}

const actions = {
    newRestaurant: ({commit, dispatch}, restaurant) => {
        return new Promise((resolve, reject) => {
            commit('REG_REST_REQUEST')
            manageRestaurant.postRegisterRestaurant(restaurant)
            .then(resp => {
                const data = resp.data
                commit('REG_REST_SUCCESS', data.id_restaurant)
                dispatch("userProfile/addRestaurant", data.id_restaurant, {root: true});
                resolve(resp.data)
            })
            .catch(err => {
                commit('REG_REST_ERROR', err.response)
                reject(err.response.data)
            })
        })
    },

    getRestaurants: ({commit}, payload) => {
        return new Promise((resolve, reject) => {
            if (Object.prototype.hasOwnProperty.call(payload, 'page_size')){
                setPageSizeCookie(payload.page_size)
            }
            else{
                payload.page_size = getPageSizeCookie()
            }

            manageRestaurant.getRestaurantList(payload)
            .then(resp => {
                const data = resp.data
                commit('REST_LIST_SUCCESS', data)
                resolve(resp)
            })
            .catch(err => {
                commit('REST_LIST_ERROR')
                reject(err)
            })
        })
    },

    searchRestaurants: ({commit}, payload) => {
        return new Promise((resolve, reject) => {
            if (Object.prototype.hasOwnProperty.call(payload, 'page_size')){
                setPageSizeCookie(payload.page_size)
            }
            else{
                payload.page_size = getPageSizeCookie()
            }
            manageRestaurant.searchRestaurantList(payload)
            .then(resp => {
                const data = resp.data
                commit('REST_LIST_SUCCESS', data)
                resolve(resp)
            })
            .catch(err => {
                commit('REST_LIST_ERROR')
                reject(err)
            })
        })
    },

    updateRestaurant: ({commit, rootGetters}, data) => {
        return new Promise((resolve, reject) => {
            var id = rootGetters["restaurantData/id"];
            manageRestaurant.updateRestaurantData(id, data)
            .then(resp => {
                const data = resp.data
                commit('REST_UPDATE_SUCCESS', data)
                resolve(resp)
            })
            .catch(err => {
                commit('REST_UPDATE_ERROR')
                reject(err.response.data)
            })
        })
    },

    getUserRestaurants: ({commit, rootGetters}) => {
        return new Promise((resolve, reject) => {
            commit('REST_USR_LIST_REQUEST')
            var restaurants = rootGetters["userProfile/restaurants"];

            if (restaurants) {
                restaurants.forEach((restaurantID) => {
                    manageRestaurant.getRestaurantData(restaurantID).then(resp => {
                        const data = resp.data
                        commit('REST_USR_LIST_ADD', data)

                    })
                      .catch(err => {
                          commit('REST_USR_LIST_ERROR')
                          reject(err)
                      })
                })
            }
            resolve(state.userList)

        })
    },

    getAutocomplete: ({commit}) =>{
         return new Promise((resolve, reject) => {
             manageRestaurant.getAutocomplete()
                 .then(respRes => {
                    commit('REST_AUTOCOMPLETE', respRes.data)
                 })
         })
    },


}

const mutations = {

    REST_AUTOCOMPLETE: (state, autocomplete) => {
        state.autocomplete = autocomplete
    },

    REST_USR_LIST_REQUEST: (state) => {
        state.userList = []
    },

    REST_USR_LIST_ADD: (state, rest) => {
        state.userList.push(rest)
    },

    REST_USR_LIST_ERROR: (state, rest) => {
        state.userList.push(rest)
    },

    REG_REST_REQUEST: (state) => {
        state.status = 'loading'
    },
    REG_REST_SUCCESS: (state, id_restaurant) => {
        state.status = 'success'
        state.id_restaurant = id_restaurant
    },
    REG_REST_ERROR: (state, error) => {
        state.status = 'error'
        state.errors = error.data
    },
    REST_LIST_SUCCESS: (state, list) => {
        state.list = list
    },
    REST_LIST_ERROR: (state) => {
        state.status = 'error_list'
    },
    REST_UPDATE_SUCCESS: () => {
    },
    REST_UPDATE_ERROR: () => {
    },

}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}

function setPageSizeCookie(page_size) {
  var d = new Date();
  var exdays = 364;
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  var expires = "expires="+ d.toUTCString();
    document.cookie = "page_size=" + page_size + ";" + expires + " ; SameSite=Lax ; Secure ; path=/";
}

function getPageSizeCookie() {
  var name = "page_size=";
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
  return 10;
}
