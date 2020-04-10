<template>
  <div class="about" id="about">
    <h1>This is an about page</h1>
  </div>
</template>

<style scoped="">
  h1 {
    color: red !important;
  }
</style>
<script>
  // Extensions
  import View from '@/views/View'

  // Mixins
  //import LoadSections from '@/mixins/load-sections'

  export default {
    name: 'rest1',

    metaInfo: { title: 'Login' },

    extends: View,

    props: {
      id: {
        type: String,
        default: 'login',
      },
    },
  }
</script>
