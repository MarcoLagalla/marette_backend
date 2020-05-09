<template>
<div class="infocard">
  <v-card dark class="mx-6 mt-12" height="50%" max-width="344" outlined color="rgba(0,0,0,0.8)">
    <v-list-item three-line>
      <v-list-item-content>
        <div class="overline mb-4"></div>
        <v-list-item-title class="title"><h1>{{activity_name}}</h1></v-list-item-title>
        <v-text-field v-if="admin">Ciao</v-text-field>
        <v-list-item-subtitle>{{activity_description}}</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>
    <v-card-actions>
    </v-card-actions>
  </v-card>
</div>
</template>
<script>
export default {
  props: ['activity_name', 'activity_description', 'admin'],
  name: "NameRestCard"
}
</script>
<style scoped>
  .title {
    text-transform: capitalize;
  }
  h1 {
    font-size: 1.5em;
  }
</style>
