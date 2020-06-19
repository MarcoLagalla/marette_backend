<template>
  <v-row >
    <v-dialog v-model="active" overlay-opacity="0.8" >
      <template v-slot:activator="{ on }">

          <button name="edit" v-on="on"  class="managebtn">
             <i class="far fa-edit"></i>
          </button>

        </template>
        <v-card justify="center">
          <newPictureInput
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
              drag: 'Trascina qui la un immagine di profilo o clicca per selezionarla',
              change: 'Cambia foto',
            }">
          </newPictureInput>
          <v-btn color="green" @click="submitImage" text>Salva immagine</v-btn>
        </v-card>
    </v-dialog>
  </v-row>
</template>

<script>

    export default {
        name: "AddHomeImage",
        props: ['imageUrl'],
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
  .managebtn {
    width: 50px;
    margin: 0;
    border: solid 0.5px grey;

    padding: 10px;
    background: rgba(250,250,250,0.8);
    text-transform: uppercase;
    transition: 0.3s ease-in-out;
  }
  .managebtn:hover {
    background: rgba(250,250,250,1);
  }
</style>