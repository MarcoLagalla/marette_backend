<template>
  <div class="container" id="Galleria">

    <div class="gallery">
      <div v-for="image in images" :key="image.id" class="gallery-item">
        <v-btn name="delete" color="red" v-if="admin" @click="$emit('removed', image.id)" class="managebutton">
          <i class="fas fa-times"></i>
        </v-btn>
        <v-btn name="edit" color="blue" v-if="admin" @click="$emit('edited', image)" class="managebutton">
          <i class="far fa-edit"></i>
        </v-btn>
        {{image.name}}
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
.container {
  max-width: 100rem;
  margin: 0 auto;
  padding: 0 2rem 2rem;
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
  display: flex;
  flex-wrap: wrap;
  /* Compensate for excess margin on outer gallery flex items */
  margin: -1rem -1rem;
}
.gallery-item {
  /* Minimum width of 24rem and grow to fit available space */
  flex: 1 0 24rem;
  /* Margin value should be half of grid-gap value as margins on flex items don't collapse */
  margin: 1rem;
  box-shadow: 0.3rem 0.4rem 0.4rem rgba(0, 0, 0, 0.4);
  overflow: hidden;
}
.gallery-image {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
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
