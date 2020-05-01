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

}