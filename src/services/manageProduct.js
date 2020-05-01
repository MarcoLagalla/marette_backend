import api from '@/services/api'

export default {
    getProductList(payload) {
        return api.get('v1/webapp/restaurant/'+ payload + '/products')
            .then(response => {
                return response
            })
    },

    addProduct(payload) {
        const config = {
            headers: {
              'content-type': 'multipart/form-data'
            }
        };
        return api.post('v1/webapp/restaurant/' + payload['id'] + '/products/add', payload['data'], config)
            .then(response => {
                return response
            })
    },

}