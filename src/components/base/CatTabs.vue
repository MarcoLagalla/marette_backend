<template>
  <v-card flat class="basil" >
    <v-tabs v-model="tab" color="basil" grow >
      <v-tab v-for="category in categories" :key="category" class="tabcat">
        {{ category }}
      </v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab">
      <v-tab-item v-for="category in categories" :key="category">
        <v-card flat >
          <base-prod-list :admin="admin" :products="menu[category]" :category="category"/>
          <base-add-product :category='category' v-if="admin" :admin="admin"></base-add-product>
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
  background-color: var(--ghostwhite) !important;
  margin-top: 1vmax;
}
.basil--text {
  color: var(--emerald) !important;
  text-shadow: 0 0 2px grey;

}
.tabcat {
  background-color: var(--ghostwhite);
}
</style>
