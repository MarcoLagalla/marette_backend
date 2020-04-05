    <template>
      <v-card width="30vmax"
      class="mx-auto mt-2">
        <v-card-title>Registration form</v-card-title>
        <v-card-text>
          <div>
            <v-text-field
            v-model="username"
            :counter="10"
            :rules="nameRules"
             label="Username"
             required
             ></v-text-field>
            <v-text-field 
            label="Email" 
            v-model="email"
           :rules="[v => !!v || 'Email is required']"
            required
            ></v-text-field>
            <v-text-field 
            label="password" 
            v-model="password"
            type="password"
            :rules="[v => !!v || 'Password is required']"
            required
            ></v-text-field>
            <v-checkbox
             v-model="checkbox"
            :rules="[v => !!v || 'You must agree to continue!']"
             label="Do you agree?"
            required
            ></v-checkbox>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-btn 
          color="success"
          @click="registerUser({username: user.username, email: user.email, password: user.password})"
          >Register</v-btn>
        </v-card-actions>
      </v-card>
    </template>

<script>
    import { mapActions } from 'vuex'

    export default {
        name: "Regform",
        data () {
            return {
                user: {
                    username:'',
                    email: '',
                    password: '',
                    //password2: '',
                    //first_name: '',
                    //last_name: '',
                    //birth_date: '',
                    //cellphone_number: ''
                }

            }
        },

        /*data: () => ({
      valid: true,
      name: '',
      nameRules: [
        v => !!v || 'Name is required',
        v => (v && v.length <= 10) || 'Name must be less than 10 characters',
      ],
      email: '',
      emailRules: [
        v => !!v || 'E-mail is required',
        v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
      ],      
      checkbox: false,
    }),*/
        methods:
        {
            ...mapActions('user', ['registerUser']),

                
        }
        
      }
    
</script>