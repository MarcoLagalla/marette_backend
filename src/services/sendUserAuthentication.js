
import api from '@/services/api'

export default {
  postRegisterUser(payload) {
    return api.post(`v1/account/customer`, payload)
          .then(response => {
            api.defaults.headers.common['Authorization'] = 'Token ' + response.data.token
            return response
          })
  },

  postRegisterBusiness(payload) {
    return api.post(`v1/account/business`, payload)
          .then(response => {
            api.defaults.headers.common['Authorization'] = 'Token ' + response.data.token
            return response
          })
  },

  signUser(payload) {
    return api.post('v1/account/login', payload)
        .then(response => {
            api.defaults.headers.common['Authorization'] =  'Token ' + response.data.token
            return response
          })

  },

  logout() {
    return api.post('v1/account/logout')
        .then(response => {
            delete api.defaults.headers.common['Authorization']
            return response
        })
  },

  AskPasswordreset(data){
        return api.post('v1/account/password/reset', data)
            .then(response => {
                return response
            })
    },

  ConfirmPasswordreset(data){
    return api.post('v1/account/password/reset/confirm', data)
      .then(response => {
        return response
      })
  },

  ValidateEmail(payload){
    return api.get('v1/account/activate/' + payload.id + '/' + payload.token)
      .then(response => {
        return response
      })
  },

  ResendValidateEmail(payload){
    return api.post('v1/account/activate/resend/' + payload)
      .then(response => {
        return response
      })
  },
}