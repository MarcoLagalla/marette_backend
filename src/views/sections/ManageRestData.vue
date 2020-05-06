<template>
  <form>
    <v-container>
      <v-row dense>
        <v-col cols="6">
          <v-card color="#616161" dark class="product">
            <div class="d-flex flex-no-wrap justify-space-between">
              <div class="quant">
                <div class>
                  <v-card-title class="headline" v-text="'Nome del locale'"></v-card-title>
                  <v-expand-transition><div v-show="show">
                  <div class="description" v-text="restData.activity_name"></div></div></v-expand-transition>
                </div>
              </div>
              <v-card-actions class="pos1">
                <v-btn @click="show = !show" color="red" class="addtocart">
                  <i class="fas fa-pencil-alt"></i>
                </v-btn>
              </v-card-actions>
            </div>
          </v-card>
        </v-col>

        <v-col cols="6">
          <v-card color="#616161" dark class="product">
            <div class="d-flex flex-no-wrap justify-space-between">
              <div class="quant">
                <div class>
                  <v-card-title class="headline" v-text="'Descrizione del locale'"></v-card-title>
                  <v-expand-transition><div v-show="show0">
                  <div class="description" v-text="restData.activity_description"></div></div></v-expand-transition>
                </div>
              </div>
              <v-card-actions class="pos1">
                <v-btn @click="show0 = !show0" color="red" class="addtocart">
                  <i class="fas fa-pencil-alt"></i>
                </v-btn>
              </v-card-actions>
            </div>
          </v-card>
        </v-col>

        <v-col cols="6">
          <v-card color="#616161" dark class="product">
            <div class="d-flex flex-no-wrap justify-space-between">
              <div class="quant">
                <div class>
                  <v-card-title class="headline" v-text="'Citta'"></v-card-title>
                  <v-expand-transition><div v-show="show1">
                  <div class="description" v-text="restData.city"></div></div></v-expand-transition>
                </div>
              </div>
              <v-card-actions class="pos1">
                <v-btn @click="show1 = !show1" color="red" class="addtocart">
                  <i class="fas fa-pencil-alt"></i>
                </v-btn>
              </v-card-actions>
            </div>
          </v-card>
        </v-col>

        <v-col cols="6">
          <v-card color="#616161" dark class="product">
            <div class="d-flex flex-no-wrap justify-space-between">
              <div class="quant">
                <div class>
                  <v-card-title class="headline" v-text="'Indirizzo'"></v-card-title>
                  <v-expand-transition><div v-show="show2">
                  <div class="description" v-text="restData.address"></div></div></v-expand-transition>
                </div>
              </div>
              <v-card-actions class="pos1">
                <v-btn @click="show2 = !show2" color="red" class="addtocart">
                  <i class="fas fa-pencil-alt"></i>
                </v-btn>
              </v-card-actions>
            </div>
          </v-card>
        </v-col>

        <v-col cols="6">
          <v-card color="#616161" dark class="product">
            <div class="d-flex flex-no-wrap justify-space-between">
              <div class="quant">
                <div class>
                  <v-card-title class="headline" v-text="'Numero civico'"></v-card-title>
                  <v-expand-transition><div v-show="show3">
                  <div class="description" v-text="restData.n_civ"></div></div></v-expand-transition>
                </div>
              </div>
              <v-card-actions class="pos1">
                <v-btn @click="show3 = !show3" color="red" class="addtocart">
                  <i class="fas fa-pencil-alt"></i>
                </v-btn>
              </v-card-actions>
            </div>
          </v-card>
        </v-col>

        <v-col cols="6">
          <v-card color="#616161" dark class="product">
            <div class="d-flex flex-no-wrap justify-space-between">
              <div class="quant">
                <div class>
                  <v-card-title class="headline" v-text="'Cap'"></v-card-title>
                  <v-expand-transition><div v-show="show4">
                  <div class="description" v-text="restData.cap"></div></div></v-expand-transition>
                </div>
              </div>
              <v-card-actions class="pos1">
                <v-btn @click="show4 = !show4" color="red" class="addtocart">
                  <i class="fas fa-pencil-alt"></i>
                </v-btn>
              </v-card-actions>
            </div>
          </v-card>
        </v-col>

        <v-col cols="6">
          <v-card color="#616161" dark class="product">
            <div class="d-flex flex-no-wrap justify-space-between">
              <div class="quant">
                <div class>
                  <v-card-title class="headline" v-text="'Numero di telefono'"></v-card-title>
                  <v-expand-transition><div v-show="show5">
                  <div class="description" v-text="restData.restaurant_number"></div></div></v-expand-transition>
                </div>
              </div>
              <v-card-actions class="pos1">
                <v-btn @click="show5 = !show5" color="red" class="addtocart">
                  <i class="fas fa-pencil-alt"></i>
                </v-btn>
              </v-card-actions>
            </div>
          </v-card>
        </v-col>

        <v-col cols="6">
          <v-card color="#616161" dark class="product">
            <div class="d-flex flex-no-wrap justify-space-between">
              <div class="quant">
                <div class>
                  <v-card-title class="headline" v-text="'Partita IVA'"></v-card-title>
                  <v-expand-transition><div v-show="show6">
                  <div class="description" v-text="restData.p_iva"></div></div></v-expand-transition>
                </div>
              </div>
              <v-card-actions class="pos1">
                <v-btn @click="show6 = !show6" color="red" class="addtocart">
                  <i class="fas fa-pencil-alt"></i>
                </v-btn>
              </v-card-actions>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
    <div class="center">
    <button type="submit" class="save">Salva cambiamenti <i class="far fa-save fa-1x"></i></button></div>
  </form>
</template>

<script>
export default {
  name: "ManageRestData",
  data() {
    return {
    show: false,
    show0:false,
    show1: false,
    show2: false,
    show3: false,
    show4: false,
    show5: false,
    show6: false,
    }
  },
  computed: {
    restData() {
      return this.$store.getters["restaurantData/restData"];
    }
  },
  beforeDestroy() {
    alert("Sicuro?");
  }
};
</script>

<style scoped>
.center {
  margin: auto;
  width: 400px;
}
.save {
  padding: 10px;
  border-radius: 25px;
  background: darkorange;
  margin: 10px;
  color: aliceblue;
  font-weight: bold;
  font-size: 1.5em;
  box-shadow: 0 0 4px var(--chilli);
  transition:ease-in-out 0.5s;
}
.save:hover {
  box-shadow: 0 0 10px var(--chilli);
}
.description {
  padding: 10px;;
}
</style>