/* eslint-disable no-unused-vars */
import manageProduct from "../../services/manageProduct";
import manageRestaurant from "../../services/manageRestaurant";

const state = {
    ID: 1,
    productList: {},
    restData: {},
    status: '',
    tags:[],
    discounts:[],
    menus: [],

    FOOD_CATEGORY_CHOICES : [
        'Altro',
        'Antipasto',
        'Contorno',
        'Dessert',
        'Caffetteria',
        'Panetteria',
        'Panini e Piadine',
        'Pizza',
        'Primo',
        'Secondo',
        'Snack'
    ],

    DISCOUNT_TYPE_CHOICES : [
        'Fisso',
        'Percentuale'
    ],


}

const getters = {
    food_category_choice: state => state.food_category_choice,
    discount_type_choices: state => state.DISCOUNT_TYPE_CHOICES,
    productList: state => state.productList,
    components: state => state.restData.components,
    restData: state => state.restData,
    tags: state => state.tags,
    discounts: state => state.discounts,
    id: state => state.ID,
    menus: state => state.menus,
    slug: state => state.restData.slug,

}

const actions = {
    activateComponent: ({commit}, componentName) =>{
         return new Promise((resolve, reject) => {
             var payload = {id: state.ID, component: componentName}
             manageRestaurant.activateComponent(payload)
                 .then(respRes => {
                    commit('REST_ADD_COMPONENT', componentName)
                 })
         })

    },
    deactivateComponent: ({commit}, componentName) =>{
         return new Promise((resolve, reject) => {
             var payload = {id: state.ID, component: componentName}
             manageRestaurant.deactivateComponent(payload)
                 .then(respRes => {
                    commit('REST_RMV_COMPONENT', componentName)
                 })
         })

    },
    getRestaurantData: ({commit}, restaurantID) => {
        return new Promise((resolve, reject) => {
            commit('REST_DATA_REQUEST', restaurantID)
            manageRestaurant.getRestaurantData(restaurantID)
            .then(respRes => {
                const dataRes = respRes.data

                commit('REST_DATA_SUCCESS', dataRes)

                commit('REST_MENU_REQUEST', restaurantID)

                manageProduct.getProductList(restaurantID)
                .then(respMenu => {
                    commit('REST_MENU_SUCCESS', respMenu.data)
                    resolve(respRes.data.components)
                })
                .catch(err => {
                    commit('REST_MENU_ERROR', err.response)
                    reject(err.response)
                })
            })
            .catch(err => {
                commit('REST_DATA_ERROR', err.response)
                reject(err.response)
            })
        })
    },



    addProduct: ({commit}, product) => {
        return new Promise((resolve, reject) => {

            var payload = {}
            payload['id'] = state.ID
            payload['data'] = product
            console.log(product)

            manageProduct.addProduct(payload)
            .then(resp => {
                commit('REST_ADD_PROD_SUCCESS')
                resolve(resp)
            })
            .catch(err => {
                commit('REST_ADD_PROD_ERROR')
                reject(err)
            })
        })
    },

    getListTag: ({commit}) => {
        return new Promise((resolve, reject) => {

            manageProduct.listTags()
            .then(resp => {
                commit('LIST_TAGS_SUCCESS', resp.data)
                console.log(resp)
                resolve(resp.data)
            })
            .catch(err => {
                commit('LIST_TAGS_ERROR')
                reject(err)
            })
        })
    },

    getListDiscounts: ({commit}) => {
        return new Promise((resolve, reject) => {

            manageProduct.listDiscounts(state.ID)
            .then(resp => {
                commit('LIST_DISCOUNTS_SUCCESS', resp.data)
                console.log(resp.data)
                resolve(resp.data)
            })
            .catch(err => {
                commit('LIST_DISCOUNTS_ERROR')
                reject(err)
            })
        })
    },
    addDiscount: ({commit}, discount) => {
        return new Promise((resolve, reject) => {


            manageProduct.addDiscount(discount, state.ID)
            .then(resp => {
                commit('ADD_DISCOUNT_SUCCESS', resp.data);
                console.log(resp);
                resolve(resp.data)
            })
            .catch(err => {
                commit('ADD_DISCOUNT_ERROR');
                reject(err)
            })
        })
    },

    addMenuEntry: ({commit}, portata) => {
        return new Promise((resolve, reject) => {
            var payload = {
                    data: {
                      name: portata.data.name,
                      num_products: portata.data.num_products,
                      products: []
                    },
                    restId: state.ID,
                    menuId: portata.menuId
                }
                portata.data.products.forEach(function (item) {
                    payload.data.products.push(item.id)
                });
            manageRestaurant.addMenuEntry(payload)
            .then(resp => {
                commit('ADD_PORTATA_SUCCESS', portata);
                resolve(resp.data)
            })
            .catch(err => {
                commit('ADD_PORTATA_ERROR');
                reject(err)
            })
        })
    },

    deleteMenuEntry: ({commit}, data) => {
        return new Promise((resolve, reject) => {

            data.restId =  state.ID
            manageRestaurant.deleteMenuEntry(data)
            .then(resp => {
                commit('RMV_PORTATA_SUCCESS', resp.data);
                resolve(resp.data)
            })
            .catch(err => {
                commit('RMV_PORTATA_ERROR');
                reject(err)
            })
        })
    },

    editMenuEntry: ({commit}, data) => {
        return new Promise((resolve, reject) => {

            data.restId =  state.ID
            manageRestaurant.editMenuEntry(data)
            .then(resp => {
                commit('EDIT_PORTATA_SUCCESS', resp.data);
                resolve(resp.data)
            })
            .catch(err => {
                commit('EDIT_PORTATA_ERROR');
                reject(err)
            })
        })
    },

    addMenu: ({commit}, menu) => {
        return new Promise((resolve, reject) => {

            const payload = {id: state.ID, data: menu}
            manageRestaurant.addMenu(payload)
            .then(resp => {
                commit('ADD_MENU_SUCCESS', resp.data);
                resolve(resp.data)
            })
            .catch(err => {
                commit('ADD_MENU_ERROR');
                reject(err)
            })
        })
    },

    editMenu: ({commit}, menu) => {
        return new Promise((resolve, reject) => {

            const payload = {restId: state.ID, data: menu.data, menuId: menu.menuId}
            manageRestaurant.editMenu(payload)
            .then(resp => {
                commit('EDIT_MENU_SUCCESS', menu);
                resolve(resp.data)
            })
            .catch(err => {
                commit('EDIT_MENU_ERROR');
                reject(err)
            })
        })
    },

    deleteMenu: ({commit}, menu) => {
        return new Promise((resolve, reject) => {
            const payload = {restId: state.ID, menuId: menu.id}
            manageRestaurant.deleteMenu(payload)
            .then(resp => {
                commit('RMV_MENU_SUCCESS', resp.data);
                resolve(menu)
            })
            .catch(err => {
                commit('RMV_MENU_ERROR');
                reject(err)
            })
        })
    },

    listMenus: ({commit}) => {
        return new Promise((resolve, reject) => {

            manageRestaurant.listMenus(state.ID)
            .then(resp => {
                commit('LIST_MENU_SUCCESS', resp.data);
                resolve(resp.data)
            })
            .catch(err => {
                commit('LIST_MENU_ERROR');
                reject(err)
            })
        })
    },
}

const mutations = {
    RMV_PORTATA_SUCCESS: () =>{
    },

    RMV_PORTATA_ERROR: () =>{
    },

    EDIT_PORTATA_SUCCESS: () =>{
    },

    EDIT_PORTATA_ERROR: () =>{
    },

    ADD_PORTATA_SUCCESS: (state, data) =>{
        state.menus.forEach( (menu) =>{
          if (menu.id === data.menuId)
            state.menus[state.menus.indexOf(menu)].entries.push(data.data)
        });
    },

    ADD_PORTATA_ERROR: () =>{
    },

    ADD_MENU_SUCCESS: (stete, menu) =>{
        stete.menus.push(menu)
    },

    ADD_MENU_ERROR: () =>{
    },

    EDIT_MENU_SUCCESS: (state, newMenu) =>{
        state.menus.forEach( (menu) =>{
          if (menu.id === newMenu.id)
            state.menus[state.menus.indexOf(menu)] = newMenu
        });
    },

    EDIT_MENU_ERROR: () =>{
    },

    RMV_MENU_SUCCESS: (state, menu) =>{
      state.menus.splice(state.menus.indexOf(menu), 1)
    },

    RMV_MENU_ERROR: () =>{
    },

    LIST_MENU_SUCCESS: (state, menus) =>{
        state.menus = menus
    },

    LIST_MENU_ERROR: () =>{
    },

    REST_ADD_PROD_SUCCESS: () =>{
    },

    REST_ADD_PROD_ERROR: () =>{
    },

    REST_RMV_COMPONENT: (state, componentName) =>{
        state.restData.components[componentName].show=false;
    },

    REST_ADD_COMPONENT: (state, componentName) =>{
        state.restData.components[componentName].show=true;
    },

    REST_DATA_REQUEST: (state, ID) => {
        state.status = 'loading'
        state.ID = ID
    },

    REST_DATA_SUCCESS: (state, data) =>{
        state.restData = data
    },

    REST_MENU_REQUEST: (state) => {
        state.status = 'loading'
    },

    REST_MENU_SUCCESS: (state, data) => {
        state.status = 'success'
        state.productList = data
    },

    REST_MENU_ERROR: (state, error) => {
        state.status = 'error'
        state.error = error
    },

    REST_DATA_ERROR: (state, error) => {
        state.status = 'error'
        state.error = error
    },

    LIST_TAGS_SUCCESS: (state, data) => {
        state.status = 'success'
        state.tags = data
    },

    LIST_TAGS_ERROR: (state, error) => {
        state.status = 'error'
        state.error = error
    },

    LIST_DISCOUNTS_SUCCESS: (state, data) => {
        state.status = 'success'
        state.discounts = data
    },

    LIST_DISCOUNTS_ERROR: (state, error) => {
        state.status = 'error'
        state.error = error
    },

    ADD_DISCOUNT_SUCCESS: (state, data) => {
        state.status = 'success'
        state.discounts = state.discounts + data
    },

    ADD_DISCOUNT_ERROR: (state, error) => {
        state.status = 'error'
        state.error = error
    },


}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}


