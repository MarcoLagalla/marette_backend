<template>
  <v-row >
    <v-dialog v-model="dialog" overlay-opacity="0.8" max-width="500">
      <template v-slot:activator="{ on }">
        <div class="rel">
          <button name="edit" class="managebutton" v-on="on" >
            Aggiungi immagine <i class="far fa-edit"></i>
          </button>
        </div>
      </template>
      <v-card class="pt-10 px-10 pb-4" justify="center">
        <br>
        <v-text-field rounded filled v-model="imagePrefill.name" label="Titolo*" type="text" required></v-text-field>
        <v-textarea rounded filled v-model="imagePrefill.description" label="Descrizione" type="text" ></v-textarea>

        <newPictureInput
          ref="background"
          @change="onChanged"
          :width="200"
          :height="200"
          size="3"
          :zIndex="0"
          :crop="true"
          :changeOnClick="true"
          :prefill="imagePrefill.image"
          accept="image/jpeg, image/png, image/gif"
          buttonClass="ui button primary"
          :customStrings="{
            upload: '<h1>Carica immagine</h1>',
            drag: 'Trascina qui la un immagine o clicca per selezionarla',
            change: 'Cambia foto',
          }">
        </newPictureInput>
        <v-btn color="green" :disabled="(image==='' || imagePrefill.name==='') && (!imagePrefill.edit || imagePrefill.name==='')" @click="submitImage" text>Salva immagine</v-btn>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>

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
            if(this.imagePrefill.edit && !this.passed) {
                this.dialog = true
                this.passed = true
            }
            if(this.passed && !this.dialog){
              this.passed = false
              this.imagePrefill.image= ''
              this.imagePrefill.name= ''
              this.imagePrefill.description= ''
              this.imagePrefill.edit= false
            }

        }

    }
</script>

<style scoped>
.managebutton {
  color: var(--ghostwhite);
  background: var(--darkslate);
  font-weight: bold;
  padding: 10px;
  border-radius: 25px;
}
</style>