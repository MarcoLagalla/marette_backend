<script>
  // Extensions
  import View from '@/views/View'

  // Mixins
  import LoadSections from '@/mixins/load-sections'

  export default {
    name: 'Login',

    metaInfo: { title: 'Login' },

    extends: View,

    mixins: [
      LoadSections([
        'logform',
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
