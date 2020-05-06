<template>
  <form>
  <v-container>
      <v-row dense>
        <v-col cols="12">
          <v-card color="#616161" dark class="product">
            <div class="d-flex flex-no-wrap justify-space-between">
              <div class="quant">
                <div class>
                  <v-card-title class="headline" v-text="'Nome del locale'"></v-card-title>
                  <div class="description" v-text="restData.activity_name"></div>
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

        <v-col cols="12">
          <v-card color="#616161" dark class="product">
            <div class="d-flex flex-no-wrap justify-space-between">
              <div class="quant">
                <div class>
                  <v-card-title class="headline" v-text="'descrizione del locale'"></v-card-title>
                  <div class="description" v-text="restData.activity_description"></div>
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

        <v-col cols="12">
          <v-card color="#616161" dark class="product">
            <div class="d-flex flex-no-wrap justify-space-between">
              <div class="quant">
                <div class>
                  <v-card-title class="headline" v-text="'Città'"></v-card-title>
                  <div class="description" v-text="restData.city"></div>
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

        <v-col cols="12">
          <v-card color="#616161" dark class="product">
            <div class="d-flex flex-no-wrap justify-space-between">
              <div class="quant">
                <div class>
                  <v-card-title class="headline" v-text="'Indirizzo'"></v-card-title>
                  <div class="description" v-text="restData.address"></div>
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

        <v-col cols="12">
          <v-card color="#616161" dark class="product">
            <div class="d-flex flex-no-wrap justify-space-between">
              <div class="quant">
                <div class>
                  <v-card-title class="headline" v-text="'Numero civico'"></v-card-title>
                  <div class="description" v-text="restData.n_civ"></div>
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

        <v-col cols="12">
          <v-card color="#616161" dark class="product">
            <div class="d-flex flex-no-wrap justify-space-between">
              <div class="quant">
                <div class>
                  <v-card-title class="headline" v-text="'CAP'"></v-card-title>
                  <div class="description" v-text="restData.cap"></div>
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

        <v-col cols="12">
          <v-card color="#616161" dark class="product">
            <div class="d-flex flex-no-wrap justify-space-between">
              <div class="quant">
                <div class>
                  <v-card-title class="headline" v-text="'Numero tlefonico del locale'"></v-card-title>
                  <div class="description" v-text="restData.restaurant_number"></div>
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

        <v-col cols="12">
          <v-card color="#616161" dark class="product">
            <div class="d-flex flex-no-wrap justify-space-between">
              <div class="quant">
                <div class>
                  <v-card-title class="headline" v-text="'Partita IVA'"></v-card-title>
                  <div class="description" v-text="restData.p_iva"></div>
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
    <button type="submit" >Salva cambiamenti</button>
  </form>
</template>

<script>
    export default {
        name: "ManageRestData",
        computed: {
          restData() {
            return this.$store.getters['restaurantData/restData']
          }
        },
      beforeDestroy() {
          alert('Sicuro?')
      }
    }
</script>

<style scoped>

</style>