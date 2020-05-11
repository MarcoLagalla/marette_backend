<template>
  <div class="body" id="VETRINA">
    <base-rest-h1> Vetrina </base-rest-h1>
    <v-container>
      <v-row>
        <v-col v-if="admin" cols="6" md="6">
          <base-add-menu @new_menu="submitMenu($event)"></base-add-menu>
        </v-col>
        <v-col v-for="menu in menus" :key="menu.id" cols="6" md="6">
          <base-menu-vetrina :menu="menu" :admin="admin" @removed="removeMenu(menu)" @edited="editMenu(menu)"></base-menu-vetrina>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>

import {mapActions} from "vuex";

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
  methods: {
    ...mapActions('restaurantData', ['deleteMenu', 'addMenu']),
    removeMenu: function (menu) {
      this.menus.splice(this.menus.indexOf(menu), 1)
      this.deleteMenu(menu.id) //TODO: se sbaglia ad eliminare devo gestire
    },
    editMenu: function (menu) {
      this.menus.splice(this.menus.indexOf(menu), 1)
      this.deleteMenu(menu.id) //TODO: se sbaglia ad eliminare devo gestire
    },
    submitMenu: function (menu) {
      this.addMenu({
          name: menu.name,
          description: menu.description,
          price: menu.price,
          iva: menu.iva
      }).then((newMenu) =>{
          this.menus.push(newMenu)
          alert('Menù aggiunto con successo')
      }).catch((err) =>{
          alert('Errore ' + err)
      })
    }
  }

}
</script>

<style scoped>
.body {
  margin: 0 !important;
  background: var(--whitesmoke);
}

</style>
