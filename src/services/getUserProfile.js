
import api from '@/services/api'

export default {
    getUserProfile(payload) {
        return api.get('v1/account/profile/' + payload, payload)
            .then(response => {
                return response
            })

    }
}