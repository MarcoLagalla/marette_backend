<template>
    <div>
        <button type="button" > Aggiungi Prodotto</button>
        <v-form>
                        <v-text-field
                        solo background-color="#486F83"
                        v-model='name'
                        type="text"
                        placeholder=" Inserire nome prodotto"
                        id="name"
                        name="name" required></v-text-field>

                        <v-text-field
                        solo background-color="#486F83"
                        v-model='description'
                        type="text"
                        placeholder=" Inserire descrizione"
                        id="description"
                        name="description" required></v-text-field>

                        <v-text-field
                        solo background-color="#486F83"
                        v-model='category'
                        type="text"
                        placeholder=" Inserire categoria"
                        id="category"
                        name="category" required></v-text-field>

                        <v-text-field
                        solo background-color="#486F83"
                        v-model='price'
                        type="text"
                        placeholder=" Inserire prezzo"
                        id="price"
                        name="price" required></v-text-field>
        </v-form>
        <p v-for="(campo, i) in user" :key="i" >{{i.replace(/_/g , ' ')}} : {{campo}}</p>
    </div>
    
</template>

<script>
    export default {
        name: "ManageRest",

        data() {

            return{

            }
        },

        computed: {
            food_category_choice(){
                return this.$store.getters['manageRestaurant/food_category_choice']
            }
        }
    }
</script>

<style scoped>

</style>