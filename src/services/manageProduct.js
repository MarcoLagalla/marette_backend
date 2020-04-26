import api from '@/services/api'

export default {
    getProductList(payload) {
        return api.get('v1/webapp/restaurant/'+ payload + '/products')
            .then(response => {
                return response
            })
    }
}