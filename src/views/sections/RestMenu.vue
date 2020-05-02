<template>
  <div class="body" id="Menu">
    <v-row>
      <v-col>
        <base-cat-tabs :menu="menu" :admin="admin"/>
      </v-col>
    </v-row>
    <v-row
    class="ma-0 pa-8"
    >
    <v-col
    >
    
  </v-col>

</v-row>
</div>
</template>

<script>

export default {
  name: "restmenu",
  props: {
      admin: {
        type: Boolean,
        default: false,
      }
  },
  data() {
    return {

    }
  },
  computed: {
      menu() {
          return this.$store.getters['restaurantData/productList']
      },
  }

}
</script>

<style scoped>

.body {
  margin: 0!important;
  background:firebrick;
}



</style>
