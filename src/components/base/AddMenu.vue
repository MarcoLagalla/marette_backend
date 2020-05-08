<template>
  <v-card color="mx-auto" width="800" height="800">
    <v-card-title class="headline" v-text="'Aggiungi menù'"></v-card-title>
    <v-card-subtitle
            v-text="'Puoi creare diverse portate, in ognuna puoi aggiungere più piatti e decidere se il cliente li potrà selezionare tutti o sceglierne uno'">
    </v-card-subtitle>
    <v-text-field v-model='name' type="text" label="Nome del menu" required></v-text-field>
    <v-text-field v-model='description' type="text" label="Descrizione del menu"></v-text-field>
    <v-text-field v-model='price' type="number" label="Prezzo del menu completo" required></v-text-field>
    <v-text-field v-model='iva' type="number" label="IVA applicata" required></v-text-field>
    <base-portata v-for="portata in portate" :key="portata.id" :portata="portata" :delete="true" @removed="deletePortata(portata)"></base-portata>
    <v-btn @click="showAddPortata = true" text>Aggiungi portata</v-btn>
    <base-add-portata v-show="showAddPortata" @added_portata="submitPortata($event)"></base-add-portata>
    <v-btn @click="submitMenu" :disabled="portate.length===0" text>Salva Menu</v-btn>
  </v-card>
</template>

<script>

import {mapActions} from "vuex";

export default {
  name: "AddMenu",
  data: () => ({
    portate: [],
    name: '',
    description: '',
    price: '',
    iva: '',
    showAddPortata: false
  }),
  methods: {
    ...mapActions('restaurantData', ['addMenuEntry', 'deleteMenuEntry']),
    submitPortata: function(portata) {
        this.showAddPortata = false
      this.portate.push(portata)
      var payload = {
          name: portata.name,
          num_products: portata.num_products,
          products: []
      }
      portata.products.forEach(function (item) {
        payload.products.push(item.id)
      });
      var id
      this.addMenuEntry(payload).then(function (resp) {
        id = resp.id
      }) //TODO: se sbaglia ad aggiungiere la entry devo gestire l'errore

      this.portate[this.portate.indexOf(portata)].id = id
    },
    deletePortata: function(portata) {
      this.portate.splice(this.portate.indexOf(portata), 1)
      this.deleteMenuEntry(portata.id) //TODO: se sbaglia ad aggiungiere la entry devo gestire l'errore
    },
    submitMenu: function() {

    }
  }
}
</script>
<style scoped>

</style>
