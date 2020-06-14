<template>
  <div class="container" id="Galleria">
    <div class="gallery">
      <div v-for="image in images" :key="image.id" class="gallery-item">
        <v-btn name="delete" color="white" v-if="admin" @click="$emit('removed', image.id)" class="managebutton">
          <i class="fas fa-times"></i>
        </v-btn>
        <v-btn name="edit" color="white" v-if="admin" @click="$emit('edited', image)" class="managebutton">
          <i class="far fa-edit"></i>
        </v-btn>
        <div class="imagname"> {{image.name}} </div>
        <img class="gallery-image" :src="image.image" :alt="image.description">
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: 'BaseRestGalleria',
  props: {
    admin: {
      type: Boolean,
      default: false,
    }
  },
  computed: {
      images() {
          return this.$store.getters['restaurantData/galleria'].immagini;
      },
  }
}
</script>
<style scoped>
  .imagname {
    position: absolute;
    bottom: 0;
    margin: 10px;
    padding: 10px;
    color: white;
    font-weight: lighter;
    font-size: 1em;
    text-transform: capitalize;
  }
.container {
  max-width: 100rem;
  margin: auto;
}
.heading {
  font-size: 4rem;
  font-weight: 500;
  line-height: 1.5;
  text-align: center;
  padding: 3.5rem 0;
  color: #1a1a1a;
}
.heading span {
  display: block;
}
.gallery {
    margin: auto;
}

.gallery-item {
  /* Minimum width of 24rem and grow to fit available space */
  max-width: 20rem;
  /* Margin value should be half of grid-gap value as margins on flex items don't collapse */
  margin: auto!important;
  overflow: hidden;
}

.gallery-image {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  margin: auto;
  transition: transform 400ms ease-out;
}
.gallery-image:hover {
  transform: scale(1.15);
}
/*
The following rule will only run if your browser supports CSS grid.
Remove or comment-out the code block below to see how the browser will fall-back to flexbox styling.
*/
@supports (display: grid) {
  .gallery {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(24rem, 1fr));
    grid-gap: 2rem;
  }
  .gallery,
  .gallery-item {
    margin: 0;
  }
}
</style>
