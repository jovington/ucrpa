<template>
  <div class="page-container py-5">
    <div class="container py-lg-5">
        <div class="row justify-content-center">
            <div class="col-12 col-lg-8">
                <div class="form-card shadow-lg">
                    <h2 class="display-6 fw-bold mb-2">Inscripción Certificación K9</h2>
                    <p class="fs-5 text-success-custom fw-semibold mb-4">Grado A, B y C (19 al 21 de Junio de 2026)</p>
                    <div class="accent-bar mb-4"></div>

                    <form @submit.prevent="submitForm">
                        <div class="mb-4">
                            <label class="form-label text-muted">Nombre del Guía</label>
                            <input type="text" class="form-control custom-input" required placeholder="Ej: Juan Pérez" v-model="form.name">
                        </div>
                        <div class="mb-4">
                            <label class="form-label text-muted">Nombre del Perro</label>
                            <input type="text" class="form-control custom-input" required placeholder="Ej: Rex" v-model="form.dog">
                        </div>
                        <div class="mb-4">
                            <label class="form-label text-muted">Grado a certificar</label>
                            <select class="form-select custom-input" required v-model="form.grade">
                                <option value="" disabled>Seleccione grado...</option>
                                <option value="A">Grado A. Básico.</option>
                                <option value="B">Grado B. Nivel Medio.</option>
                                <option value="C">Grado C. Nivel Avanzado.</option>
                            </select>
                        </div>
                        <div class="mb-4">
                            <label class="form-label text-muted">Adjuntar Cartilla Sanitaria (Opcional, en PDF)</label>
                            <input type="file" class="form-control custom-file" accept="application/pdf" @change="onFileChange">
                        </div>

                        <div v-if="successMsg" class="alert alert-success custom-success">{{ successMsg }}</div>
                        <div v-if="errorMsg" class="alert alert-danger custom-danger">{{ errorMsg }}</div>

                        <button type="submit" class="btn btn-primary-custom w-100 py-3 mt-2" :disabled="isSubmitting">
                            {{ isSubmitting ? 'Enviando Datos Seguros...' : 'Enviar Inscripción' }}
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// En un entorno profesional esto se configuraría vía variables de entorno.
// Usamos el host actual para que funcione tanto en local como en red local (192.168.1.26).
const API_URL = `${window.location.protocol}//${window.location.hostname}:8000`; 
const isSubmitting = ref(false);
const successMsg = ref('');
const errorMsg = ref('');

const form = ref({
    name: '',
    dog: '',
    grade: '',
    file: null
});

const onFileChange = (e) => {
    const files = e.target.files;
    if(files.length > 0) {
        form.value.file = files[0];
    }
};

const submitForm = async () => {
    isSubmitting.value = true;
    errorMsg.value = '';
    successMsg.value = '';
    const token = localStorage.getItem('token');

    try {
        if (form.value.file) {
            const formData = new FormData();
            formData.append('file', form.value.file);

            const fileRes = await fetch(`${API_URL}/upload`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                body: formData,
            });

            if (!fileRes.ok) throw new Error('Fallo al adjuntar el archivo PDF.');
        }

        console.log("Inscripción enviada exitosamente: ", form.value);
        successMsg.value = '¡Inscripción recibida correctamente! Nos pondremos en contacto contigo a la brevedad.';
        
        form.value.name = '';
        form.value.dog = '';
        form.value.grade = '';
        form.value.file = null;
        
    } catch (e) {
        errorMsg.value = e.message || 'Error de conexión con el servidor.';
    } finally {
        isSubmitting.value = false;
    }
};
</script>

<style scoped>
.page-container {
    padding-top: 100px; /* Offset for navbar */
    min-height: 100vh;
}
.form-card {
    background: rgba(30, 41, 59, 0.7);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 2rem;
}
@media (min-width: 768px) {
    .form-card {
        padding: 4rem;
    }
}
.text-success-custom {
    color: var(--brand-green);
}
.accent-bar {
    width: 60px;
    height: 5px;
    background: var(--brand-blue);
    border-radius: 3px;
}

/* CUSTOM INPUTS PARA SOBREESCRIBIR BOOTSTRAP DEFAULT BLANCO */
.custom-input {
    background-color: rgba(11, 17, 32, 0.6) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    color: white !important;
    padding: 0.8rem 1rem;
    border-radius: 8px;
}
.custom-input::placeholder {
    color: rgba(255, 255, 255, 0.7) !important;
}
.custom-input:focus {
    box-shadow: 0 0 0 0.25rem rgba(32, 136, 194, 0.25) !important;
    border-color: var(--brand-blue) !important;
}

.custom-file {
    background-color: rgba(11, 17, 32, 0.6) !important;
    border: 1px dashed var(--brand-blue) !important;
    color: white !important;
    padding: 0.8rem;
    border-radius: 8px;
}
.custom-file::file-selector-button {
    background-color: var(--bg-soft);
    color: white;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 4px;
    padding: 0.4rem 1rem;
    margin-right: 1rem;
    cursor: pointer;
}

.custom-success {
    background: rgba(21, 108, 54, 0.2);
    color: #4ADE80;
    border: 1px solid rgba(21, 108, 54, 0.4);
}
.custom-danger {
    background: rgba(239, 68, 68, 0.2);
    color: #F87171;
    border: 1px solid rgba(239, 68, 68, 0.4);
}
</style>
