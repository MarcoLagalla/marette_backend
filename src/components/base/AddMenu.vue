<template>
  <v-card color="mx-auto" width="800" height="800">
    <v-card-title class="headline" v-text="'Aggiungi menù'"></v-card-title>
    <v-card-subtitle
            v-text="'Puoi creare diverse portate, in ognuna puoi aggiungere più piatti e decidere se il cliente li potrà selezionare tutti o sceglierne uno'">
    </v-card-subtitle>
    <v-btn @click="addPortata" text>Aggiungi portata</v-btn>
    <base-add-portata v-for="portata in portate" :key="portata">{{portata}}</base-add-portata>
  </v-card>
</template>

<script>

export default {
  name: "AddMenu",
  data: () => ({
    portate: []
  }),
  methods: {
    addPortata: function() {
      if (this.portate.length === 0){
        this.portate.push(0)
      }
      else {
        this.portate.push( this.portate[this.portate.length - 1] + 1)
      }
    }
  }
}
</script>
<style scoped>

</style>
