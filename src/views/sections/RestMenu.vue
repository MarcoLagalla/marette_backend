<template>
  <div class="body" id="Menu">
    <v-row>
      <v-col>
        <base-cat-tabs/>
      </v-col>
    </v-row>
    <v-row
    class="ma-0 pa-8"
    >
    <v-col
    >
    
  </v-col>

</v-row>
</div>
</template>

<script>

export default {
  name: "restmenu",
  props: ['name', 'id'],
  data() {
    return {

    }
  },

}
</script>

<style scoped>

.body {
  margin: 0!important;
  background: #35302D;
}



</style>
