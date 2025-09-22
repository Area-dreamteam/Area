<template>
  <div class="container">
    <RouterLink to="/login" class="btn">Login</RouterLink>
    <RouterLink to="/register" class="btn">Register</RouterLink>
  </div>
</template>

<style>
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
}
</style>
