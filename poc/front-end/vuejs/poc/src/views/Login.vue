<template>
  <section class="login-section">
    <div class="login-box">
      <h2 class="login-title">LOGIN</h2>

      <input
        type="email"
        placeholder="Email"
        class="input-field"
      />

      <div>
        <input
          type="password"
          placeholder="Password"
          class="input-field"
        />
        <button type="button" class="icon-btn">
        </button>
      </div>

      <RouterLink to="/isLogged">
        <button class="btn">Login</button>
      </RouterLink>

      <RouterLink to="/register">
        <button class="btn">Register</button>
      </RouterLink>
    </div>
  </section>
</template>

<style>
.login-section {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-box {
  width: 100%;
  max-width: 400px;
  padding: 40px;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 45px;
}

.login-title {
  font-size: 2.5rem;
  font-weight: 800;
  text-align: center;
  margin-bottom: 20px;
  color: black;
}

.input-field {
  width: 100%;
  padding: 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 1rem;
}

.icon-btn {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  cursor: pointer;
  color: #6b7280;
}

.btn {
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  font-weight: 800;
  color: white;
  background-color: blue;
  cursor: pointer;
  transition: background-color 0.2s;
  margin-top: 10px;
}
</style>
