<script>
  // Extensions
  import View from '@/views/View'

  // Mixins
  import LoadSections from '@/mixins/load-sections'

  export default {
    name: 'NewRestaurant',

    metaInfo: { title: 'NewRestaurant' },

    extends: View,

    mixins: [
      LoadSections([
        'NewRestaurant',
        'info',
      ]),
    ],

    props: {
      id: {
        type: String,
        default: 'newRestaurant',
      },
    },
  }
</script>