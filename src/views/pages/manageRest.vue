<template>
  <div>
    <div class="buttons">
      <button @click="manageComponents('home')">{{getButtonMessageFor('home')}}</button>
      <button @click="manageComponents('vetrina')">{{getButtonMessageFor('vetrina')}}</button>
      <button @click="manageComponents('menu')">{{getButtonMessageFor('menu')}}</button>
      <button @click="manageComponents('galleria')">{{getButtonMessageFor('galleria')}}</button>
      <button @click="manageComponents('contattaci')">{{getButtonMessageFor('contattaci')}}</button>
    </div>
    <RestBanner v-if="activeComponents.home.show" :restData="restData" :admin="admin"></RestBanner>

    <RestVetrina v-if="activeComponents.vetrina.show" :admin="admin"></RestVetrina>

    <Restmenu v-if="activeComponents.menu.show" :admin="admin"></Restmenu>

    <RestGalleria v-if="activeComponents.galleria.show" ></RestGalleria>

    <RestInfo v-if="activeComponents.contattaci.show" ></RestInfo>
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
  name: 'manageRest',
  components: {
    Restmenu,
    RestBanner,
    RestVetrina,
    RestGalleria,
    RestInfo,
    Info
  },
  metaInfo: {
    title: 'manageRest'
  },

  extends: View,

  data() {
    return {
      restID: this.$route.params.id,
      name: this.$route.params.name,
      admin: true,

    }
  },
  methods: {
    ...mapActions('restaurantData', ['getRestaurantData', 'activateComponent', 'deactivateComponent']),
      manageComponents(nameComponent){
        if (this.activeComponents[nameComponent].show){
            this.deactivateComponent(nameComponent);
        }
        else {
            this.activateComponent(nameComponent)
        }
      },
      getButtonMessageFor(nameComponent){
        if (this.activeComponents[nameComponent].show)
            return 'Disattiva ' + nameComponent
          else
              return 'Attiva ' + nameComponent
      }
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
<style scoped>
  .buttons {
    position: fixed;
    z-index: 100;
    color: white;
    font-weight: bold;
    -webkit-text-stroke-width: 1px;
  -webkit-text-stroke-color: grey;
  }
  button {
    padding: 10px;
    
    border: solid white 1px;
    transition: 0.4s
  }
  button:hover {
    background: rgba(255, 255, 255, 0.5);
  }
</style>
