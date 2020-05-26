<template>
  <div>
    <div class="buttons">
      <button @click="manageComponents('home')">{{getButtonMessageFor('home')}}</button><hr>
      <button @click="manageComponents('vetrina')">{{getButtonMessageFor('vetrina')}}</button><hr>
      <button @click="manageComponents('menu')">{{getButtonMessageFor('menu')}}</button><hr>
      <button @click="manageComponents('galleria')">{{getButtonMessageFor('galleria')}}</button><hr>
      <button @click="manageComponents('contattaci')">{{getButtonMessageFor('contattaci')}}</button><hr>
    </div>
    <RestHome v-if="activeComponents.home.show" :restData="restData" :admin="admin"></RestHome>

    <RestVetrina v-if="activeComponents.vetrina.show" :admin="admin"></RestVetrina>

    <RestMenu v-if="activeComponents.menu.show" :admin="admin"></RestMenu>

    <RestGalleria v-if="activeComponents.galleria.show" :admin="admin" ></RestGalleria>

    <RestInfo v-if="activeComponents.contattaci.show" ></RestInfo>
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

export default {
  name: 'manageRest',
  components: {
    RestMenu,
    RestHome,
    RestVetrina,
    RestGalleria,
    RestInfo,
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
            return ' - ' + nameComponent
          else
              return ' + ' + nameComponent
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
    right: 0;
    top: 300px;
    z-index: 100;
    color: white;
    font-weight: bold;

    -webkit-text-stroke-width: 1px;
  -webkit-text-stroke-color: grey;
  }
 /* @media only screen and (max-width: 600px) {
    .buttons {
      left: 0;
      width: 50%;
    }
  }  */
  button {
    padding: 10px;
    width: 100%;
    border: solid white 1px;
    transition: 0.4s;
    background: rgba(5,5,5,0.5);
    border-radius: 15px 0 0 15px;
  }
  button:hover {
    background: rgba(255, 255, 255, 0.5);
  }
</style>
