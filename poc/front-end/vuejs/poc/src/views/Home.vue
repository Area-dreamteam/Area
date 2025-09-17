<template>
  <div class="container">
    <RouterLink to="/login" class="btn">Login</RouterLink>
    <RouterLink to="/register" class="btn">Register</RouterLink>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  gap: 20px;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
.btn {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background-color: #e60012;
  color: #fff;
  font-weight: 700;
  text-decoration: none;
  transition: transform .2s, background-color .2s;
}
.btn:hover { transform: scale(1.06); background-color: #ff1a1a; }
</style>
