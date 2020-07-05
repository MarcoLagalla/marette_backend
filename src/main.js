import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './plugins'
import vuetify from './plugins/vuetify';
import api from '@/services/api'
import SweetModal from 'sweet-modal-vue/src/plugin.js'
Vue.use(SweetModal)
import x5GMaps from 'x5-gmaps'

import PictureInput from "vue-picture-input";

Vue.use(x5GMaps, 'AIzaSyADeNZHXA5OfUA2DtSs7SA3fh4s7rhX_gA')

Vue.config.productionTip = false

delSessionid()
var token = getToken();
var id = getID();


if (token && id) { //voglio caricarli solo se li ho entrambi
  api.defaults.headers.common['Authorization'] = 'Token ' + token;
  store.dispatch("userProfile/getUserData", id);
}

Vue.component('PictureInput', PictureInput);
const newPictureInput = Vue.component('PictureInput').extend({
  methods: {
    preloadImage (source, options) {
      console.log("questo picture input ha l'header modificato")
      // ie 11 support
      let File = window.File
      try {
        new File([], '') // eslint-disable-line
      } catch (e) {
        File = class File extends Blob {
          constructor (chunks, filename, opts = {}) {
            super(chunks, opts)
            this.lastModifiedDate = new Date()
            this.lastModified = +this.lastModifiedDate
            this.name = filename
          }
        }
      }
      options = Object.assign({}, options)
      if (typeof source === 'object') {
        this.imageSelected = true
        this.image = ''
        if (this.supportsPreview) {
          this.loadImage(source, true)
        } else {
          this.$emit('prefill')
        }
        return
      }
      var proxyUrl = 'https://cors-anywhere.herokuapp.com/'

      let headers = new Headers()
      headers.append('Origin', 'https://marette.ovh')
      headers.append('Accept', 'image/*')
      headers.append('Access-Control-Allow-Origin', 'https://marette.ovh/')
      headers.append('Access-Control-Allow-Credentials', 'true')
      headers.append('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
      headers.append('Access-Control-Allow-Headers', 'Accept,Authorization,Cache-Control,Content-Type,DNT,If-Modified-Since,Keep-Alive,Origin,User-Agent,X-Requested-With')
      headers.append('Host', 'https://marette.ovh')
      fetch(proxyUrl + source, {
        method: 'GET',
        mode: 'cors',
        headers: headers
      }).then(response => {
        return response.blob()
      })
      .then(imageBlob => {
        let e = { target: { files: [] } }
        const fileName = options.fileName || source.split('/').slice(-1)[0]
        let mediaType = options.mediaType || ('image/' + (options.fileType || fileName.split('.').slice(-1)[0]))
        mediaType = mediaType.replace('jpg', 'jpeg')
        e.target.files[0] = new File([imageBlob], fileName, { type: mediaType })
        this.onFileChange(e, true)
      })
      .catch(err => {
        this.$emit('error', {
          type: 'failedPrefill',
          message: 'Failed loading prefill image: ' + err
        })
      })
    }
  }
});

Vue.component('newPictureInput', newPictureInput);

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')


function getID() {
 var result = document.cookie.match(new RegExp('user_private' + '=([^;]+)'));
 result && (result = JSON.parse(result[1]));
 return result ? result.id : '';
}

function getToken() {
 var result = document.cookie.match(new RegExp('user-token' + '=([^;]+)'));
 result && (result = result[1]);
 return result ? result : '';
}

function delSessionid() {
  var user = getCookie("sessionid");
  if (user !== "") {
    document.cookie = "sessionid=; expires=Thu, 01 Jan 1970 00:00:00 UTC; SameSite=Lax ; Secure ; path=/;";
  }
}

function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}


