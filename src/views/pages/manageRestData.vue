<script>
// Extensions
import View from '@/views/View'

// Mixins
import LoadSections from '@/mixins/load-sections'

export default {
  name: 'manageRestData',

  metaInfo: {
    title: 'ManageRestData'
  },

  extends: View,

  mixins: [
    LoadSections([
      'ManageRestData',
      'info',
    ]),
  ],
}
</script>
