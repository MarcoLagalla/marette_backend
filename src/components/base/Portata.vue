<template>
  <v-card color="mx-auto" width="800" height="800">
    <v-card-title class="headline" v-text="portata.name"></v-card-title>
    <v-card-subtitle
            v-text="'Puoi scegliere ' + portata.num_products + ' di questi prodotti'">
    </v-card-subtitle>
    <v-btn @click="addPortata" text>Aggiungi portata</v-btn>
    <base-add-portata @added_portata="submitPortata($event)"></base-add-portata>
  </v-card>
</template>

<script>
    export default {
        name: "Portata",
        props: ['portata']
    }
</script>

<style scoped>

</style>