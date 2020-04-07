import api from '@/services/api'

export default {
  postRegisterUser(payload) {
    return api.post(`v1/account/customer`, payload)
          .then(response => {
            api.defaults.headers.common['Authorization'] = response.data.token
            return response
          })

  },
  signUser(payload) {
    return api.post('v1/account/login', payload)
        .then(response => {
            api.defaults.headers.common['Authorization'] = response.data.token
            return response
          })

  },
  logout() {
    return api.post('v1/account/logout')
        .then(response => response)

  }
}