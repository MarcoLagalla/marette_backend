<template>
  <div class="body" id="GALLERIA">

    <base-rest-h1> Galleria </base-rest-h1>
    <div class="gallerycont">

      <base-rest-galleria :admin="admin" @removed="removeImage($event)" @edited="askForEdit($event)"> </base-rest-galleria>
      <base-add-gallery-image v-if="admin" :imagePrefill="imagePrefill" @added="submitImage($event)"></base-add-gallery-image>
    </div>
  </div>
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
  data: function () {
    return {
      imagePrefill: {
        image: '',
        name: '',
        description: '',
        edit: false
      },

    }
  },

  methods: {
    ...mapActions('restaurantData', ['addGalleryImage', 'removeGalleryImage', 'editGalleryImage']),
    submitImage: function (img) {
      if(this.imagePrefill.edit){
          const payload = {data: img, imageId: this.imagePrefill.id}
          this.editGalleryImage(payload)
      }
      else
        this.addGalleryImage(img)

      this.imagePrefill = {
        image: '',
        name: '',
        description: '',
        edit: false
      }
    },
    removeImage: function (imgId) {
      this.removeGalleryImage(imgId)
    },
    askForEdit: function (img) {
        img.edit = true
        this.imagePrefill = img
    },
  }

}
</script>

<style scoped>
.gallerycont {
  padding: 30px;
  background: var(--whitesmoke);
}
</style>
