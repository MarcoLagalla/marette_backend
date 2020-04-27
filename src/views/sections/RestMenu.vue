<template>
  <div class="body" id="Menu">
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
        cols="9"
        md="9"
      >
<base-menu />
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
