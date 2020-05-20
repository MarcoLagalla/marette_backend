<template>
  <v-row >
    <v-dialog v-model="active" overlay-opacity="0.8" >
      <template v-slot:activator="{ on }">
        <div class="rel">
          <v-btn name="edit" color="white" v-on="on"  class="managebutton">
            Modifica immagine di sfondo <i class="far fa-edit"></i>
          </v-btn>
        </div>
        </template>
        <v-card justify="center">
          <picture-input
            ref="background"
            @change="onChanged"
            :width="400"
            :height="400"
            size="3"
            :zIndex="0"
            :crop="true"
            :changeOnClick="true"
            :prefill="imageUrl"
            accept="image/jpeg, image/png, image/gif"
            buttonClass="ui button primary"
            :customStrings="{
            upload: '<h1>Carica immagine</h1>',
            drag: 'Trascina qui la un immagine di vetrina o clicca per selezionarla'}">
          </picture-input>
          <v-btn color="green" @click="submitImage" text>Salva immagine</v-btn>
        </v-card>
    </v-dialog>
  </v-row>
</template>

<script>

    import PictureInput from "vue-picture-input";

    export default {
        name: "AddHomeImage",
        props: ['imageUrl'],
        components: {
            PictureInput,
        },
        data: () => ({
            image: '',
            active: false
        }),
        methods: {
            submitImage(){
                this.$emit('edited', this.image)
                this.active = false
            },
            onChanged() {
                if (this.$refs.background.file) {
                    this.image = this.$refs.background.file;
                } else {
                    console.log("Old browser. No support for Filereader API");
                }
            },
        }

    }
</script>

<style scoped>

</style>