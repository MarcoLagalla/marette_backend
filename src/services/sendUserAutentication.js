import api from '@/services/api'

export default {
  postRegisterUser(payload) {
    return api.post(`v1/account/customer`, payload)
          .then(response => response)
  },
  signUser(payload) {
    return api.post('v1/account/login', payload)
        .then(response => response)

  },
  logout() {
    return api.post('v1/account/logout')
        .then(response => response)

  }
}