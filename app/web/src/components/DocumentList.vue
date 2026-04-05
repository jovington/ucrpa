<template>
  <div class="document-list">
    <h2 class="title">Tus Archivos</h2>
    <div v-if="documents.length === 0" class="empty-state">
      No hay documentos alojados en la plataforma aún.
    </div>
    <div v-else class="grid">
      <div class="card" v-for="doc in documents" :key="doc.id">
        <div class="card-icon">📄</div>
        <div class="card-info">
          <h3 class="filename" :title="doc.filename">{{ doc.filename }}</h3>
          <p class="meta">{{ formatDate(doc.upload_date) }} &bull; {{ formatSize(doc.size_bytes) }}</p>
        </div>
        <a :href="`http://localhost:8000/download/${doc.id}`" target="_blank" class="action-btn">
          Abrir
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  documents: {
    type: Array,
    required: true
  }
});

const formatSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('es-ES', { day: '2-digit', month: 'short', year: 'numeric' });
};
</script>

<style scoped>
.document-list {
  margin-top: 2rem;
  width: 100%;
}

.title {
  color: #E2E8F0;
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
}

.empty-state {
  padding: 3rem;
  text-align: center;
  background: rgba(30, 41, 59, 0.4);
  backdrop-filter: blur(12px);
  border: 1px dashed rgba(148, 163, 184, 0.2);
  border-radius: 16px;
  color: #94A3B8;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.card {
  display: flex;
  align-items: center;
  padding: 1.25rem;
  background: rgba(30, 41, 59, 0.7);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
  border-color: rgba(99, 102, 241, 0.5);
}

.card-icon {
  font-size: 2.5rem;
  margin-right: 1rem;
}

.card-info {
  flex: 1;
  min-width: 0;
}

.filename {
  font-size: 1.1rem;
  font-weight: 600;
  color: #F8FAFC;
  margin: 0 0 0.25rem 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.meta {
  font-size: 0.85rem;
  color: #94A3B8;
  margin: 0;
}

.action-btn {
  padding: 0.5rem 1rem;
  background: rgba(99, 102, 241, 0.1);
  color: #818CF8;
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.2s ease;
}

.action-btn:hover {
  background: #6366F1;
  color: #FFFFFF;
}
</style>
