<template>
  <div class="container" id="Galleria">
        <div class="gallery">
        <div v-for="(image, index) in images" :key="image.id" class="card-wrapper" ref="images">
                <div class="image-holder">
                    <v-btn name="delete" color="white" v-if="admin" @click="$emit('removed', image.id)" class="managebutton">
                        <i class="fas fa-times"></i>
                    </v-btn>
                <v-btn name="edit" color="white" v-if="admin" @click="$emit('edited', image)" class="managebutton">
                    <i class="far fa-edit"></i>
                </v-btn>

                    <div class="image-liquid image-holder--original" v-bind:style="{ backgroundImage: 'url(' + image.image + ')' }">
                    </div>
                </div>

                <div class="product-description" @mouseleave="resetScroll(index)">
                    <vue-custom-scrollbar class="scroll-area" :settings="settings" @ps-scroll-y="scrollHanle">
                    <!-- title -->
                        <div>
                    <h1 class="product-description__title">
                        <a href="#">
                            {{image.name}}
                            </a>
                    </h1>
                    <div v-if="image.description">
                            <br />
                            <!-- divider -->
                            <hr />

                            <!-- description -->
                            <div class="color-wrapper">

                                <b>Descrizione</b>
                                <br />
                                <p>{{ image.description }}</p>
                            </div>
                    </div>
                            </div>
                    </vue-custom-scrollbar>
                </div>


            </div>

        <!-- dd -->
    </div>
  </div>
</template>
<script>
        import vueCustomScrollbar from 'vue-custom-scrollbar';
export default {

  name: 'BaseRestGalleria',
  components: {vueCustomScrollbar},
  props: {
    admin: {
      type: Boolean,
      default: false,
    }
  },
  data: () => ({
      settings: {
        maxScrollbarLength: 60,
        minScrollbarLength: 1

      }
    }),
    methods: {
      scrollHanle() {
                //console.log(evt)
            },
       resetScroll(d) {
          this.$refs.images[d].getElementsByClassName('ps-container')[0].scrollTop = 0;
       } ,
    },
  computed: {
      images() {
          return this.$store.getters['restaurantData/galleria'].immagini;
      },
  }
}
</script>
<style scoped>

.list-inline li {
  padding: 0;
}

.card-wrapper {
  position: relative;
  max-width: 20rem;
  /* Margin value should be half of grid-gap value as margins on flex items don't collapse */
  margin: auto!important;
    width: 20rem;
  overflow: hidden!important;
  border: 1px solid #e5e5e5;
  border-bottom-width: 2px;
}
.card-wrapper:after {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  transition: opacity 0.6s cubic-bezier(0.165, 0.84, 0.44, 1);
}

.card-wrapper:hover .image-holder:before {
  opacity: .75;
}
.card-wrapper:hover .image-holder:after {
  opacity: 1;
  transform: translate(-50%, -50%);
}
.card-wrapper:hover .image-holder--original {
  transform: translateY(-15px);
}

.card-wrapper:hover .product-description {
  height: 205px;
}
@media (min-width: 768px) {
  .card-wrapper:hover .product-description {
    height: 185px;
  }
}

.image-holder {
  display: block;
  position: relative;
  width: 100%;
  height: 310px;
  background-color: #ffffff;
  z-index: 1;
}
@media (min-width: 768px) {
  .image-holder {
    height: 300px;
        overflow: hidden!important;
  }
}

.image-holder .image-holder--original {
  transition: transform 0.8s cubic-bezier(0.165, 0.84, 0.44, 1);
}

.image-liquid {
  width: 100%;
  height: 325px;
  background-size: cover;
  background-position: center center;
}

.product-description {
  position: absolute;
  left: 0;
  bottom: 0;
  width: 100%;
  height: 80px;
  padding: 10px 15px;
  overflow: hidden!important;
  background: rgba(156, 156, 156, 0.5);
  border-top: 1px solid #e5e5e5;
  color: white;
  transition: height 0.6s cubic-bezier(0.165, 0.84, 0.44, 1);
  z-index: 2;
}

@media (min-width: 768px) {
  .product-description {
    height: 40px;
        overflow: hidden!important;
  }
}
@media (max-width: 768px) {
  .product-description {
    height: 40px;
        overflow: hidden!important;
  }
}
.product-description p {
  margin: 0 0 5px;
}
.product-description .product-description__title {
  font-family: 'Raleway', sans-serif;
  position: relative;
  white-space: nowrap;
  overflow: hidden!important;
  margin: 0;
  font-size: 18px;
  line-height: 1.25;
}

.product-description .product-description__title a {
  text-decoration: none;
  color: inherit;
}

  .imagname {
    position: absolute;
    bottom: 20px;
    margin: 10px;
    padding: 10px;
    color: white;
    font-weight: lighter;
    font-size: 1em;
    text-transform: capitalize;
     z-index: 99;
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

        body {
        overflow: hidden!important;
    }
    .gallery {
        overflow: hidden!important;
    }
    .container {
        overflow: hidden!important;
    }
    .card-wrapper {
        overflow: hidden!important;
    }
    .image-holder {
        overflow: hidden!important;
    }
    .product-description {
        overflow: hidden!important;
    }
    .scroll-area {
          position: relative;
  margin: auto;
  max-width: 25rem;
  max-height: 25rem;
        overflow: hidden!important;
    }

</style>
