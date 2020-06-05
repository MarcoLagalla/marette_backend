<template>
<div class="infocard">
        <h1>{{name}}</h1>
        <div class="divider"></div>
          <v-textarea class="descript"  dark :readonly='!admin' @input="edited= true" v-model="activity_description"></v-textarea>
          <v-btn v-if="admin" name="edit" :disabled="!edited" color="blue" @click="$emit('edited', activity_description)" class="editbutton">
            Modifica descrizione<i class="far fa-edit"></i>
          </v-btn>
  <button class="infoicon" @click="$refs.orarimodal.open()" >
    <i class="fas fa-info-circle"></i>
  </button>
    <sweet-modal ref="orarimodal">
        <base-orari>

        </base-orari>
    </sweet-modal>
        <ul class="orari">
          <li class="infos">
              {{category}}
          </li>
          <li class="infos">
            Aperto ora/Apre alle
          </li>
        </ul>
</div>
</template>
<script>

export default {
  props: {
    name: {
      type: String,
      required: true,
    },
    category: {
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
  .divider {
    width: 100px;
    background: var(--ming);
    height: 5px;
    margin: 20px 0;
    filter: blur(2px);
  }
  h1 {
    font-size: 1.5em;
    text-transform: capitalize;
    color: white;
    margin: 1vmax 0;
  }
  .infocard {
    position: relative;
  background: rgba(0,0,0,0.4);
padding: 1vmax;
    display: block;
    width: 100%;
    height: 400px;
    box-shadow: 0 0 10px black;
  }
  .descript {
    width: 50%;
    font-size: 0.9em;
  }
  .orari {
    position: absolute;
    bottom: 0;
    left: 0;
    margin: 10px;
    list-style-type: none;
    text-align: left;
    padding: 0;
  }
  .orari li {
    color: white;
    display: inline-block;
    font-size: 20px;
    padding: 10px;
  }
  .infoicon {
    position: absolute;
    top: 0;
    right: 0;
    margin: 10px;
    color: white;
    transition: 0.4s ease-in-out;
  }
  .infoicon:hover {
    color: limegreen;
  }
  i {
    font-size: 30px;
  }
</style>
