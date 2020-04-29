<template>
  <div>

    <button @click="manageComponents('Home')">{{getButtonMessageFor('Home')}}</button><br>
    <RestBanner v-if="activeComponents.includes('Home')" :restData="restData" :admin="admin"></RestBanner>

    <button @click="manageComponents('Vetrina')">{{getButtonMessageFor('Vetrina')}}</button><br>
    <RestVetrina v-if="activeComponents.includes('Vetrina')"></RestVetrina>

    <button @click="manageComponents('Menu')">{{getButtonMessageFor('Menu')}}</button><br>
    <Restmenu v-if="activeComponents.includes('Menu')" :id="restID" :name="name"></Restmenu>

    <button @click="manageComponents('Galleria')">{{getButtonMessageFor('Galleria')}}</button><br>
    <RestGalleria v-if="activeComponents.includes('Galleria')" ></RestGalleria>
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
