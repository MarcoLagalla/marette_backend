<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" max-width="500px">
      <template v-slot:activator="{ on }">
        <div class="rel">
          <button class="btn-6" v-on="on"><span>Login</span></button></div>
        </template>
        <v-card>
          <v-form @submit.prevent="login" class="container">
            <h1>MEMBER LOGIN</h1>
            <p class="error" v-if="errors.error" id="error">{{errors.error[0]}}</p>
            <div class="regbtn">
              <v-text-field prepend-inner-icon="mdi-account" solo v-model='email' :error-messages="errors.email" @change="errors.email=''" type="email" placeholder="Inserire Email" id="email" name="email" required>
              </v-text-field>
            </div>
            <div class="regbtn">
              <v-text-field prepend-inner-icon="mdi-key" solo v-model='password' :error-messages="errors.password" @change="errors.password=''" type="password" placeholder="Inserire Password" id="psw" name="psw" required>
              </v-text-field>
            </div>
            <div class="regbtn2">
              <div class="center">
                <button class="btn" type="submit">
                  <svg width="180px" height="60px" viewBox="0 0 180 60" class="border">
                    <polyline points="179,1 179,59 1,59 1,1 179,1" class="bg-line" />
                    <polyline points="179,1 179,59 1,59 1,1 179,1" class="hl-line" />
                  </svg>
                  <span>Login</span>
                </button>
              </div>
            </div>
            <v-card-text @click="dialog=false"><a style="color:white" href="#">
              <router-link to="/resetpass" >Hai dimenticato la password? </router-link>
            </a></v-card-text>
          </v-form>
        </v-card>
      </v-dialog>
    </v-row>
  </template>
  <script>
  // Mixins
  import Heading from '@/mixins/heading'
  import {
    mapActions
  } from 'vuex'
  export default {
    name: 'BaseForm',
    mixins: [Heading],
    data: () => ({
      dialog: false,
      email: '',
      password: ''
    }),
    methods: {
      ...mapActions('userAuthentication', ['signIn']),
      login: function() {
        this.signIn({
          email: this.email,
          password: this.password,
        })
      }
    },
    computed: {
      status() {
        return this.$store.getters['userAuthentication/status']
      },
      errors() {
        return this.$store.getters['userAuthentication/errorsL']
      }
    }
  }
  </script>
  <style scoped>
  {
    box-sizing: border-box
  }
  /* Add padding to containers */
  .rel {
    padding: 10px;
  }
  h1 {
    text-align: center;
    margin-bottom: 5%;
    color: white;
  }
  .v-text-field {
    max-width: 60%;
    border-radius: 25px;
    background-color: inherit;
  }
  .regbtn2 {
    padding: 10px;
    margin: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .regbtn {
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .v-card-text {
    text-align: center;
  }
  .v-dialog {
    border-radius: 10px;
  }
  .v-card {
    background: #3c3c3c;
    opacity: 0.9
  }
  .center {
    width: 180px;
    height: 60px;
    position: absolute;
  }
  .btn {
    width: 180px;
    height: 60px;
    cursor: pointer;
    background: #626e60;
    border: 1px solid white;
    outline: none;
    transition: 1s ease-in-out;
  }
  svg {
    position: absolute;
    left: 0;
    top: 0;
    fill: none;
    stroke: #fff;
    stroke-dasharray: 150 480;
    stroke-dashoffset: 150;
    transition: 1s ease-in-out;
  }
  .btn:hover {
    transition: 1s ease-in-out;
    background: #628e60;
  }
  .btn:hover svg {
    stroke-dashoffset: -480;
  }
  .btn span {
    color: white;
    font-size: 18px;
    font-weight: 600;
  }
  .btn-6 {
    display: inline-block;
    position: relative;
    border-radius: 2px;
    background: none;
    border: none;
    color: #fff;
    font-size: 18px;
    cursor: pointer;
    box-shadow: 0 0 2px black;
    transition: all 0.2s linear;
    background: #2F4F4F;
  }
  .btn-6:hover {
    color: #666;
    transition: all 0.2s linear;
    background: #C0C0C0;
    box-shadow: 0 0 6px black;
  }
  span {
    display: block;
    padding: 5px 20px;
    font-weight: ;
    letter-spacing: 5px;
    text-transform: uppercase;
  }
  .btn-6::before,
  .btn-6::after {
    content: "";
    width: 0;
    height: 2px;
    position: absolute;
    transition: all 0.2s linear;
    background: #2F4F4F;
    filter: blur(2px);
  }
  span::before,
  span::after {
    content: "";
    width: 2px;
    height: 0;
    position: absolute;
    transition: all 0.2s linear;
    background: #2F4F4F;
    filter: blur(2px);
  }
  .btn-6:hover::before,
  .btn-6:hover::after {
    width: 100%;
  }
  .btn-6:hover span::before,
  .btn-6:hover span::after {
    height: 100%;
  }
  .btn-6::before {
    left: 50%;
    top: 0;
    transition-duration: 0.4s;
  }
  .btn-6::after {
    left: 50%;
    bottom: 0;
    transition-duration: 0.4s;
  }
  .btn-6 span::before {
    left: 0;
    top: 50%;
    transition-duration: 0.4s;
  }
  .btn-6 span::after {
    right: 0;
    top: 50%;
    transition-duration: 0.4s;
  }
  .btn-6:hover::before,
  .btn-6:hover::after {
    left: 0;
  }
  .btn-6:hover span::before,
  .btn-6:hover span::after {
    top: 0;
  }
  </style>
