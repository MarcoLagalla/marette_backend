<template>
  <div class="container" id="Galleria">

    <div class="gallery">
      <div class="gallery-item">
        <img class="gallery-image" src="https://images.unsplash.com/photo-1488190211105-8b0e65b80b4e?w=500&h=500&fit=crop" alt="person writing in a notebook beside by an iPad, laptop, printed photos, spectacles, and a cup of coffee on a saucer">
      </div>
      <div class="gallery-item">
        <img class="gallery-image" src="https://images.unsplash.com/photo-1515260268569-9271009adfdb?w=500&h=500&fit=crop" alt="sunset behind San Francisco city skyline">
      </div>
      <div class="gallery-item">
        <img class="gallery-image" src="https://images.unsplash.com/photo-1506045412240-22980140a405?w=500&h=500&fit=crop" alt="people holding umbrellas on a busy street at night lit by street lights and illuminated signs in Tokyo, Japan">
      </div>
      <div class="gallery-item">
        <img class="gallery-image" src="https://images.unsplash.com/photo-1506045412240-22980140a405?w=500&h=500&fit=crop" alt="people holding umbrellas on a busy street at night lit by street lights and illuminated signs in Tokyo, Japan">
      </div>
      <div class="gallery-item">
        <img class="gallery-image" src="https://images.unsplash.com/photo-1506045412240-22980140a405?w=500&h=500&fit=crop" alt="people holding umbrellas on a busy street at night lit by street lights and illuminated signs in Tokyo, Japan">
      </div>
      <div class="gallery-item">
        <img class="gallery-image" src="https://images.unsplash.com/photo-1506045412240-22980140a405?w=500&h=500&fit=crop" alt="people holding umbrellas on a busy street at night lit by street lights and illuminated signs in Tokyo, Japan">
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
