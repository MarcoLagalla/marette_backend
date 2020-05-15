<template>
  <div class="body" id="GALLERIA">

  <base-rest-h1> Galleria </base-rest-h1>
  <div class="gallerycont">

 <base-rest-galleria :admin="admin"> </base-rest-galleria>
    <base-add-gallery-image v-if="admin" @added="submitImage($event)"></base-add-gallery-image>
   </div> </div>
</template>

<script>
import {mapActions} from "vuex";

export default {
  name: "restgalleria",
  props: {
    admin: {
      type: Boolean,
      default: false,
    }
  },

  methods: {
    ...mapActions('restaurantData', ['addGalleryImage']),
    submitImage: function (img) {
      this.addGalleryImage(img)
    }
  }

}
</script>

<style scoped>
.gallerycont {
  padding: 30px;
  background: var(--whitesmoke);
}
</style>
