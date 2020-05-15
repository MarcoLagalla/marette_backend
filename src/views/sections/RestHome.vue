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
    <template v-if="admin">
      <v-btn name="delete" color="red" @click="deleteImage()">
        Elimina immagine di sfondo <i class="fas fa-times"></i>
      </v-btn>
      <base-add-home-image :imageUrl="imageURL" @edited="submitImage($event)"></base-add-home-image>
    </template>
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
  data: function() {
      return {
          modImage: false,
      }
  },
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
    submitImage: function(img) {
      const formData = new FormData();
      formData.append('data','{}');
      formData.append('image',img);
      this.editHomeComponent(formData)
    },
    deleteImage: function() {
      const formData = new FormData();
      formData.append('image', '');
      formData.append('data', '{}');
      this.editHomeComponent(formData)
    },

  },
  computed: {
    image() {
        const imgUrl = this.$store.getters['restaurantData/home'].image;
        return { backgroundImage: "url(" + imgUrl + ") " }
    },
    imageURL() {
        return this.$store.getters['restaurantData/home'].image;
    },
    description(){
      return this.$store.getters['restaurantData/home'].description
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
