
<script>
      // Extensions
        import View from '@/views/View'

      // Mixins
        import LoadSections from '@/mixins/load-sections'

    export default {
        name: "manageRest",

        metaInfo: { title: 'manageRest' },

        extends: View,

    mixins: [
        LoadSections([
            'ManageRest',
            'info',
         ]),
    ],

    props: {
      id: {
        type: String,
        default: 'manageRest',
      },
    },

    }

</script>

<style scoped>

</style>