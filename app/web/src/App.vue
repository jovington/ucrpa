<template>
  <div class="app-wrapper">
    <!-- Navbar Institucional con Autenticación -->
    <nav class="navbar navbar-expand-lg fixed-top" :class="{ 'scrolled': isScrolled }">
      <div class="container-xl">
        <router-link class="navbar-brand d-flex align-items-center gap-2" to="/">
          <img src="/logo.png" alt="UCRPA Logo" class="brand-logo" v-if="hasLogo" @error="hasLogo = false" />
          <span class="logo-icon text-white" v-else>🐾</span>
          <span class="logo-text text-white fw-bold">UCRPA</span>
        </router-link>
        
        <button class="navbar-toggler custom-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
          <ul class="navbar-nav align-items-lg-center gap-lg-3 mt-3 mt-lg-0">
            <li class="nav-item">
              <router-link class="nav-link" to="/">Inicio</router-link>
            </li>
            
            <!-- Enlaces Protegidos -->
            <template v-if="isLoggedIn">
                <li class="nav-item">
                  <router-link class="nav-link" to="/directorio">Directorio</router-link>
                </li>
                <li class="nav-item">
                  <router-link class="btn btn-outline-brand ms-lg-2" to="/inscripcion">Certificación 2026</router-link>
                </li>
                <li class="nav-item ms-lg-2 mt-2 mt-lg-0">
                  <button @click="logout" class="btn btn-danger-custom">Cerrar Sesión</button>
                </li>
            </template>
            
            <!-- Enlaces Públicos -->
            <template v-else>
                <li class="nav-item">
                  <router-link class="nav-link" to="/login">Acceder</router-link>
                </li>
                <li class="nav-item mt-2 mt-lg-0">
                  <router-link class="btn btn-primary-custom w-100" to="/registro">Registrarse</router-link>
                </li>
            </template>
          </ul>
        </div>
      </div>
    </nav>

    <main class="router-view-container">
        <router-view />
    </main>

    <footer class="footer mt-auto py-4">
        <div class="container text-center">
            <p class="mb-0 text-white">&copy; 2026 UCRPA - Unidad Canina de Rescate del Principado de Asturias.</p>
            <p class="small text-muted mt-2" v-if="isLoggedIn">Sesión activa: {{ userGroup }}</p>
        </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const isScrolled = ref(false);
const hasLogo = ref(true);
const isLoggedIn = ref(false);
const userGroup = ref('');

const checkAuth = () => {
    isLoggedIn.value = !!localStorage.getItem('token');
    userGroup.value = localStorage.getItem('agrupacion') || '';
};

const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('agrupacion');
    localStorage.removeItem('user_email');
    checkAuth();
    router.push('/login');
};

const handleScroll = () => {
    isScrolled.value = window.scrollY > 50;
};

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
  checkAuth();
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});
</script>

<style>
/* ... (Estilos Base mantenidos) ... */
:root {
  --bg-color: #0B1120;
  --bg-soft: #1E293B;
  --brand-blue: #2088c2; 
  --brand-green: #156c36;
  --text-main: #FFFFFF;
  --text-muted: #FFFFFF;
}

body {
  background-color: var(--bg-color);
  color: var(--text-main);
  font-family: 'Inter', sans-serif;
}

.navbar {
  min-height: 90px;
  background: rgba(11, 17, 32, 0.4);
  backdrop-filter: blur(12px);
  transition: all 0.3s ease;
}

.navbar.scrolled {
  background: rgba(11, 17, 32, 0.95);
  border-bottom: 2px solid var(--brand-blue);
}

.btn-primary-custom {
  background-color: var(--brand-green);
  color: white !important;
  font-weight: 700;
  border: none;
  border-radius: 8px;
  padding: 0.6rem 1.5rem;
}

.btn-outline-brand {
    border: 2px solid var(--brand-blue);
    color: white !important;
    font-weight: 600;
    border-radius: 8px;
    padding: 0.5rem 1.2rem;
}

.btn-danger-custom {
    background-color: transparent;
    color: #F87171 !important;
    border: 1px solid #F87171;
    font-weight: 500;
    border-radius: 8px;
    padding: 0.4rem 1rem;
}
.btn-danger-custom:hover {
    background-color: #F87171;
    color: white !important;
}

.nav-link {
  color: white !important;
  font-weight: 500;
}
.nav-link:hover, .router-link-active:not(.navbar-brand) {
  color: var(--brand-blue) !important;
}

.custom-toggler .navbar-toggler-icon {
    background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'%3e%3cpath stroke='rgba%28255, 255, 255, 1%29' stroke-linecap='round' stroke-miterlimit='10' stroke-width='2' d='M4 7h22M4 15h22M4 23h22'/%3e%3c/svg%3e") !important;
}

.footer {
  background: #080C17;
  border-top: 2px solid var(--brand-blue);
}
</style>
