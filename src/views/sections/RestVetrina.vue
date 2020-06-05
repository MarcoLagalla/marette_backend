<template>
  <div class="body" id="VETRINA">
  <div class="body2" >
    <base-rest-h1> Vetrina </base-rest-h1>
    <v-container>
      <base-add-menu v-if="true" :menu="menuToManage" @new_menu="submitMenu($event)" @edit_menu="submitEditMenu($event)"></base-add-menu>
      <v-alert type="info">Puoi creare al massimo 3 menu</v-alert>
      <v-row>
        <v-snackbar top v-model="snackbar" :timeout="timeout" :color="color" >{{text}}</v-snackbar>

        <v-col v-for="menu in menus" :key="menu.id" cols="12" md="4">
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
          edit: false,
      },
    snackbar: false,
    timeout: 4000,
    color: 'green',
    text: 'Menu creato con successo'
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
        this.snackbar = true;
        this.text = 'Menu modificato con successo';
      })
      .catch((err) =>{
        this.snackbar = true;
        this.text = 'Errore'+ err;
        this.color = 'error';
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
          this.snackbar = true;
          this.text = 'Menu creato con successo';
      }).catch((err) =>{
        this.snackbar = true;
        this.text = 'Errore'+ err;
        this.color = 'error';
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
