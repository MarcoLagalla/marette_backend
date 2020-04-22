
<script>
  // Extensions
  import View from '@/views/View'

  // Mixins
  import LoadSections from '@/mixins/load-sections'

  export default {
    name: 'rest1',

    metaInfo: { title: 'Login' },

    extends: View,

    mixins: [
      LoadSections([
        'rest-banner',
        'rest-menu',
        //'rest-events',
        //'rest-map',
        'info',
      ]),
    ],

    props: {
      id: {
        type: String,
        default: 'login',
      },
    },
  }
</script>
