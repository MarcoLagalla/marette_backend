<template>
  <header class="header" role="banner">
    <h1 class="logo">
      <a href="#"> <span>Categorie</span></a>
    </h1>
    <div class="nav-wrap">
      <nav class="main-nav" role="navigation">
        <ul class="unstyled list-hover-slide">
          <li><a href="#">Pizze</a></li>
          <li><a href="#">Bevande</a></li>
          <li><a href="#">Menu</a></li>
          <li><a href="#">Vegan</a></li>
        </ul>
      </nav>

    </div>
  </header>
</template>

<script>
  export default {
    name: 'BaseMenuCat',

    inheritAttrs: false,


  }
</script>
<style scoped>
*, :before, :after {
box-sizing: border-box;
}

.unstyled {
list-style: none;
padding: 0;
margin: 0;
}
.unstyled a {
text-decoration: none;
}

.list-inline {
overflow: hidden;
}
.list-inline li {
float: left;
}

.header {
position: relative;
left: 0;
top: 0;

width: 17.5em;
background: #35302D;
}

.logo {
text-transform: ;
font: 300 2em ;
text-align: center;
padding: 0;
margin: 0;
}
.logo a {
display: block;
padding: 1em 0;
color: #DFDBD9;
text-decoration: none;
transition: .15s linear color;
}
.logo a:hover {
color: #fff;
}
.logo a:hover span {
color: #DF4500;
}
.logo span {
font-weight: 700;
transition: .15s linear color;
}

.main-nav ul {
border-top: solid 1px #3C3735;
}
.main-nav li {
border-bottom: solid 1px #3C3735;
}
.main-nav a {
padding: 1.1em 0;
color: #DFDBD9;
font: 400 1.125em;
text-align: center;
text-transform: ;
}
.main-nav a:hover {
color: #fff;
}

.social-links {
border-bottom: solid 1px #3C3735;
}
.social-links li {
width: 25%;
border-left: solid 1px #3C3735;
}
.social-links li:first-child {
border: none;
}
.social-links a {
display: block;
height: 5.5em;
text-align: center;
color: #3C3735;
font: 0.75em/5.5em "Source Sans Pro", Helvetica, Arial, sans-serif;
}
.social-links a:hover {
color: #DFDBD9;
}

.list-hover-slide li {
position: relative;
overflow: hidden;
}
.list-hover-slide a {
display: block;
position: relative;
z-index: 1;
transition: .35s ease color;
}
.list-hover-slide a:before {
content: '';
display: block;
z-index: -1;
position: absolute;
left: -100%;
top: 0;
width: 100%;
height: 100%;
border-right: solid 5px #DF4500;
background: #3C3735;
transition: .35s ease left;
}
.list-hover-slide a.is-current:before, .list-hover-slide a:hover:before {
left: 0;
}

</style>
