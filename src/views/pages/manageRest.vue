<template>
  <div>
    <div class="buttons">
      <button @click="manageComponents('Home')">{{getButtonMessageFor('Home')}}</button><hr>
      <button @click="manageComponents('Vetrina')">{{getButtonMessageFor('Vetrina')}}</button><hr>
      <button @click="manageComponents('Menu')">{{getButtonMessageFor('Menu')}}</button><hr>
      <button @click="manageComponents('Galleria')">{{getButtonMessageFor('Galleria')}}</button><hr>
      <button @click="manageComponents('Info')">{{getButtonMessageFor('Info')}}</button><hr>
    </div>
    <RestBanner v-if="activeComponents.includes('Home')" :restData="restData" :admin="admin"></RestBanner>

    <RestVetrina v-if="activeComponents.includes('Vetrina')"></RestVetrina>

    <Restmenu v-if="activeComponents.includes('Menu')" :admin="admin"></Restmenu>

    <RestGalleria v-if="activeComponents.includes('Galleria')" ></RestGalleria>

    <RestInfo v-if="activeComponents.includes('Info')" ></RestInfo>
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
      admin: true

    }
  },
  methods: {
    ...mapActions('restaurantData', ['getRestaurantData', 'addComponent', 'removeComponent']),
      manageComponents(nameComponent){
        if (this.activeComponents.includes(nameComponent)){
            this.removeComponent(nameComponent);
        }
        else {
            this.addComponent(nameComponent)
        }
      },
      getButtonMessageFor(nameComponent){
        if (this.activeComponents.includes(nameComponent))
            return 'Disattiva ' + nameComponent
          else
              return 'Attiva ' + nameComponent
      }
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
    width: 100%;
    border: solid white 1px;
    transition: 0.4s
  }
  button:hover {
    background: rgba(255, 255, 255, 0.5);
  }
</style>
