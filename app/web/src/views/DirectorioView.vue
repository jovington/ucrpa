<template>
  <div class="page-container">
    <section class="directory-section">
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import DocumentList from '../components/DocumentList.vue';

const API_URL = 'http://localhost:8000'; 

const documents = ref([]);
const isDragging = ref(false);
const isUploading = ref(false);
const errorMessage = ref(null);
const fileInput = ref(null);

const fetchDocuments = async () => {
  const token = localStorage.getItem('token');
  try {
    const response = await fetch(`${API_URL}/documents`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    if (!response.ok) {
        if (response.status === 401) {
             errorMessage.value = "Sesión expirada. Por favor, entre de nuevo.";
             localStorage.removeItem('token');
        }
        throw new Error('Error de red o sesión');
    }
    documents.value = await response.json();
  } catch (error) {
    console.error("Error fetching docs", error);
    errorMessage.value = "Conexión interrumpida con el Directorio Operativo central.";
  }
};

onMounted(() => {
  fetchDocuments();
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
  const token = localStorage.getItem('token');
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch(`${API_URL}/upload`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
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

<style scoped>
.page-container {
    padding-top: 100px; /* Para que baje del navbar */
    min-height: calc(100vh - 100px);
}
.directory-section {
  padding: 2rem 0 6rem 0;
}
.directory-header {
  text-align: center;
  margin-bottom: 3rem;
}
.section-subtitle {
  color: var(--text-muted);
  font-size: 1.1rem;
}
.dropzone {
  margin: 0 auto 3rem auto;
  max-width: 700px;
  background: rgba(11, 17, 32, 0.4);
  backdrop-filter: blur(8px);
  border: 2px dashed var(--brand-blue);
  border-radius: 16px;
  padding: 3rem 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
}
.dropzone:hover, .dropzone.is-dragging {
  background: rgba(32, 136, 194, 0.15);
  border-color: var(--brand-green);
}
.upload-icon {
  color: var(--brand-green);
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
  color: var(--brand-blue) !important;
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
</style>
