<template>
  <div class="body">
  <div class="body2" id="VETRINA">
    <base-rest-h1> Vetrina </base-rest-h1>
    <v-container>
      <v-row>
        <v-col v-if="admin" cols="12" md="6">
          <base-add-menu  :menu="menuToManage" @new_menu="submitMenu($event)" @edit_menu="submitEditMenu($event)"></base-add-menu>
        </v-col>
        <v-col v-for="menu in menus" :key="menu.id" cols="12" md="6">
          <base-menu-vetrina :menu="menu" :admin="admin" @removed="removeMenu(menu)" @edited="askEditMenu(menu)"></base-menu-vetrina>
        </v-col>
      </v-row>
    </v-container>
  </div>
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
      menuToManage: {
          name: '',
          description: '',
          price: '',
          iva: '',
          edit: false
      }
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
    ...mapActions('restaurantData', ['deleteMenu', 'addMenu', 'editMenu']),
    removeMenu: function (menu) {
      this.deleteMenu(menu) //TODO: se sbaglia ad eliminare devo gestire
    },
    askEditMenu: function (menu) {
        menu.edit = true
        this.menuToManage = menu
        document.getElementById('AddMenu').scrollIntoView(false)
        document.getElementById('AddMenu').focus({
          preventScroll: true
        });
    },
    submitEditMenu: function (menu) {
      this.editMenu({
        menuId: menu.id,
        data: {
          name: menu.name,
          description: menu.description,
          price: menu.price,
          iva: menu.iva,
          entries: menu.entries
        }
      })
      .then(() =>{
        alert('Menù aggiornato con successo')
      })
      .catch((err) =>{
        alert('Errore ' + err)
      })

      this.menuToManage = {
          name: '',
          description: '',
          price: '',
          iva: '',
          edit: false
      }
    },
    submitMenu: function (menu) {
      this.addMenu({
          name: menu.name,
          description: menu.description,
          price: menu.price,
          iva: menu.iva
      }).then(() =>{
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

  background: var(--whitesmoke);
}
.body2 {
  margin: auto;
  width: 90%;
}
h1 {
  color: white;
  text-align: center;
  padding-top: 20px;
}
.addtocart {
  position: absolute;
  bottom: 10px;
  right: 10px;
  background: var(--emerald);
  padding: 10px;
  color: white;
  border-radius: 25px;
  border: inset 2px var(--emerald);
  font-weight: bold;
  transition: 0.4s ease-in-out;
}
.addtocart:hover {
  transform: rotate(360deg);
}
.vetrinacard {
  box-shadow: 0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22);
  }

</style>
