<template>
  <section class="login-section">
    <div class="login-box">
      <h2 class="login-title">LOGIN</h2>

      <input
        type="email"
        placeholder="Email"
        class="input-field"
      />

      <div class="input-group">
        <input
          type="password"
          placeholder="Password"
          class="input-field"
        />
        <button type="button" class="icon-btn">
          <!-- Icône d’œil par ex si tu veux -->
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

<style scoped>
/* Section principale avec fond image */
.login-section {
  min-height: 100vh;
  background: url('/BackGround_Rotate.jpg') center/cover no-repeat;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

/* Box blanche translucide */
.login-box {
  width: 100%;
  max-width: 400px;
  padding: 40px;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 45px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Titre */
.login-title {
  font-size: 2.5rem;
  font-weight: 800;
  text-align: center;
  margin-bottom: 20px;
  color: #F18585;
  font-family: 'Montserrat', sans-serif;
}

/* Champs */
.input-field {
  width: 100%;
  padding: 12px;
  border: 1px solid #d1d5db; /* gris clair */
  border-radius: 8px;
  font-size: 1rem;
}
.input-field:focus {
  outline: none;
  border-color: #F18585;
  box-shadow: 0 0 0 2px rgba(241, 133, 133, 0.5);
}

/* Group input + bouton (ex: œil pour mot de passe) */
.input-group {
  position: relative;
}
.icon-btn {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  cursor: pointer;
  color: #6b7280; /* gris */
}

/* Boutons */
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
.btn:hover {
  background-color: #e07070;
}
</style>
