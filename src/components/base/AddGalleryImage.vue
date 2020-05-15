<template>
  <v-row >
    <v-dialog v-model="dialog" overlay-opacity="0.8" >
      <template v-slot:activator="{ on }">
        <div class="rel">
          <v-btn name="edit" color="blue" v-on="on"  class="managebutton">
            Aggiungi immagine <i class="far fa-edit"></i>
          </v-btn>
        </div>
      </template>
      <v-card justify="center">

        <v-text-field v-model="imagePrefill.name" label="Titolo*" type="text" required></v-text-field>
        <v-textarea v-model="imagePrefill.description" label="Descrizione" type="text" ></v-textarea>

        <picture-input
          ref="background"
          @change="onChanged"
          :width="400"
          :height="400"
          size="3"
          :zIndex="0"
          :crop="true"
          :changeOnClick="true"
          :prefill="imagePrefill.image"
          accept="image/jpeg, image/png, image/gif"
          buttonClass="ui button primary"
          :customStrings="{
          upload: '<h1>Carica immagine</h1>',
          drag: 'Trascina qui la un immagine o clicca per selezionarla'}">
        </picture-input>
        <v-btn color="green" :disabled="(image==='' || imagePrefill.name==='') && (!imagePrefill.edit || imagePrefill.name==='')" @click="submitImage" text>Salva immagine</v-btn>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>

    import PictureInput from "vue-picture-input";

    export default {
        name: "AddGalleryImage",
        props: {
          imagePrefill: {
            type: Object,
            required: false,
            default:() => ({
              image: '',
              name: '',
              description: '',
              edit: false
            })
          }
        },
        components: {
            PictureInput,
        },
        data: function () {
          return {
            image: '',
            dialog: false,
              passed: false,
          }
        },
        methods: {
            onChanged() {
                if (this.$refs.background.file) {
                    this.image = this.$refs.background.file;
                } else {
                    console.log("Old browser. No support for Filereader API");
                }
            },
            submitImage() {
                const data = {
                  name: this.imagePrefill.name,
                  description: this.imagePrefill.description
                };
                const formData = new FormData();
                formData.append('data',JSON.stringify(data));
                formData.append('image',this.image);
                this.$emit('added', formData)
            }
        },
        updated() {
            console.log(this.imagePrefill.edit && !this.passed)
            if(this.imagePrefill.edit && !this.passed) {
                this.dialog = true
                this.passed = true
            }
            if(this.passed && !this.dialog)
                this.passed = false
        }

    }
</script>

<style scoped>

</style>