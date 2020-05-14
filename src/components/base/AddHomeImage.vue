<template>
  <v-row >
    <v-dialog overlay-opacity="0.8" >
      <template v-slot:activator="{ on }">
        <div class="rel">
          <v-btn name="edit" color="blue" v-on="on"  class="managebutton">
            Modifica immagine di sfondo <i class="far fa-edit"></i>
          </v-btn>
        </div>
        </template>
        <v-card justify="center">
          <picture-input
            ref="background"
            @change="onChanged"
            :width="200"
            :height="200"
            size="3"
            :zIndex="0"
            :crop="true"
            :changeOnClick="false"
            accept="image/jpeg, image/png, image/gif"
            buttonClass="ui button primary"
            :customStrings="{
            upload: '<h1>Carica immagine</h1>',
            drag: 'Trascina qui la un immagine di vetrina o clicca per selezionarla'}">
          </picture-input>
          <v-btn color="green" @click="$emit('edited', image)" text>Salva immagine</v-btn>
        </v-card>
    </v-dialog>
  </v-row>
</template>

<script>

    import PictureInput from "vue-picture-input";

    export default {
        name: "AddHomeImage",
        components: {
            PictureInput,
        },
        data: () => ({
            image: '',
        }),
        methods: {
            onChanged() {
                if (this.$refs.background.file) {
                    this.image = this.$refs.background.file;
                } else {
                    console.log("Old browser. No support for Filereader API");
                }
            },
        },

    }
</script>

<style scoped>

</style>