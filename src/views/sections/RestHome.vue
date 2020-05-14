<template>
  <div :style="image" class="body" id="HOME">
    <v-row align="center" class="ma-0 pa-8" justify="center">
      <v-col cols="6" md="4">
      </v-col>
      <v-col cols="6" md="4">
      </v-col>
      <v-col cols="12" md="4">
        <base-name-rest-card :activity_description="restData.activity_description" :activity_name="restData.activity_name" :admin="admin"></base-name-rest-card>
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
      admin: {
        type: Boolean,
        default: false,
      }
  },
  data: () => ({
  }),
  computed: {
    image() {
        const imageURL = this.$store.getters['restaurantData/home'].image;
        console.log(imageURL)
        return { backgroundImage: "url(" + imageURL + ") " }
    },
  }
}
</script>
<style scoped>
.infocard {
  height: 400px;
}
.body {
  margin: 0 !important;
  right: 0!important;
  height: 100%;
  width: 100%;
  background: no-repeat center center fixed ;
  background-size: cover;


}
.regbtn2 {
  padding: 10px;
  margin: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
