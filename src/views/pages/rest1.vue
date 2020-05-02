<template>
<div>
  <RestBanner v-if="activeComponents.includes('Home')" :restData="restData"></RestBanner>
  <RestVetrina v-if="activeComponents.includes('Vetrina')"></RestVetrina>
  <Restmenu v-if="activeComponents.includes('Menu')" ></Restmenu>
  <RestGalleria v-if="activeComponents.includes('Galleria')" ></RestGalleria>
  <RestInfo v-if="activeComponents.includes('Info')"></RestInfo>
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
  created() {
    this.getRestaurantData(this.restID).catch(error => {
      if (error.status === 404)
        this.$router.push('/404')
    })
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
