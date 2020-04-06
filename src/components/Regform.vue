    <template>
      <v-card 
      width="30vmax"
      class="mx-auto mt-0">
        <v-card-title>Registration form</v-card-title>
        
        <v-card-text>
          <div>
            <v-text-field
            id="username"
            v-model="username"
             label="Username"
             required
             ></v-text-field>
            <v-text-field 
            id="email"
            label="Email" 
            v-model="email"
            required
            ></v-text-field>
            <v-text-field 
            id="password"
            label="Insert password" 
            v-model="password"
            type="password"
            required
            ></v-text-field>
            <v-text-field 
            id="password2"
            label="Confirm your password" 
            v-model="password2"
            type="password"
            required
            ></v-text-field>
            <v-text-field 
            id="first_name"
            label="First name" 
            v-model="first_name"
            type="name"
            
            ></v-text-field>
            <v-text-field 
            id="last_name"
            label="Last name" 
            v-model="last_name"
            type="name"
            
            ></v-text-field>
            <v-text-field 
            id="birth_date"
            label="Birth date" 
            v-model="birth_date"
            type="date"
            
            ></v-text-field>
            <v-text-field
            id="phone"
            name="phone"
            label="Phone number" 
            v-model="phone"
            type="tel"
            ></v-text-field>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-btn 
          color="success"
          @click="submit"
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
                username:'',
                email: '',
                password: '',
                password2: '',
                first_name: '',
                last_name: '',
                birth_date: '',
                phone: '',
            }
        },
        methods:
        {
            ...mapActions('user', ['registerUser']),
            submit: function () {
                if (this.disable)
                    alert("Inserisci tutti i campi obbligatori");
                else
                {
                    if (!this.first_name && !this.last_name)
                        this.registerUser({
                            username: this.username,
                            email: this.email,
                            password: this.password,
                            password2: this.password2,
                            phone: this.phone
                        });
                    else
                        this.registerUser({
                            username: this.username,
                            email: this.email,
                            password: this.password,
                            password2: this.password2,
                            phone: this.phone,
                            first_name: this.first_name,
                            last_name: this.last_name,
                            birth_date: this.birth_date
                        });
                }
            },
        },
        computed:
            {
                disable: function() {
                    return !this.username || !this.email || !this.password || !this.password2 || !this.phone
                },
                response(){
                    return this.$store.state.user.result
                }
            }
    }
    
</script>




