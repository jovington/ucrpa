<template>
  <div class="app-wrapper">
    <!-- Navbar Institucional con Router -->
    <nav class="navbar" :class="{ 'scrolled': isScrolled }">
      <div class="nav-content">
        <router-link to="/" class="brand" style="text-decoration:none;">
          <img src="/logo.png" alt="UCRPA Logo" class="brand-logo" v-if="hasLogo" @error="hasLogo = false" />
          <span class="logo-icon" v-else>🐾</span>
          <span class="logo-text">UCRPA</span>
        </router-link>
        
        <div class="links d-none-mobile">
          <router-link to="/">Inicio</router-link>
          <router-link to="/directorio">Directorio Operativo</router-link>
          <!-- El botón está resaltado gracias a unas clases en styles globales -->
          <router-link to="/inscripcion" class="btn-primary">Certificación 2026</router-link>
        </div>
      </div>
    </nav>

    <main class="router-view-container">
        <!-- Renderiza la vista según la URL -->
        <router-view />
    </main>

    <!-- Footer -->
    <footer class="footer">
        <p>&copy; 2026 UCRPA - Unidad Canina de Rescate del Principado de Asturias.</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const isScrolled = ref(false);
const hasLogo = ref(true); // Controla si la imagen cargó exitosamente

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
/* PALETA DE COLORES INSTITUCIONAL SEGÚN LOGO OFICIAL */
:root {
  --bg-color: #0B1120;
  --bg-soft: #1E293B;
  --brand-blue: #2088c2; /* Azul del aro del logo */
  --brand-green: #156c36; /* Verde del fondo del logo */
  --danger-red: #EF4444; 
  --text-main: #F8FAFC;
  --text-muted: #94A3B8;
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

.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

/* NAVBAR */
.navbar {
  position: fixed;
  top: 0; left: 0; right: 0;
  height: 90px;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  transition: all 0.3s ease;
  background: rgba(11, 17, 32, 0.4);
  backdrop-filter: blur(12px);
}

.navbar.scrolled {
  background: rgba(11, 17, 32, 0.95);
  border-bottom: 2px solid var(--brand-blue);
  box-shadow: 0 4px 20px rgba(0,0,0,0.4);
}

.nav-content {
  width: 100%;
  max-width: 1200px;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand {
  font-size: 1.5rem;
  font-weight: 800;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.brand-logo {
    height: 55px; 
    width: 55px;
    object-fit: contain;
}

.logo-text {
  color: var(--text-main);
  letter-spacing: 1px;
}

.links {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.links a {
  color: var(--text-main);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
  transition: color 0.2s;
}

.links a:hover, .links a.router-link-active {
  color: var(--brand-blue);
}

.btn-primary {
  background: var(--brand-green);
  color: white !important;
  padding: 0.6rem 1.5rem;
  border-radius: 8px;
  font-weight: 700 !important;
  transition: all 0.2s !important;
  border: none;
}

.btn-primary:hover {
  background: #1ca350;
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(21, 108, 54, 0.4);
}

.footer {
  text-align: center;
  padding: 2rem;
  background: #080C17;
  color: var(--text-muted);
  border-top: 2px solid var(--brand-blue);
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .d-none-mobile {
      display: none;
  }
}
</style>
