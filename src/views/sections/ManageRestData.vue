<template>
  <v-container>
      <v-row dense>
        <v-col v-for="(data, i) in restData" :key="i" cols="12">
          <v-card color="#616161" dark class="product">
            <div class="d-flex flex-no-wrap justify-space-between">
              <div class="quant">
                <div class>
                  <v-card-title class="headline" v-text="data.name"></v-card-title>
                  <v-card-subtitle class="pb-0" v-text="data.category"></v-card-subtitle>
                  <div class="description" v-text="data.description"></div>
                </div>
              </div>
              <v-card-actions class="pos1">
                <v-btn color="red" class="addtocart">
                  <i class="fas fa-shopping-basket"></i>
                </v-btn>
              </v-card-actions>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
</template>

<script>
    export default {
        name: "ManageRestData",
        computed: {
          restData() {
            return this.$store.getters['restaurantData/restData']
          }
        }
    }
</script>

<style scoped>

</style>