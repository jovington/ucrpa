<template>
  <div class="app-wrapper">
    <!-- Navbar Bootstrap -->
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
            <li class="nav-item">
              <router-link class="nav-link" to="/directorio">Directorio Operativo</router-link>
            </li>
            <li class="nav-item mt-2 mt-lg-0">
              <router-link class="btn btn-primary-custom w-100" to="/inscripcion">Certificación 2026</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <main class="router-view-container">
        <router-view />
    </main>

    <footer class="footer mt-auto py-4">
        <div class="container text-center">
            <p class="mb-0">&copy; 2026 UCRPA - Unidad Canina de Rescate del Principado de Asturias.</p>
        </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const isScrolled = ref(false);
const hasLogo = ref(true);

const handleScroll = () => {
    isScrolled.value = window.scrollY > 50;
};

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});
</script>

<style>
/* CSS ROOT & GLOBALS */
:root {
  --bg-color: #0B1120;
  --bg-soft: #1E293B;
  --brand-blue: #2088c2; 
  --brand-green: #156c36;
  --text-main: #F8FAFC;
  --text-muted: #E2E8F0; /* Color más claro para mejor contraste */
}

html {
  scroll-behavior: smooth;
}

body {
  margin: 0;
  padding: 0;
  background-color: var(--bg-color);
  color: var(--text-main);
  font-family: 'Inter', sans-serif;
  overflow-x: hidden;
}

.app-wrapper {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

.router-view-container {
    flex: 1;
}

/* NAVBAR CUSTOMIZATIONS PARA SOBREESCRIBIR BOOTSTRAP */
.navbar {
  height: auto;
  min-height: 90px;
  background: rgba(11, 17, 32, 0.4);
  backdrop-filter: blur(12px);
  transition: all 0.3s ease;
}

.navbar.scrolled {
  background: rgba(11, 17, 32, 0.95);
  border-bottom: 2px solid var(--brand-blue);
  box-shadow: 0 4px 20px rgba(0,0,0,0.4);
}

.brand-logo {
    height: 55px; 
    width: 55px;
    object-fit: contain;
}

.nav-link {
  color: var(--text-main) !important;
  font-weight: 500;
  font-size: 1rem;
  transition: color 0.2s;
  padding: 0.5rem 0 !important;
}

.nav-link:hover, .router-link-active {
  color: var(--brand-blue) !important;
}

.btn-primary-custom {
  background-color: var(--brand-green);
  color: white !important;
  font-weight: 700;
  border: none;
  border-radius: 8px;
  padding: 0.6rem 1.5rem;
  transition: all 0.2s ease;
}

.btn-primary-custom:hover {
  background-color: #1ca350;
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(21, 108, 54, 0.4);
}

/* Custom Hamburger Icon Color */
.custom-toggler {
    border-color: rgba(255,255,255,0.2) !important;
}
.custom-toggler .navbar-toggler-icon {
    background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'%3e%3cpath stroke='rgba%28255, 255, 255, 1%29' stroke-linecap='round' stroke-miterlimit='10' stroke-width='2' d='M4 7h22M4 15h22M4 23h22'/%3e%3c/svg%3e") !important;
}

.collapse.show, .collapsing {
    background: rgba(11, 17, 32, 0.98);
    padding: 1rem;
    border-radius: 12px;
    margin-top: 1rem;
    border: 1px solid rgba(255,255,255,0.05);
}

.text-muted {
  color: var(--text-muted) !important;
}

.footer {
  background: #080C17;
  color: var(--text-muted);
  border-top: 2px solid var(--brand-blue);
  font-size: 0.9rem;
}
</style>
