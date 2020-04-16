<script>
  // Extensions
  import View from '@/views/View'

  // Mixins
  import LoadSections from '@/mixins/load-sections'

  export default {
    name: 'RegBusiness',

    metaInfo: { title: 'RegBusiness' },

    extends: View,

    mixins: [
      LoadSections([
        'newsletter',
        'RegBusiForm',
        'info',
      ]),
    ],

    props: {
      id: {
        type: String,
        default: 'RegBusiness',
      },
    },
  }
</script>