import api from '@/services/api'

export default {
    postRegisterRestaurant(payload) {
        return api.post('v1/webapp/restaurant/new', payload)
            .then(response => {
                return response
            })
    },

    getRestaurantList() {
        return api.get('v1/webapp/restaurant/list')
            .then(response => {
                return response
            })
    },

    getRestaurantData(payload) {
        return api.get('v1/webapp/restaurant/' + payload)
            .then(response => {
                return response
            })
    },

    activateComponent(payload) {
        return api.post('v1/webapp/restaurant/' + payload.id + '/components/' + payload.component + '/activate')
            .then(response => {
                return response
            })
    },

    deactivateComponent(payload) {
        return api.post('v1/webapp/restaurant/' + payload.id + '/components/' + payload.component + '/deactivate')
            .then(response => {
                return response
            })
    },

    updateRestaurantData(id, data) {
        return api.post('v1/webapp/restaurant/' + id + '/update', data)
            .then(response => {
                return response
            })
    },

    addMenuEntry(payload) {
        return api.post('v1/webapp/restaurant/' + payload.restId + '/menus/' + payload.menuId + '/entry/add', payload.data)
            .then(response => {
                return response
            })
    },

    deleteMenuEntry(payload) {
        return api.post('v1/webapp/restaurant/' + payload.restId + '/menus/' + payload.menuId + '/entry/' + payload.entryId + '/delete')
            .then(response => {
                return response
            })
    },

    editMenuEntry(payload) {
        return api.post('v1/webapp/restaurant/' + payload.restId + '/menus/' + payload.menuId + '/entry/' + payload.entryId + '/edit', payload.data)
            .then(response => {
                return response
            })
    },

    addMenu(payload) {
        return api.post('v1/webapp/restaurant/' + payload.id + '/menus/add', payload.data)
            .then(response => {
                return response
            })
    },

    editMenu(payload) {
        return api.post('v1/webapp/restaurant/' + payload.restId + '/menus/' + payload.menuId + '/edit', payload.data)
            .then(response => {
                return response
            })
    },

    deleteMenu(payload) {
        return api.post('v1/webapp/restaurant/' + payload.restId + '/menus/' + payload.menuId + '/delete')
            .then(response => {
                return response
            })
    },

    listMenus(payload) {
        return api.get('v1/webapp/restaurant/' + payload + '/menus')
            .then(response => {
                return response
            })
    },

    editHomeComponent(payload) {
        return api.post('v1/webapp/restaurant/' + payload.restId + '/components/home/edit', payload.data)
            .then(response => {
                return response
            })
    },

    addGalleryImage(payload) {
        return api.post('v1/webapp/restaurant/' + payload.restId + '/components/galleria/images/add', payload.data)
            .then(response => {
                return response
            })
    },

    deleteGalleryImage(payload) {
        return api.post('v1/webapp/restaurant/' + payload.restId + '/components/galleria/images/' + payload.imageId + '/delete')
            .then(response => {
                return response
            })
    },

    editGalleryImage(payload) {
        return api.post('v1/webapp/restaurant/' + payload.restId + '/components/galleria/images/' + payload.imageId + '/edit', payload.data)
            .then(response => {
                return response
            })
    },
}