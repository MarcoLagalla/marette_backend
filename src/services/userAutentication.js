import api from '@/services/api'

export default {
  postRegisterUser(payload) {
    return api.post('/v1/account/customer', payload)
              .then(response => response.data)
  }
}