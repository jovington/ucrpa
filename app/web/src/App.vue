<template>
  <div class="app-wrapper">
    <header class="header">
      <div class="header-content">
        <h1 class="logo-text">UCRPA Pdf Manager</h1>
        <p class="subtitle">Repositorio central de documentos</p>
      </div>
    </header>

    <main class="main-container">
      <!-- Zona de Carga Drag & Drop -->
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
          <div class="upload-icon">☁️</div>
          <h2 v-if="!isUploading">Arrastra tu PDF aquí o haz clic para subir</h2>
          <h2 v-else class="uploading-text">Subiendo archivo... 🚀</h2>
          <p class="restrictions">Sólo archivos con extensión .pdf</p>
        </div>
      </div>

      <!-- Error Notification -->
      <div v-if="errorMessage" class="error-toast">
        {{ errorMessage }}
      </div>

      <!-- Listado de Documentos -->
      <DocumentList :documents="documents" />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import DocumentList from './components/DocumentList.vue';

const API_URL = 'http://localhost:8000'; // Asegúrate de que el puerto coincida o usa una variable env

const documents = ref([]);
const isDragging = ref(false);
const isUploading = ref(false);
const errorMessage = ref(null);
const fileInput = ref(null);

// Cargar la lista de documentos al iniciar
const fetchDocuments = async () => {
  try {
    const response = await fetch(`${API_URL}/documents`);
    if (!response.ok) throw new Error('Error recuperando documentos');
    documents.value = await response.json();
  } catch (error) {
    console.error("Error fetching docs", error);
    errorMessage.value = "No se pudo conectar a la API del backend. Comprueba que el Docker está corriendo.";
  }
};

onMounted(() => {
  fetchDocuments();
});

// Manejo de archivos
const processFile = async (file) => {
  if (!file) return;
  if (file.type !== 'application/pdf' && !file.name.toLowerCase().endsWith('.pdf')) {
    showError("Por favor selecciona únicamente archivos PDF.");
    return;
  }
  
  await uploadFile(file);
};

const handleDrop = (e) => {
  isDragging.value = false;
  const files = e.dataTransfer.files;
  if (files.length > 0) {
    processFile(files[0]);
  }
};

const handleFileSelect = (e) => {
  const files = e.target.files;
  if (files.length > 0) {
    processFile(files[0]);
  }
  // Resetear el input para permitir subir el mismo archivo si es necesario
  e.target.value = '';
};

// Subida al servidor
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
      throw new Error(errorData.detail || 'Fallo desconocido al subir');
    }

    // El documento se subió exitosamente
    await fetchDocuments(); 

  } catch (err) {
    console.error(err);
    showError(`Error al subir el PDF: ${err.message}`);
  } finally {
    isUploading.value = false;
  }
};

const showError = (msg) => {
  errorMessage.value = msg;
  setTimeout(() => {
    errorMessage.value = null;
  }, 5000);
};
</script>

<style>
/* Estilos Base Globales para Glassmorphism y Paleta Oscura */
:root {
  --bg-color: #0F172A;
  --text-main: #F8FAFC;
  --text-muted: #94A3B8;
  --accent: #6366F1;
  --accent-hover: #818CF8;
}

body {
  margin: 0;
  padding: 0;
  background-color: var(--bg-color);
  background-image: 
    radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%), 
    radial-gradient(at 50% 0%, hsla(225,39%,30%,0.2) 0, transparent 50%), 
    radial-gradient(at 100% 0%, hsla(339,49%,30%,0.1) 0, transparent 50%);
  background-attachment: fixed;
  color: var(--text-main);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, 'Open Sans', 'Helvetica Neue', sans-serif;
  min-height: 100vh;
}

/* Componentes Principales */
.app-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.header {
  padding: 2rem;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  justify-content: center;
}

.header-content {
  width: 100%;
  max-width: 1200px;
}

.logo-text {
  margin: 0;
  font-size: 1.8rem;
  font-weight: 800;
  background: linear-gradient(135deg, #818CF8 0%, #C084FC 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.subtitle {
  margin: 0.25rem 0 0 0;
  color: var(--text-muted);
  font-size: 0.95rem;
}

.main-container {
  flex: 1;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 3rem 2rem;
  box-sizing: border-box;
}

/* Dropzone Premium */
.dropzone {
  background: rgba(30, 41, 59, 0.5);
  backdrop-filter: blur(10px);
  border: 2px dashed rgba(99, 102, 241, 0.3);
  border-radius: 24px;
  padding: 4rem 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.dropzone:hover, .dropzone.is-dragging {
  background: rgba(49, 46, 129, 0.2);
  border-color: var(--accent);
  transform: scale(1.02);
}

.upload-icon {
  font-size: 3.5rem;
  margin-bottom: 1rem;
  filter: drop-shadow(0px 4px 8px rgba(0,0,0,0.3));
}

.dropzone h2 {
  font-size: 1.4rem;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
}

.uploading-text {
  color: var(--accent-hover);
  animation: pulse 1.5s infinite;
}

.restrictions {
  color: var(--text-muted);
  font-size: 0.9rem;
  margin: 0;
}

.error-toast {
  margin-top: 1.5rem;
  padding: 1rem;
  background: rgba(220, 38, 38, 0.2);
  border: 1px solid rgba(220, 38, 38, 0.4);
  color: #FCA5A5;
  border-radius: 12px;
  text-align: center;
  font-weight: 500;
}

/* Animaciones */
@keyframes pulse {
  0% { opacity: 0.6; }
  50% { opacity: 1; }
  100% { opacity: 0.6; }
}

* {
  box-sizing: border-box;
}
</style>
