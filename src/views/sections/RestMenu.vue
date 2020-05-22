<template>
  <div class="body">
  <div class="body2" id="MENU">
    <v-row>
      <v-col>
        <base-rest-h1>Menu</base-rest-h1>
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
  </div>
</template>

<script>

import BaseRestH1 from "../../components/base/RestH1";
export default {
  name: "restmenu",
  components: {BaseRestH1},
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

  background: var(--whitesmoke);

}
.body2 {
  width: 90%;
  margin: auto;
}


</style>
