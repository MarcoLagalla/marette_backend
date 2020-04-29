<template>
<div class="cartbody">
  <h1>Carrello</h1>
  <v-row dense>
    <v-col>
      <v-card class="mx-2 mt-2" max-width="344" outlined color="rgba(220,220,220,0.9)">
        <v-list-item three-line>
          <v-list-item-content>
            <div class="overline mb-4"></div>
            <v-list-item-title class="headline mb-1">roba nel carrello</v-list-item-title>
            <v-list-item-subtitle>bla bla bla</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-card-actions>
          <button type="button" name="button">checkout</button>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</div>
</template>
<script>
export default {
  name: 'BaseRestCart',
  inheritAttrs: false,
}
</script>
<style scoped>
h1 {
  color: white;
  margin-bottom: 10px;
  margin-left: 10px;
}
</style>
