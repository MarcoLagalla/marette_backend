<template>
  <div>
    <v-alert :value="pswSuccess !== ''" type="success">{{pswSuccess}}</v-alert>
    <v-alert :value="pswError !== ''" type="error" >{{pswError}}</v-alert>

    <v-card-actions>
        <v-btn class="managebutton" @click="show = !show" text>Modifica password
            <v-icon>{{ show ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
        </v-btn>
    </v-card-actions>
    <v-expand-transition>
        <div v-show="show">
            <v-divider></v-divider>
            <v-form @submit.prevent="change_psw">
                <v-row align="center" class="ma-0 mt-8" justify="center">
                    <v-col cols="12" sm="6" md="4">
                        <v-text-field light :error-messages="errors.old_password"
                                      @change="errors.old_password=''"  v-model='old_password'
                                      type="password"
                                      placeholder=" Inserire vecchia password"
                                      id="old_password"
                                      name="old_password" required>
                        </v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                        <v-text-field light :rules="passwordRules"
                                      :error-messages="errors.password"
                                      @change="errors.password=''"  v-model='new_password'
                                      type="password"
                                      placeholder=" Inserire nuova password"
                                      id="new_password" name="new_password" required>
                        </v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                        <v-text-field light :rules="password2Rules"
                                      :error-messages="errors.password"
                                      @change="errors.password=''" v-model='new_password2'
                                      type="password"
                                      placeholder=" Reinserire nuova password"
                                      id="new_password2" name="new_password2" required>
                        </v-text-field>
                    </v-col>
                </v-row>
                <div class="regbtn2">
                    <div class="center">
                        <button type="submit" class="managebutton2">Modifica Password
                        </button>
                    </div>
                </div>
            </v-form>
        </div>
    </v-expand-transition>
  </div>
</template>

<script>
  import {mapActions} from "vuex";

  export default {
    name: "ChangePassword",
    data() {
      return {
        show: false,
        old_password: '',
        new_password: '',
        new_password2: '',
        passwordRules: [
            v => !!v || 'Campo obbligatorio',
            v => v !== this.old_password || "La nuova password deve essere diversa dalla vecchia"
        ],
        password2Rules: [
            v => !!v || 'Campo obbligatorio',
            v => v === this.new_password || "Le password devono combaciare"
        ],
        pswSuccess: '',
        pswError: '',
      }
    },
    methods: {
      ...mapActions('userProfile', ['changePassword']),
      change_psw: function () {
          this.changePassword({
              old_password: this.old_password,
              new_password: this.new_password,
              new_password2: this.new_password2,

          }).then(messaggio => {
              this.show = false
              this.pswError = ''
              this.pswSuccess = messaggio
          }).catch(() => {
              this.pswError = 'Errore!'
              this.pswSuccess = ''
          })

      }
    },
    computed: {
        errors() {
            return this.$store.getters['userProfile/errors']
        },
    },
  }
</script>

<style scoped>
  .regbtn2 {
      padding: 10px;
      margin-bottom: 10px;
      display: flex;
      align-items: left;
      justify-content: left;
  }

  .password_btn {
      background-color: var(--emerald);
      color: white;
      border: inset var(--emerald) 2px !important;
      padding: 16px 20px;
      margin: 4px 0;
      border: none;
      cursor: pointer;
      width: 100%;
      opacity: 0.8;
      transition: all 0.3s cubic-bezier(.25, .8, .25, 1);
      border-radius: 10px;
  }

  .password_btn:hover {
      opacity: 1;
      box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22);
  }

</style>