<template>
<div>
  <RestBanner v-if="activeComponents.home.show" :restData="restData"></RestBanner>
  <RestVetrina v-if="activeComponents.vetrina.show"></RestVetrina>
  <Restmenu v-if="activeComponents.menu.show" ></Restmenu>
  <RestGalleria v-if="activeComponents.galleria.show" ></RestGalleria>
  <RestInfo v-if="activeComponents.contattaci.show"></RestInfo>
  <Info></Info>
</div>
</template>


<script>
// Extensions
import View from '@/views/View'

// Components
import Restmenu from "../sections/RestMenu";
import RestBanner from "../sections/RestBanner";
import RestVetrina from "../sections/RestVetrina";
import RestGalleria from "../sections/RestGalleria";
import RestInfo from "../sections/RestInfo";
import Info from "../sections/Info";
import {
  mapActions
} from "vuex";

export default {
  name: 'restaurant',
  components: {
    Restmenu,
    RestBanner,
    RestVetrina,
    RestGalleria,
    RestInfo,
    Info
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
  }
}
</script>
