<template>
<v-row>
  <v-col>
    <router-link v-for="(name, i) in items" :key="i" :to="'#'+name" :ripple="false" min-width="96" tag="button"><a>{{ name }}</a></router-link>
  </v-col>
</v-row>
</template>

<script>
export default {
  name: "RestMenu",
  props: ['items']
}
</script>

<style scoped>
a {
  text-decoration: none;
  scroll-behavior: smooth;
}

.ul {
  margin: 0;
  padding: 0;
  display: flex;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.ul .li {
  list-style: none;
  margin: 0 15px;
}

@import url('https://fonts.googleapis.com/css2?family=B612&display=swap');

.ul .li a {
  padding-left: 5px;
  position: relative;
  display: block;
  text-align: center;
  line-height: 45px;
  border: solid rgba(255, 255, 255, 0) 4px;
  font-size: 1.5em;
  font-weight: bold;
  font-family: 'B612', sans-serif;
  text-transform: ;
  color: #666;
  transition: .4s;
}

.ul .li a::before {
  content: '';
  position: absolute;
  margin-left: -5px;
  margin-bottom: -5px;
  border-color: white;
  border-style: solid;
  border-width: 3px 0 0 0;
  height: 0;
  bottom: 0;
  width: 0;
  transition: .4s;
}

.ul .li a:hover::before {
  transition: ease .4s;
  content: '';
  position: absolute;
  border-color: #af473c;
  border-style: solid;
  border-width: 3px 0 0 0;
  height: 0.5em;
  bottom: 0;
  width: 100%;
  filter: blur(2px);
}

.ul .li a:hover {
  transition: ease .4s;
  text-shadow: 0 0 8px black;
  color: white
}
</style>
