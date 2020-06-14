import axios from 'axios'
import Cookies from 'js-cookie'

export default axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': Cookies.get('csrftoken'),
    'Access-Control-Allow-Origin': 'https://marette.ovh'
  }
})
