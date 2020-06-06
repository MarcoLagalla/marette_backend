<template>
  <div class="body" id="GALLERIA">
    <div class="body2">
    <base-rest-h1> Galleria </base-rest-h1>
    <div class="gallerycont">
      <base-rest-galleria :admin="admin" @removed="removeImage($event)" @edited="askForEdit($event)"> </base-rest-galleria>
      <base-add-gallery-image v-if="admin" :key="componentKey" :imagePrefill="imagePrefill" @added="submitImage($event)"></base-add-gallery-image>
    </div>
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
        edit: false,

      },
      componentKey: 0,
      imageToEdit: {}

    }
  },

  methods: {
    ...mapActions('restaurantData', ['addGalleryImage', 'removeGalleryImage', 'editGalleryImage']),
    submitImage: function (img) {
      if(this.imagePrefill.edit){
          const payload = {data: img, imageId: this.imagePrefill.id}
          this.editGalleryImage(payload).then((resp) =>{
              this.imageToEdit.image = resp.image
          })
      }
      else{
          this.addGalleryImage(img)
      }


      this.imagePrefill = {
        image: '',
        name: '',
        description: '',
        edit: false
      }
      this.componentKey += 1;
    },
    removeImage: function (imgId) {
      this.removeGalleryImage(imgId)
    },
    askForEdit: function (img) {
        this.imageToEdit = img
        img.edit = true
        this.imagePrefill = clone(img)
    },
  }

}

function clone(obj) {
    if (null == obj || "object" != typeof obj) return obj;
    var copy = obj.constructor();
    for (var attr in obj) {
        // eslint-disable-next-line no-prototype-builtins
        if (obj.hasOwnProperty(attr)) copy[attr] = obj[attr];
    }
    return copy;
}
</script>

<style scoped>
.gallerycont {
  padding: 30px;

}

.body2 {
  margin: auto;
  width: 90%;
}

.body {
  background: var(--whitesmoke);
}
</style>
