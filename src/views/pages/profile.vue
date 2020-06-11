<script>
// Extensions
import View from '@/views/View'

// Mixins
import LoadSections from '@/mixins/load-sections'

export default {
  name: 'Profile',

  metaInfo: {
    title: 'Profile'
  },

  extends: View,

  mixins: [
    LoadSections([
      'BannerValidateEmail',
      'Profile',
      'NewRestaurant',
    ]),
  ],

  props: {
    id: {
      type: String,
      default: 'profile',
    },
  },
}
</script>
