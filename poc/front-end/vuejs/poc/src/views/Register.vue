<template>
  <section class="login-section">
    <div class="login-box">
      <h2 class="register-title">REGISTER</h2>

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
        <button type="button">
        </button>
      </div>

      <RouterLink to="/isRegisted">
        <button class="btn">Register</button>
      </RouterLink>

      <RouterLink to="/login">
        <button class="btn">login</button>
      </RouterLink>
    </div>
  </section>
</template>

<style>
.register-section {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.register-box {
  width: 100%;
  max-width: 400px;
  padding: 40px;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 45px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.register-title {
  font-size: 2rem;
  font-weight: 800;
  text-align: center;
  margin-bottom: 20px;
}

.input-field {
  width: 100%;
  padding: 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 1rem;
}

.btn {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 8px;
  font-weight: 800;
  color: white;
  background-color: #F18585;
  cursor: pointer;
  transition: background-color 0.2s;
  margin-top: 10px;
}

</style>
