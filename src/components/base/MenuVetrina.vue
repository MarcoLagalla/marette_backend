<template>
  <v-card dark width="800" height="800" class="scrollovf">
    <div class="blutitle">
      <v-card-title class="titlemenu" v-text="menu.name"></v-card-title>
      <v-card-subtitle
              v-text="menu.description">
      </v-card-subtitle>
    </div>
    <div class="addmenu">
      <base-portata v-for="portata in menu.entries" :key="portata.id" :portata="portata" :delete="admin"
                    @removed="deletePortata(portata)"></base-portata>
      <template v-if="admin">
        <v-btn @click="showAddPortata = true" text>Aggiungi portata</v-btn>
        <base-add-portata v-show="showAddPortata" @added_portata="submitPortata($event)"></base-add-portata>
      </template>
    </div>
    <v-card-actions>
      <button v-if="!admin" @click="$emit('added')" class="addtocart">Aggiungi al carrello <i class="fas fa-shopping-basket"></i></button>
    </v-card-actions>
  </v-card>
</template>

<script>
    import {mapActions} from "vuex";

    export default {
        name: "MenuVetrina",
        props: {
            menu: {
                type: Object,
                required: true
            },
            admin: {
              type: Boolean,
              required: false,
              default: false
            },
        },
        data: () => ({
            showAddPortata:  false
        }),
        methods: {
            ...mapActions('restaurantData', ['addMenuEntry', 'deleteMenuEntry']),
            submitPortata: function (portata) {
                this.showAddPortata = false
                this.menu.entries.push(portata)
                var payload = {
                    data: {
                      name: portata.name,
                      num_products: portata.num_products,
                      products: []
                    },
                    menuId: this.menu.id
                }
                portata.products.forEach(function (item) {
                    payload.data.products.push(item.id)
                });
                this.addMenuEntry(payload)//TODO: se sbaglia ad aggiungiere la entry devo gestire l'errore

            },
            deletePortata: function (portata) {
                this.menu.entries.splice(this.menu.entries.indexOf(portata), 1)
                const payload = {menuId: this.menu.id, entryId: portata.id}
                this.deleteMenuEntry(payload) //TODO: se sbaglia ad aggiungiere la entry devo gestire l'errore
            },
        }
    }
</script>

<style scoped>

.addtocart {
  position: absolute;
  bottom: 10px;
  right: 10px;
  background: var(--chilli);
  padding: 10px;
  color: white;
  border-radius: 25px;
  border: inset 2px var(--chilli);
  font-weight: bold;
}
  h1 {
  color: white;
  text-align: center;
  padding-top: 20px;
}

  .vetrinacard {
    box-shadow: 0 0 10px var(--charcoal);

  }
</style>