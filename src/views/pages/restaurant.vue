<template>
<div>
  <RestHome v-if="activeComponents.home.show" :restData="restData"></RestHome>
  <RestVetrina v-if="activeComponents.vetrina.show"></RestVetrina>
  <RestMenu v-if="activeComponents.menu.show" ></RestMenu>
  <RestGalleria v-if="activeComponents.galleria.show" ></RestGalleria>
  <RestInfo v-if="activeComponents.contattaci.show"></RestInfo>
  <RestCart v-if="activeComponents.menu.show || activeComponents.vetrina.show"></RestCart>
</div>
</template>


<script>
// Extensions
import View from '@/views/View'

// Components
import RestMenu from "../sections/RestMenu";
import RestHome from "../sections/RestHome";
import RestVetrina from "../sections/RestVetrina";
import RestGalleria from "../sections/RestGalleria";
import RestInfo from "../sections/RestInfo";
import {
  mapActions
} from "vuex";
import RestCart from "../sections/RestCart";

export default {
  name: 'restaurant',
  components: {
    RestCart,
    RestMenu,
    RestHome,
    RestVetrina,
    RestGalleria,
    RestInfo,
  },
  metaInfo: {
    title: 'Restaurant'
  },

  extends: View,

  data() {
    return {
      restID: this.$route.params.id,
      name: this.$route.params.name
    }
  },
  methods: {
    ...mapActions('restaurantData', ['getRestaurantData']),
  },
  computed: {
    activeComponents() {
      return this.$store.getters['restaurantData/components']
    },
    restData() {
      return this.$store.getters['restaurantData/restData']
    }
  },
}
</script>
