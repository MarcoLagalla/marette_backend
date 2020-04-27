<template>
  <div class="body" id="Home">
    <v-row
    align="center"
    class="ma-0 pa-8"
    justify="center"
    >
    <v-col
       cols="6"
       md="4"
     >

     </v-col>
     <v-col
        cols="6"
        md="4"
      >

      </v-col>
      <v-col
         cols="6"
         md="4"
       >
       <div class="infocard">
         <v-card dark
           class="mx-6 mt-12"
           height="50%"
           max-width="344"
           outlined
           color="rgba(0,0,0,0.8)"
         >
           <v-list-item three-line>
             <v-list-item-content>
               <div class="overline mb-4"></div>
               <v-list-item-title class="headline mb-1">{{restData.activity_name}}</v-list-item-title>
               <v-list-item-subtitle>{{restData.activity_description}}</v-list-item-subtitle>
             </v-list-item-content>


           </v-list-item>

           <v-card-actions>

           </v-card-actions>
         </v-card>
       </div>
       </v-col>
</v-row>
</div>
</template>

<script>

export default {
  name: "restban",

  props: {
      restData: {
          type: Object,
          required: true,
      },
  }

}
</script>

<style scoped>
.infocard {
  height:400px;
}
.body {
  margin: 0!important;
  background: url("https://images6.alphacoders.com/609/609345.jpg") no-repeat center center fixed;
  background-size: cover;

}

.regbtn2{
    padding: 10px;
    margin: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

</style>
