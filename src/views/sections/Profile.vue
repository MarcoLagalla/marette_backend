<template>
    <div class="body">
  <v-container>
    <router-link tag="button" v-if="isBusiness" to="newRestaurant">Aggiungi ristorante</router-link>


      <v-row dense>
      <v-col cols="12">
        <v-card
        color="#385F73"
        dark
        >
        <v-card-title class="headline">Profilo utente</v-card-title>

        <v-card-subtitle>
            <p v-for="(campo, i) in user" :key="i" >{{i.replace(/_/g , ' ')}} : {{campo}}</p>
        </v-card-subtitle>

        <v-card-actions>
          <v-btn @click="show = !show" text>Modifica password<v-icon>{{ show ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon></v-btn>
        </v-card-actions>
        <v-expand-transition>
          <div v-show="show">
            <v-divider></v-divider>

            <v-form @submit.prevent="change_psw">
              <v-row
              align="center"
              class="ma-0 mt-8"
              justify="center"
              >
              <v-col cols="12" sm="6" md="4">
              <v-text-field solo background-color="#486F83" :error-messages="errors.old_password" @change="errors.old_password=''"  v-model='old_password' type="password" placeholder=" Inserire vecchia password" id="old_password" name="old_password" required></v-text-field>
</v-col><v-col cols="12" sm="6" md="4">
              <v-text-field solo background-color="#486F83" v-model='new_password' type="password" placeholder=" Inserire nuova password" id="new_password" name="new_password" required></v-text-field>

            </v-col><v-col cols="12" sm="6" md="4">
              <v-text-field solo background-color="#486F83"  v-model='new_password2' type="password" placeholder=" Reinserire nuova password" id="new_password2" name="new_password2" required></v-text-field>
            </v-col>
            </v-row><div class="regbtn2">
                <div class="center">
              <button type="submit" class="password_btn" >Modifica Password</button>
            </div>
        </div>
            </v-form>
          </div>
        </v-expand-transition>
      </v-card>
    </v-col>

    <v-col
    v-for="(item, i) in items"
    :key="i"
    cols="12"
    >
    <v-card
    :color="item.color"
    dark
    >
    <div class="d-flex flex-no-wrap justify-space-between">
      <div>
        <v-card-title
        class="headline"
        v-text="item.title"
        ></v-card-title>

        <v-card-subtitle v-text="item.artist"></v-card-subtitle>
      </div>

      <v-avatar
      class="ma-3"
      size="125"
      tile
      >
      <v-img :src="item.src"></v-img>
    </v-avatar>
  </div>
</v-card>
</v-col>
</v-row>
</v-container>
</div>
</template>

<script>
import Heading from '@/mixins/heading'
import { mapActions } from 'vuex'

export default {
  name: "Profile",

  mixins: [Heading],

  data() {
    return {
      old_password: '',
      new_password: '',
      new_password2: '',
      show: false,
      items: [
        {
          color: '#1F7087',
          src: 'https://cdn.vuetifyjs.com/images/cards/docks.jpg',
          title: 'Ristorante 1',
          artist: '',
        },
        {
          color: '#952175',
          src: "https://cdn.vuetifyjs.com/images/cards/docks.jpg",
          title: 'Ristorante 2',
          artist: '',
        },
      ],
    }
  },
  methods:
  {
    ...mapActions('userProfile', ['changePassword']),
    change_psw: function () {
      this.changePassword({
        old_password: this.old_password,
        new_password: this.new_password,
        new_password2: this.new_password2,

      }).then( messaggio => {

        alert(messaggio)

      })

    }
  },
  computed:
  {
    user() {
      return this.$store.getters['userProfile/user']
    },
    user_private() {
      return this.$store.getters['userProfile/user_private']
    },
    errors(){
      return this.$store.getters['userProfile/errors']
    },
    isBusiness(){
        return this.$store.getters['userProfile/isBusiness']
      }
  },
}
</script>

<style scoped>
.body {
  /*background: linear-gradient(to bottom, #aaffa9, #11ffbd)!important;*/
  background:#e1e1f1;
}

.regbtn2{
    padding: 10px;
    margin-bottom: 10px;
  display: flex;
  align-items: left;
  justify-content: letf;
}

.password_btn {
  background-color: #4CAF50;
  color: white;
  border: inset #4CAF50 2px!important;
  padding: 16px 20px;
  margin: 4px 0;
  border: none;
  cursor: pointer;
  width: 100%;
  opacity: 0.8;
  transition: 0.5s;
  border-radius: 10px;
}
.password_btn:hover {
  opacity:1;
  box-shadow: 0 0 10px grey;
}
</style>
