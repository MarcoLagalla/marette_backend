<script>
// Extensions
import View from '@/views/View'

// Mixins
import LoadSections from '@/mixins/load-sections'

export default {
  name: 'TerminiECondizioni',

  metaInfo: {
    title: 'TerminiECondizioni'
  },

  extends: View,

  mixins: [
    LoadSections([
      'TerminiECondizioni'
    ]),
  ],

  props: {
    id: {
      type: String,
      default: 'TerminiECondizioni',
    },
  },
}
</script>