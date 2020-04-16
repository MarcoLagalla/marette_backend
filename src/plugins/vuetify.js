import Vue from 'vue';
import Vuetify from 'vuetify/lib';

Vue.use(Vuetify, {
  theme: {
    primary: '#CBAA5C',
    secondary: '#083759',
    options: {
      customProperties: true,
    },
  },
  iconfont: 'mdi'
});

export default new Vuetify({
});
