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
    restCategories: [],
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
    productList: state => state.productList,
    restCategories: state => state.restCategories,
    components: state => state.restData.components,
    restData: state => state.restData,
    openingDays: state => state.restData.openingDays,
    tags: state => state.tags,
    discounts: state => state.discounts,
    id: state => state.ID,
    menus: state => state.menus,
    slug: state => state.restData.slug,
    home: state => state.restData.components.home,
    galleria: state => state.restData.components.galleria,

}

const actions = {
    getRestCategories: ({commit}) =>{
         return new Promise((resolve, reject) => {
             manageRestaurant.getRestCategories()
                 .then(respRes => {
                    commit('REST_CATEGORIES', respRes.data)
                 })
         })
    },


    addOpeningDays: ({commit}, day) =>{
         return new Promise((resolve, reject) => {
             manageRestaurant.addOpeningDay({restId: state.ID, data: {day: day, restaurant: state.ID}})
             .then(respRes => {
                  respRes.data.day = day
                commit('REST_ADD_OP_DAY', respRes.data)
                 resolve()
             })


         })
    },


    addTimeInterval: ({commit}, payload) =>{
         return new Promise((resolve, reject) => {
             payload.data.restaurant = state.ID
             manageRestaurant.addTimeInterval({restId: state.ID, data: payload.data, dayId: payload.day.id})
             .then(respRes => {
                  respRes.day = payload.day
                commit('REST_ADD_TIME_INT', respRes)
                 resolve()
             })


         })
    },


    removeTimeInterval: ({commit}, payload) =>{
         return new Promise((resolve, reject) => {
             manageRestaurant.removeTimeInterval({restId: state.ID, timeId: payload.time.id, dayId: payload.day.id})
             .then(respRes => {
                commit('REST_RMV_TIME_INT', payload)
                 resolve()
             })


         })
    },


    removeOpeningDay: ({commit}, day) =>{
         return new Promise((resolve, reject) => {
             var payload = {restId: state.ID, day: day.id}
             manageRestaurant.removeOpeningDay(payload)
             .then(respRes => {
                commit('REST_RMV_OP_DAY', day)
                 resolve()
             })


         })
    },

    getTimeTable: ({commit}) =>{
         return new Promise((resolve, reject) => {
             manageRestaurant.getTimeTable(state.ID)
                 .then(respRes => {
                    commit('REST_GET_TIME_TABS', respRes.data)
                 })
         })
    },

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

    editHomeComponent: ({commit}, data) =>{
         return new Promise((resolve, reject) => {
             var payload = {restId: state.ID, data: data}
             manageRestaurant.editHomeComponent(payload)
                 .then(respRes => {
                    commit('MOD_HOME_COMPONENT', respRes.data)
                     resolve(respRes.data)
                 })
         })
    },

    addGalleryImage: ({commit}, data) =>{
         return new Promise((resolve, reject) => {
             var payload = {restId: state.ID, data: data}
             manageRestaurant.addGalleryImage(payload)
                 .then(respRes => {
                    commit('ADD_GALLERY_IMG', respRes.data)
                     resolve(respRes.data)
                 })
         })
    },

    removeGalleryImage: ({commit}, imageId) =>{
         return new Promise((resolve, reject) => {
             var payload = {restId: state.ID, imageId: imageId}
             manageRestaurant.deleteGalleryImage(payload)
                 .then(respRes => {
                    commit('RMV_GALLERY_IMG', imageId)
                     resolve(respRes.data)
                 })
         })
    },

    editGalleryImage: ({commit}, payload) =>{
         return new Promise((resolve, reject) => {
             payload.restId= state.ID
             manageRestaurant.editGalleryImage(payload)
                 .then(respRes => {
                    commit('EDIT_GALLERY_IMG', respRes.data)
                     resolve(respRes.data)
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

                manageRestaurant.getTimeTable(restaurantID)
                 .then(respRes => {
                    commit('REST_GET_TIME_TABS', respRes.data)
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

            let payload = {};
            payload['id'] = state.ID;
            payload['data'] = product;
            manageProduct.addProduct(payload)
            .then(resp => {
                commit('REST_ADD_PROD_SUCCESS', resp.data);
                resolve(resp)
            })
            .catch(err => {
                commit('REST_ADD_PROD_ERROR');
                reject(err)
            })
        })
    },

    updateProduct: ({commit}, product) => {
        return new Promise((resolve, reject) => {

            let payload = {};
            payload['id'] = state.ID;
            payload['data'] = product;
            manageProduct.updateProduct(payload)
            .then(resp => {
                commit('REST_ADD_PROD_SUCCESS', resp.data);
                resolve(resp)
            })
            .catch(err => {
                commit('REST_ADD_PROD_ERROR');
                reject(err)
            })
        })
    },

    removeProduct: ({commit}, product_id) => {
        return new Promise((resolve, reject) => {
            let payload = {id: state.ID, p_id: product_id};
            manageProduct.removeProduct(payload)
            .then(resp => {
                commit('REST_REMOVE_PROD_SUCCESS', resp.data)
                resolve(resp.data)
            })
            .catch(err => {
                commit('REST_REMOVE_PROD_ERROR');
                reject(err.response.data)
            })
        })
    },

    getListTag: ({commit}) => {
        return new Promise((resolve, reject) => {

            manageProduct.listTags()
            .then(resp => {
                commit('LIST_TAGS_SUCCESS', resp.data)
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
                resolve(resp.data)
            })
            .catch(err => {
                commit('LIST_DISCOUNTS_ERROR')
                reject(err)
            })
        })
    },
    addNewDiscount: ({commit}, discount) => {
        return new Promise((resolve, reject) => {


            manageProduct.addNewDiscount(discount, state.ID)
            .then(resp => {
                commit('ADD_DISCOUNT_SUCCESS', resp.data);
                resolve(resp.data)
            })
            .catch(err => {
                commit('ADD_DISCOUNT_ERROR');
                reject(err)
            })
        })
    },

    addDiscountToProduct: ({commit}, payload) => {
        return new Promise((resolve, reject) => {
            manageProduct.addNewDiscountToProduct(payload, state.ID)
            .then(resp => {
                commit('ADD_DISCOUNT_TO_PRODUCT_SUCCESS', resp.data);
                resolve(resp.data)
            })
            .catch(err => {
                commit('ADD_DISCOUNT_TO_PRODUCT_ERROR');
                reject(err.response.data)
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
                portata.data.id = resp.data.id
                commit('ADD_PORTATA_SUCCESS', portata);
                resolve(resp.data)
            })
            .catch(err => {
                commit('ADD_PORTATA_ERROR');
                reject(err.response.data)
            })
        })
    },

    deleteMenuEntry: ({commit}, data) => {
        return new Promise((resolve, reject) => {

            data.restId =  state.ID
            manageRestaurant.deleteMenuEntry(data)
            .then(resp => {
                commit('RMV_PORTATA_SUCCESS', data);
                resolve(resp.data)
            })
            .catch(err => {
                commit('RMV_PORTATA_ERROR');
                reject(err.response.data)
            })
        })
    },

    editMenuEntry: ({commit}, payload) => {
        return new Promise((resolve, reject) => {

            payload.restId =  state.ID
            manageRestaurant.editMenuEntry(payload)
            .then(resp => {
                commit('EDIT_PORTATA_SUCCESS',payload);
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
                reject(err.response.data)
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
                reject(err.response.data)
            })
        })
    },

    deleteMenu: ({commit}, menu) => {
        return new Promise((resolve, reject) => {
            const payload = {restId: state.ID, menuId: menu.id}
            manageRestaurant.deleteMenu(payload)
            .then(resp => {
                commit('RMV_MENU_SUCCESS', menu);
                resolve(resp.data)
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
    REST_CATEGORIES: (state, categories) => {
        state.restCategories = categories

    },

    REST_ADD_TIME_INT: (state, payload) => {
        state.restData.openingDays[state.restData.openingDays.indexOf(payload.day)].fasce.push(payload.data)
    },

    REST_RMV_TIME_INT: (state, payload) => {
        state.restData.openingDays[state.restData.openingDays.indexOf(payload.day)].fasce.splice(state.restData.openingDays[state.restData.openingDays.indexOf(payload.day)].fasce.indexOf(payload.time), 1)
    },

    REST_GET_TIME_TABS: (state, days) => {
        state.restData.opens_at = days.opens_at
        state.restData.opened_now = days.opened_now
        state.restData.openingDays = days.timetable
    },

    REST_ADD_OP_DAY: (state, data) => {
        state.restData.openingDays.push({day: data.day, fasce: [], id: data.id})
    },

    REST_RMV_OP_DAY: (state, day) => {
        state.restData.openingDays.splice(state.restData.openingDays.indexOf(day), 1)
    },

    MOD_HOME_COMPONENT: (state, home) => {
        state.restData.components.home = home
    },

    ADD_GALLERY_IMG: (state, img) => {
        state.restData.components.galleria.immagini.push(img)
    },

    RMV_GALLERY_IMG: (state, imgId) => {
        state.restData.components.galleria.immagini.forEach((img) => {
            if (img.id === imgId)
                state.restData.components.galleria.immagini.splice(state.restData.components.galleria.immagini.indexOf(img), 1)
        });
    },

    EDIT_GALLERY_IMG: (state, newImg) => {
        state.restData.components.galleria.immagini.forEach((img) => {
            if (img.id === newImg.id)
                state.restData.components.galleria.immagini[state.restData.components.galleria.immagini.indexOf(img)] = newImg
        });
    },

    RMV_PORTATA_SUCCESS: (state, data) => {
        state.menus.forEach((menu) => {
            if (menu.id === data.menuId) {
                menu.entries.forEach((portata) => {
                    if (portata.id === data.entryId)
                        menu.entries.splice(menu.entries.indexOf(portata), 1)
                })
            }
        });
    },

    RMV_PORTATA_ERROR: () => {
    },

    EDIT_PORTATA_SUCCESS: (state, payload) => {
        state.menus.forEach((menu) => {
            if (menu.id === payload.menuId) {
                menu.entries.forEach((portata) => {
                    if (portata.id === payload.entryId) {
                        menu.entries[menu.entries.indexOf(portata)] = payload.portata
                    }
                })
            }
        });
    },

    EDIT_PORTATA_ERROR: () => {
    },

    ADD_PORTATA_SUCCESS: (state, data) => {
        state.menus.forEach((menu) => {
            if (menu.id === data.menuId)
                state.menus[state.menus.indexOf(menu)].entries.push(data.data)
        });
    },

    ADD_PORTATA_ERROR: () => {
    },

    ADD_MENU_SUCCESS: (stete, menu) => {
        stete.menus.push(menu)
    },

    ADD_MENU_ERROR: () => {
    },

    EDIT_MENU_SUCCESS: (state, newMenu) => {
        state.menus.forEach((menu) => {
            if (menu.id === newMenu.id)
                state.menus[state.menus.indexOf(menu)] = newMenu
        });
    },

    EDIT_MENU_ERROR: () => {
    },

    RMV_MENU_SUCCESS: (state, menu) => {
        state.menus.splice(state.menus.indexOf(menu), 1)
    },

    RMV_MENU_ERROR: () => {
    },

    LIST_MENU_SUCCESS: (state, menus) => {
        state.menus = menus
    },

    LIST_MENU_ERROR: () => {
    },

    REST_ADD_PROD_SUCCESS: (state, product) => {
        state.productList[product.category].push(product)
    },

    REST_ADD_PROD_ERROR: () => {
    },

    REST_REMOVE_PROD_SUCCESS: (state) => {
        state.status = 'success'

        // this.products.splice(this.products.indexOf(product), 1);
        // state.productList[product.category].splice(state.productList[product.category].product, 1)


    },

    REST_REMOVE_PROD_ERROR: () => {
    },


    REST_RMV_COMPONENT: (state, componentName) => {
        state.restData.components[componentName].show = false;
    },

    REST_ADD_COMPONENT: (state, componentName) => {
        state.restData.components[componentName].show = true;
    },

    REST_DATA_REQUEST: (state, ID) => {
        state.status = 'loading'
        state.ID = ID
    },

    REST_DATA_SUCCESS: (state, data) => {
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
        state.discounts.push(data)
    },

    ADD_DISCOUNT_ERROR: (state, error) => {
        state.status = 'error'
        state.error = error
    },

    ADD_DISCOUNT_TO_PRODUCT_SUCCESS: (state) => {
        state.status = 'success'
    },

    ADD_DISCOUNT_TO_PRODUCT_ERROR: (state, error) => {
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




