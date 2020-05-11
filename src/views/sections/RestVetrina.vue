<template>
  <div class="body" id="VETRINA">
    <base-rest-h1> Vetrina </base-rest-h1>
    <v-container>
      <v-row>
        <v-col v-if="admin" cols="6" md="6">
          <base-add-menu></base-add-menu>
        </v-col>
        <v-col v-for="menu in menus" :key="menu.id" cols="6" md="6">
          <base-menu-vetrina :menu="menu" :admin="admin"></base-menu-vetrina>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>

export default {
  name: "restvetrina",
  props: {
    admin: {
      type: Boolean,
      required: false,
      default: false
    },
  },
  data: () => ({
    }),
  computed: {
      menus() {
          return this.$store.getters['restaurantData/menus']
      },
  },
  created() {
    this.$store.dispatch("restaurantData/listMenus")
  },

}
</script>

<style scoped>
.body {
  margin: 0 !important;
  background: var(--whitesmoke);
}

</style>
