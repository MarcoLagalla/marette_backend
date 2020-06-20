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

    updateProduct(payload) {
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


    removeProduct(payload){
        return api.post('v1/webapp/restaurant/' + payload['id'] + '/products/'+ payload['p_id']+ '/delete', payload)
                    .then(response => {
                return response
            })
    },

    listTags(){
                return api.get('v1/webapp/restaurant/product/tags')
            .then(response => {
                return response
            })
    },

    listDiscounts(id){
                return api.get('v1/webapp/restaurant/' + id + '/products/discounts')
            .then(response => {
                return response
            })
    },

    addNewDiscount(discount, id){
                    return api.post('v1/webapp/restaurant/' + id + '/products/discounts/add', discount)
            .then(response => {
                return response
            })
    },

    addNewDiscountToProduct(payload, id){

        return api.post('v1/webapp/restaurant/' + id + '/products/' + payload.id + '/setdiscounts', payload.discounts)
            .then(response => {
                return response
            })
    }

}