
<script>
// Extensions
import View from '@/views/View'

// Mixins
import LoadSections from '@/mixins/load-sections'

export default {
  name: "resetPass",

  metaInfo: {
    title: 'resetPass'
  },

  extends: View,

  mixins: [
    LoadSections([
      'ResetPass',
    ]),
  ],

  props: {
    id: {
      type: String,
      default: 'resetPass',
    },
  },

}
</script>

<style scoped>

</style>