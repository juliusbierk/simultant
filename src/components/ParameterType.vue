<template>
  {{ name }}
</template>

<script>
export default {
  name: "ParameterType",
  props: {
    name: String,
    type: String,
    id: String
  }
};
</script>

<style scoped></style>
