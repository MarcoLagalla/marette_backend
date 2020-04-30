<template>
  <v-card color="basil">
    <v-card-title class="text-center justify-center py-6">
      <h1 class="font-weight-bold display-3 basil--text">Categorie</h1>
    </v-card-title>
    <v-tabs v-model="tab" background-color="transparent" color="basil" grow>
      <v-tab v-for="category in categories" :key="category">
        {{ category }}
      </v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab">
      <v-tab-item v-for="category in categories" :key="category">
        <v-card color="basil" flat>
          <base-menu :products="menu[category]"/>
          <base-add-product :category='category' :v-if="admin"></base-add-product>
        </v-card>
      </v-tab-item>
    </v-tabs-items>
  </v-card>
</template>

<script>
export default {
  name: 'BaseCatTabs',
    props: {
    menu: {
      type: Object,
      required: true,
    },
    admin: {
      type: Boolean,
      default: false,
    }
  },
  data() {
    return {
      tab: null,
      text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
    }
  },
    computed:{
      categories() {
        var cat = []
        var men = this.menu
        var ad = this.admin
        Object.keys(men).forEach(function(key) {
          if(men[key].length!==0 || ad){
            cat.push(key)
          }
        });
        return cat
      }

    }
}
</script>
<style lang="css" scoped>
/* Helper classes */
.basil {
  background-color: #FFFBE6 !important;
}
.basil--text {
  color: #356859 !important;
}
</style>
