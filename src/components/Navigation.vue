<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
    <div class="container">
        <router-link to="/">Marette</router-link>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarResponsive">
            <ul class="navbar-nav ml-auto">
                <!--
                <li class="nav-item active">
                    <a class="nav-link" href="#">Home
                        <span class="sr-only">(current)</span>
                    </a>
                </li>
                -->

                    <div v-if="isAuthenticated" class="dropdown mb-0">
                        <!--img class="img-profile rounded-circle" style="width: 30px; height:30px;" src="{% static "webapp/img/avatar.svg" %}"-->
                        <button class="btn btn-outline-secondary btn-sm m-1 mb-0 dropdown-toggle text-white" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                            {{ username }}
                        </button>
                        <button @click="logout" class="btn btn-outline-secondary btn-sm m-1 mb-0 dropdown-toggle text-white" type="button"  data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
LogOut
                        </button>
                        <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                            <!--a class="dropdown-item" href="{% url 'Account:user-profile' user_id=user.id %}"><i class="fa fa-user p-2"></i>Profile</a>
                            <div class="dropdown-divider"></div>
                            <a class="dropdown-item" href="{% url 'Account:user-logout' %}"><i class="fa fa-sign-out p-2"></i>Logout</a-->
                        </div>
                    </div>
                    <template v-else>
                        <div class="dropdown mb-0">

                            <router-link to="/login" tag="button" class="btn btn-outline-secondary btn-sm m-1 mb-0 dropdown-toggle text-white" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                Login
                            </router-link>
                            <router-link to="/registration" tag="button" class="btn btn-outline-secondary btn-sm m-1 mb-0 dropdown-toggle text-white" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                Registrati
                            </router-link>
                            <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">

                            </div>
                        </div>
                        <li class="divider-vertical"></li>
                        <!--li class="nav-item"><a class="btn btn-secondary btn-sm m-1" href="{% url 'Account:business-signup' %}">Business Sign up</a></li>
                        <li class="nav-item"><a class="btn btn-secondary btn-sm m-1" href="{% url 'Account:user-signup' %}">Sign up</a></li-->
                    </template>
            </ul>
        </div>
    </div>
</nav>
</template>

<script>
    import {mapActions} from "vuex";

    export default {
        data () {
        return {
            name: "Navigation",
            }
        },
        methods:
        {
            ...mapActions('userAutentication', ['logout']),

        },

        computed:
            {
                username(){
                    return this.$store.getters['userAutentication/username']
                },
                isAuthenticated(){
                    return this.$store.getters['userAutentication/isAuthenticated']
                },

            }


    }
</script>

<style scoped>

</style>