<template>
  <div :style="image" class="body" id="HOME">
    <v-row align="center" class="ma-0 pa-8" justify="center">
      <v-col cols="6" md="4">
        <base-name-rest-card :description="description" :name="restData.activity_name" :admin="admin" @edited="submitDescription($event)"></base-name-rest-card>
      </v-col>
      <v-col cols="6" md="4">
      </v-col>
      <v-col cols="12" md="4">

      </v-col>
    </v-row>
  </div>
</template>
<script>
import {mapActions} from "vuex";

export default {
  name: "restHome",
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
  methods: {
    ...mapActions('restaurantData', ['editHomeComponent']),
    submitDescription: function(des) {
      const data = {
        description: des
      };
      const formData = new FormData();
      formData.append('data', JSON.stringify(data));
      this.editHomeComponent(formData)
    },

  },
  computed: {
    image() {
        const imageURL = this.$store.getters['restaurantData/home'].image;
        return { backgroundImage: "url(" + imageURL + ") " }
    },
    description(){
      return this.$store.getters['restaurantData/home'].description
    }
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
