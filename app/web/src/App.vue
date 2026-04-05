<template>
  <div class="app-wrapper">
    <!-- Navbar Institucional -->
    <nav class="navbar" :class="{ 'scrolled': isScrolled }">
      <div class="nav-content">
        <div class="brand">
          <span class="logo-icon">🐾</span>
          <span class="logo-text">UCRPA</span>
        </div>
        <div class="links">
          <a href="#inicio">Inicio</a>
          <a href="#mision">Nuestra Misión</a>
          <a href="#directorio" class="btn-primary">Directorio Operativo</a>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <header id="inicio" class="hero-section">
      <div class="hero-overlay"></div>
      <div class="hero-content">
        <h1 class="hero-title">Unidad Canina de Rescate<br>del Principado de Asturias</h1>
        <p class="hero-subtitle">Salvar vidas es nuestra misión. Lealtad, valor y trabajo en equipo.</p>
        <a href="#mision" class="btn-secondary">Conocer Más</a>
      </div>
    </header>

    <!-- Sección Institucional -->
    <section id="mision" class="mission-section">
        <div class="mission-container">
            <div class="mission-text">
                <h2 class="section-title">Especialistas en Búsqueda K9</h2>
                <div class="accent-bar"></div>
                <p>
                La asociación <strong>UCRPA</strong> se dedica incansablemente a la formación, certificación y operatividad de equipos cinológicos (binomios compuestos por guía y perro) para la localización de personas desaparecidas en grandes áreas, zonas de montaña y estructuras colapsadas.
                </p>
                <p>
                Nuestros ejemplares caninos, fundamentados en un entrenamiento exhaustivo, el respeto mutuo y un agudo sentido del olfato, se convierten en la herramienta más valiosa y precisa en el terreno cuando cada minuto es crítica.
                </p>
            </div>
            <div class="mission-image">
                <img src="/team.png" alt="Equipo de Rescate K9 en acción" />
                <div class="image-accent"></div>
            </div>
        </div>
    </section>

    <!-- Directorio Operativo (Gestor de PDFs) -->
    <section id="directorio" class="directory-section">
      <div class="container">
        <div class="directory-header">
            <h2 class="section-title">Directorio Operativo</h2>
            <p class="section-subtitle">Intranet para la gestión interna de protocolos, cartografía táctica y manuales.</p>
        </div>
        
        <!-- Zona de Carga -->
        <div 
          class="dropzone" 
          :class="{ 'is-dragging': isDragging }"
          @dragover.prevent="isDragging = true"
          @dragleave.prevent="isDragging = false"
          @drop.prevent="handleDrop"
          @click="$refs.fileInput.click()"
        >
          <input 
            type="file" 
            ref="fileInput" 
            @change="handleFileSelect" 
            accept="application/pdf" 
            style="display: none" 
          />
          <div class="drop-content">
            <div class="upload-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
            </div>
            <h3 v-if="!isUploading">Añadir Documento Oficial</h3>
            <h3 v-else class="uploading-text">Cargando al servidor seguro...</h3>
            <p>Arraste aquí su PDF táctico o haga clic</p>
          </div>
        </div>

        <div v-if="errorMessage" class="error-toast">{{ errorMessage }}</div>

        <!-- Componente Listado -->
        <DocumentList :documents="documents" />
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <p>&copy; 2026 UCRPA - Patinando huellas, salvando vidas.</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import DocumentList from './components/DocumentList.vue';

// En producción esto debiese usar el dominio oficial o ser vacio (si está routeado con Nginx en el mismo dom)
const API_URL = 'http://localhost:8000'; 

// UI State
const documents = ref([]);
const isDragging = ref(false);
const isUploading = ref(false);
const errorMessage = ref(null);
const fileInput = ref(null);
const isScrolled = ref(false);

const handleScroll = () => {
    isScrolled.value = window.scrollY > 50;
};

const fetchDocuments = async () => {
  try {
    const response = await fetch(`${API_URL}/documents`);
    if (!response.ok) throw new Error('Network error');
    documents.value = await response.json();
  } catch (error) {
    console.error("Error fetching docs", error);
    errorMessage.value = "Conexión interrumpida con el Directorio Operativo central.";
  }
};

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
  fetchDocuments();
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});

const processFile = async (file) => {
  if (!file) return;
  if (file.type !== 'application/pdf' && !file.name.toLowerCase().endsWith('.pdf')) {
    showError("Acceso denegado: formato de archivo no permitido. Solo PDFs.");
    return;
  }
  await uploadFile(file);
};

const handleDrop = (e) => {
  isDragging.value = false;
  const files = e.dataTransfer.files;
  if (files.length > 0) processFile(files[0]);
};

const handleFileSelect = (e) => {
  const files = e.target.files;
  if (files.length > 0) processFile(files[0]);
  e.target.value = '';
};

const uploadFile = async (file) => {
  isUploading.value = true;
  errorMessage.value = null;
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch(`${API_URL}/upload`, {
      method: 'POST',
      body: formData,
    });
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Fallo de subida cifrada');
    }
    await fetchDocuments(); 
  } catch (err) {
    showError(err.message);
  } finally {
    isUploading.value = false;
  }
};

const showError = (msg) => {
  errorMessage.value = msg;
  setTimeout(() => errorMessage.value = null, 5000);
};
</script>

<style>
/* PALETA DE COLORES INSTITUCIONAL */
:root {
  --bg-color: #0B1120;
  --bg-soft: #1E293B;
  --primary-navy: #1E3A8A; /* Azul UCRPA */
  --accent-yellow: #F59E0B; /* Amarillo Rescue */
  --accent-yellow-hover: #FBBF24;
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
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  transition: all 0.3s ease;
  background: transparent;
}

.navbar.scrolled {
  background: rgba(11, 17, 32, 0.9);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
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
  gap: 0.5rem;
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

.links a:hover {
  color: var(--accent-yellow);
}

.btn-primary {
  background: var(--accent-yellow);
  color: #111827 !important;
  padding: 0.6rem 1.5rem;
  border-radius: 8px;
  font-weight: 700 !important;
  transition: all 0.2s !important;
}

.btn-primary:hover {
  background: var(--accent-yellow-hover);
  transform: translateY(-2px);
}

/* HERO SECTION */
.hero-section {
  height: 100vh;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  background-image: url('/hero.png');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
}

.hero-overlay {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: linear-gradient(to bottom, rgba(11,17,32,0.4) 0%, rgba(11,17,32,0.9) 100%);
  z-index: 1;
}

.hero-content {
  position: relative;
  z-index: 2;
  text-align: center;
  max-width: 800px;
  padding: 2rem;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 1.5rem;
  text-shadow: 0 4px 20px rgba(0,0,0,0.5);
}

.hero-subtitle {
  font-size: 1.25rem;
  color: #CBD5E1;
  margin-bottom: 2.5rem;
  font-weight: 400;
}

.btn-secondary {
  background: transparent;
  color: var(--text-main);
  border: 2px solid var(--text-main);
  padding: 0.8rem 2rem;
  border-radius: 8px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: var(--text-main);
  color: var(--bg-color);
}

/* INSTITUCIONAL / MISION */
.mission-section {
  padding: 6rem 0;
  background: var(--bg-color);
}

.mission-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  max-width: 1200px;
  margin: 0 auto;
  align-items: center;
  padding: 0 2rem;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.accent-bar {
  width: 60px;
  height: 4px;
  background: var(--accent-yellow);
  margin-bottom: 2rem;
  border-radius: 2px;
}

.mission-text p {
  color: var(--text-muted);
  line-height: 1.8;
  font-size: 1.1rem;
  margin-bottom: 1.5rem;
}

.mission-image {
  position: relative;
}

.mission-image img {
  width: 100%;
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.5);
  z-index: 2;
  position: relative;
}

.image-accent {
  position: absolute;
  top: -20px;
  right: -20px;
  width: 100%;
  height: 100%;
  border: 4px solid var(--primary-navy);
  border-radius: 16px;
  z-index: 1;
}

/* DIRECTORIO OPERATIVO */
.directory-section {
  padding: 6rem 0;
  background: var(--bg-soft);
  border-top: 1px solid rgba(255,255,255,0.05);
}

.directory-header {
  text-align: center;
  margin-bottom: 3rem;
}

.section-subtitle {
  color: var(--text-muted);
  font-size: 1.1rem;
}

/* DROPZONE */
.dropzone {
  margin: 0 auto 3rem auto;
  max-width: 700px;
  background: rgba(11, 17, 32, 0.4);
  backdrop-filter: blur(8px);
  border: 2px dashed var(--primary-navy);
  border-radius: 16px;
  padding: 3rem 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
}

.dropzone:hover, .dropzone.is-dragging {
  background: rgba(30, 58, 138, 0.15);
  border-color: var(--accent-yellow);
}

.upload-icon {
  color: var(--accent-yellow);
  margin-bottom: 1rem;
}

.dropzone h3 {
  font-size: 1.3rem;
  margin: 0 0 0.5rem 0;
  color: var(--text-main);
}

.dropzone p {
  color: var(--text-muted);
  margin: 0;
  font-size: 0.9rem;
}

.uploading-text {
  color: var(--accent-yellow) !important;
}

.error-toast {
  max-width: 700px;
  margin: 0 auto 2rem auto;
  padding: 1rem;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #F87171;
  border-radius: 8px;
  text-align: center;
  font-weight: 500;
}

.footer {
  text-align: center;
  padding: 2rem;
  background: #080C17;
  color: var(--text-muted);
  border-top: 1px solid rgba(255,255,255,0.05);
  font-size: 0.9rem;
}

/* RESPONSIVE */
@media (max-width: 768px) {
  .mission-container {
    grid-template-columns: 1fr;
  }
  .hero-title {
    font-size: 2.2rem;
  }
}
</style>
