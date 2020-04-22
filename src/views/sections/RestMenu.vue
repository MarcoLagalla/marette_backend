<template>
  <div class="body">
    <v-row

    class="ma-0 pa-8"

    >
    <v-col
       cols=""
       md="3"
     >
<base-menu-cat />
     </v-col>
     <v-col
        cols="6"
        md="6"
      >
<base-menu />
      </v-col>
      <v-col
         cols=""
         md="3"
       >
<base-rest-cart />
       </v-col>
</v-row>
</div>
</template>

<script>

export default {
  name: "restmenu",

}
</script>

<style scoped>

.body {
  margin: 0!important;
  background: #35302D;
}



</style>
