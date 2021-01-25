<template>
  <nav data-role="ribbonmenu">
    <ul class="tabs-holder h-100">
      <li v-on:click="rpush('/')">
        <a href="#"><p class="topmenuitem">Home</p></a>
      </li>
      <li v-on:click="rpush('/models')">
        <a href="#"><p class="topmenuitem">Models</p></a>
      </li>
      <li v-on:click="rpush('/data')">
        <a href="#"><p class="topmenuitem">Data</p></a>
      </li>
      <li v-on:click="rpush('/specifyfit')">
        <a href="#"><p class="topmenuitem">Fit Topology</p></a>
      </li>
      <li v-on:click="rpush('/runfit')">
        <a href="#"><p class="topmenuitem">Run Fit</p></a>
      </li>
    </ul>
  </nav>

  <!--  <div id="nav">-->

  <!--  </div>-->

  <router-view />
</template>

<script>
export default {
  data() {
    return {};
  },
  methods: {
    rpush(to) {
      this.$router.push(to);
    }
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.topmenuitem {
  position: relative;
  top: 1px;
  font-size: 14px;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}

.window-caption > .title {
  margin-left: 5px;
}

:not(input):not(textarea),
:not(input):not(textarea)::after,
:not(input):not(textarea)::before,
:not(#code) {
  -webkit-user-select: none;
  user-select: none;
}

input,
button,
textarea,
:focus {
  outline: none;
}

button,
a {
  cursor: default;
}

.defaultcursor,
.select-input,
.default-icon-cross,
.dropdown-toggle,
.drop-container,
.select.input-normal,
.input-clear-button,
.remover,
.checkbox {
  cursor: default !important;
}
</style>
