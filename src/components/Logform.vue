    <template>
      <v-card width="30vmax"
      class="mx-auto mt-2">
        <v-card-title>Login form</v-card-title>
                    <h2 v-if="response.status === 200">Utente Collegato!</h2>
        <v-card-text>
          <div>
            <v-text-field
            v-model="email"
            type="email"
            label="Email"
            required
            ></v-text-field>
            <v-text-field 
            label="password" 
            v-model="password"
            type="password"
            :rules="[v => !!v || 'Password is required']"
            required
            ></v-text-field>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-btn 
          color="success"
          @click="submit"
          >Login</v-btn>
        </v-card-actions>
      </v-card>
    </template>

<script>
     import { mapActions } from 'vuex'

      export default {
        name: "Logform",
        data () {
            return {
                    email:'',
                    password:''
            }
        },
        methods:
        {
            ...mapActions('user', ['signIn']),
            submit: function () {
                if (!this.email || !this.password)
                {
                    alert("Inserisci tutti i campi obbligatori");
                }
                else
                {
                    this.signIn({
                    email: this.email,
                    password: this.password,
                    });
                }
            }
        },
        computed:
            {
                response(){
                    return this.$store.state.user.result
                }
            }
    }
    
</script>