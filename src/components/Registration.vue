<template>
     <form>
        <div class="container">
            <h1>Registrati</h1>
            <p>Dammi dei bei dati per registrare un account.</p>
            <hr>

            <label for="username"><b>Username</b></label>
            <input v-model='user.username' type="text" placeholder="Inserire Username" id="username" name="username" required>

            <label for="email"><b>Email</b></label>
            <input v-model='user.email' type="text" placeholder="Inserire Email" id="email" name="email" required>

            <label for="psw"><b>Password</b></label>
            <input v-model='user.passowrd' type="password" placeholder="Inserire Password" id="psw" name="psw" required>

            <label for="psw-repeat"><b>Ripeti la Password</b></label>
            <input v-model='user.password2' type="password" placeholder="Ripetere Password" id="psw-repeat" name="psw-repeat" required>

            <label for="phone"><b>Numero di Telefono valido</b></label>
            <input v-model='user.cellphone_number' type="tel" placeholder="Inserire Numero di Telefono" id="phone" name="phone" required>

            <label for="first_name"><b>Nome</b></label>
            <input v-model='user.first_name' type="text" placeholder="Inserire Nome" id="first_name" name="first_name">

            <label for="last_name"><b>Cognome</b></label>
            <input v-model='user.last_name' type="text" placeholder="Inserire Cognome" id="last_name" name="last_name">

            <label for="birth_date"><b>Data di nascita</b></label>
            <input v-model='user.birth_date' type="date" placeholder="Inserire Data di Nascita" id="birth_date" name="birth_date">

            <hr>

            <p>Registrando un account accetti i nostri <router-link to="/termini">Terms & Privacy</router-link>.</p>
            <button type="submit" class="registerbtn">Registrati</button>
        </div>

        <div class="container signin">
            <p>Hai già un account? <a href="#">Dillo prima, coglione</a>.</p>
        </div>
    </form>
</template>

<script>
    export default {
        name: "Registration",
        data () {
            return {
                user: {
                    username:'',
                    email: '',
                    passowrd: '',
                    password2: '',
                    first_name: '',
                    last_name: '',
                    birth_date: '',
                    cellphone_number: ''
                }

            }
        }
    }
</script>

<style scoped>
     {box-sizing: border-box}

/* Add padding to containers */
.container {
  padding: 16px;
}

/* Full-width input fields */
input[type=text], input[type=password] , input[type=tel] , input[type=date] {
  width: 100%;
  padding: 15px;
  margin: 5px 0 22px 0;
  display: inline-block;
  border: none;
  background: #f1f1f1;
}

input[type=text]:focus, input[type=password], input[type=tel] , input[type=date] :focus {
  background-color: #ddd;
  outline: none;
}

/* Overwrite default styles of hr */
hr {
  border: 1px solid #f1f1f1;
  margin-bottom: 25px;
}

/* Set a style for the submit/register button */
.registerbtn {
  background-color: #4CAF50;
  color: white;
  padding: 16px 20px;
  margin: 8px 0;
  border: none;
  cursor: pointer;
  width: 100%;
  opacity: 0.9;
}

.registerbtn:hover {
  opacity:1;
}

/* Add a blue text color to links */
a {
  color: dodgerblue;
}

/* Set a grey background color and center the text of the "sign in" section */
.signin {
  background-color: #f1f1f1;
  text-align: center;
}

</style>