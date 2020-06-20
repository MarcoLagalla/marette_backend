import api from '@/services/api'

export default {
    getUserProfile(payload) {
        return api.get('v1/account/profile/' + payload, payload)
            .then(response => {
                return response
            })
    },

    changePassword(id, data) {
        return api.put('v1/account/password/' + id + '/change', data)
            .then(response => {
                api.defaults.headers.common['Authorization'] = 'Token ' + response.data.token
                return response
            })
    },

    updateUser(id, data) {
        return api.post('v1/account/profile/' + id + '/customer/update', data)
            .then(response => {
                return response
            })
    },

    updateBusiness(id, data) {
        return api.post('v1/account/profile/' + id + '/business/update', data)
            .then(response => {
                return response
            })
    },
}