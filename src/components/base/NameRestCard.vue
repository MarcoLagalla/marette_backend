<template>
<div class="infocard">
  <v-card dark class="mx-6 mt-12" height="60%" max-width="344" outlined color="rgba(0,0,0,0.8)">
    <v-list-item three-line>
      <v-list-item-content>
        <div class="overline mb-4"></div>
        <v-list-item-title class="title"><h1>{{name}}</h1></v-list-item-title>
          <v-textarea :readonly='!admin' @input="edited= true" v-model="activity_description"></v-textarea>
          <v-btn v-if="admin" name="edit" :disabled="!edited" color="blue" @click="$emit('edited', activity_description)" class="managebutton">
            Modifica descrizione<i class="far fa-edit"></i>
          </v-btn>
      </v-list-item-content>
    </v-list-item>
    <v-card-actions>
    </v-card-actions>
  </v-card>
</div>
</template>
<script>
export default {
  props: {
    name: {
      type: String,
      required: true,
    },
    description: {
      type: String,
      required: false,
      default: ''
    },
    admin: {
      type: Boolean,
      default: false,
    }
  },
  name: "NameRestCard",
  data: function () {
    return {
      edited: false,
      activity_description: this.description
    }
  },
}
</script>
<style scoped>
  .title {
    text-transform: capitalize;
  }
  h1 {
    font-size: 1.5em;
  }
</style>
