<template>
  <nav data-role="ribbonmenu">
    <ul class="tabs-holder h-100">
      <li v-on:click="rpush('/')" :class="{ active: routeName === 'Home' }">
        <a href="#"><p class="topmenuitem">Home</p></a>
      </li>
      <li
        v-on:click="rpush('/models')"
        :class="{ active: routeName === 'Models' }"
      >
        <a href="#"><p class="topmenuitem">Models</p></a>
      </li>
      <li v-on:click="rpush('/data')" :class="{ active: routeName === 'Data' }">
        <a href="#"><p class="topmenuitem">Data</p></a>
      </li>
      <li
        v-on:click="rpush('/specifyfit')"
        :class="{ active: routeName === 'SpecifyFit' }"
      >
        <a href="#"><p class="topmenuitem">Fit Topology</p></a>
      </li>
      <li
        v-on:click="rpush('/runfit')"
        :class="{ active: routeName === 'RunFit' }"
      >
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
  },
  computed: {
    routeName() {
      return this.$route.name;
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
.switch,
.check,
.check::after {
  cursor: default !important;
}
</style>
