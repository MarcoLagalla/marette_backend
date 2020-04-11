<script>
  // Extensions
  import View from '@/views/View'

  // Mixins
  import LoadSections from '@/mixins/load-sections'

  export default {
    name: 'ContactUs',

    metaInfo: { title: 'Contact Us' },

    extends: View,

    mixins: [
      LoadSections([
        'hero-alt',
        'pro-features',
        'contact-us',
        'info'
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
