<template>
  <div>
    <v-btn class="managebutton" @click="portata.showAddPortata = true" text>{{addBtn}}</v-btn>
    <div v-show="portata.showAddPortata" class="addportata" id="AddPortata">
      <v-text-field outlined v-model='portata.name' type="text" label="Nome della portata" required></v-text-field>
      <v-text-field outlined v-model='portata.num_products' type="number" label="Numero di piatti selezionabili" required></v-text-field>

      <v-row >
          <v-col v-for="(product, i) in portata.products" :key="i" cols="12" >
            <base-product :product="product" :delete="true" @removed="removeProduct(product)" :discounts_list="[]"></base-product>
          </v-col>
        </v-row>

      <v-btn class="managebutton" @click="showAddProduct=true" text>Aggiungi prodotto</v-btn>
      <base-add-product-to-portata v-show="showAddProduct" @added_product="addProduct($event)"></base-add-product-to-portata>

      <v-btn class="managebutton"  @click="submitPortata" :disabled="portata.products.length===0" text>{{submitBtn}}</v-btn>
    </div>
  </div>
</template>

<script>

  export default {
    name: "AddPortata",
    props: {
      portata: {
        type: Object,
        required: false,
        default:() => ({
          name: '',
          num_products: 1,
          products: [],
          edit: false,
          showAddPortata: false,
        })
      },
    },
    data: () => ({
        showAddProduct: false,
        addBtnNew: 'Aggiungi portata',
        addBtnEdit: 'Modifica portata',
        submitBtnNew: 'Salva portata',
        submitBtnEdit: 'Salva cambiamenti',
    }),
    methods: {
      addProduct: function(prod) {
        this.portata.products = this.portata.products.concat(prod);
        this.showAddProduct =  false
      },
      removeProduct: function(prod){
        this.portata.products.splice(this.portata.products.indexOf(prod), 1);
      },
      submitPortata: function(){
          if (this.portata.edit)
              this.$emit('edit_portata', this.portata)
          else
              this.$emit('new_portata', this.portata)
      }
    },
    computed: {
      addBtn() {
          return this.portata.edit? this.addBtnEdit : this.addBtnNew
      },
      submitBtn() {
          return this.portata.edit? this.submitBtnEdit : this.submitBtnNew
      },
    },
  }
</script>

<style scoped>
.addportata {

}
</style>