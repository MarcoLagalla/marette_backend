<script>
// Extensions
import View from '@/views/View'

// Mixins
import LoadSections from '@/mixins/load-sections'

export default {
  name: 'About',

  metaInfo: {
    title: 'About Us'
  },

  extends: View,

  mixins: [
    LoadSections([
      'chisiamo',
      'info',
    ]),
  ],

  props: {
    id: {
      type: String,
      default: 'about',
    },
  },
}
</script>
