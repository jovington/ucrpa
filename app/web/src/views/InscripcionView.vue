<template>
  <div class="page-container">
    <div class="container" style="max-width: 800px;">
        <div class="form-card">
            <h2 class="title">Inscripción Certificación K9</h2>
            <p class="subtitle">Grado A, B y C (19 al 21 de Junio de 2026)</p>
            <div class="accent-bar"></div>

            <form @submit.prevent="submitForm">
                <div class="form-group">
                    <label>Nombre del Guía</label>
                    <input type="text" required placeholder="Ej: Juan Pérez" v-model="form.name">
                </div>
                <div class="form-group">
                    <label>Nombre del Perro</label>
                    <input type="text" required placeholder="Ej: Rex" v-model="form.dog">
                </div>
                <div class="form-group">
                    <label>Grado a certificar</label>
                    <select required v-model="form.grade">
                        <option value="" disabled>Seleccione grado...</option>
                        <option value="A">Grado A. Basico.</option>
                        <option value="B">Grado B. Nivel Medio.</option>
                        <option value="C">Grado C. Nivel Avanzado.</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Adjuntar Cartilla Sanitaria (Opcional, en PDF)</label>
                    <input type="file" accept="application/pdf" @change="onFileChange">
                </div>

                <div v-if="successMsg" class="success-toast">{{ successMsg }}</div>
                <div v-if="errorMsg" class="error-toast">{{ errorMsg }}</div>

                <button type="submit" class="btn-submit" :disabled="isSubmitting">
                    {{ isSubmitting ? 'Enviando...' : 'Enviar Inscripción' }}
                </button>
            </form>
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const API_URL = 'http://localhost:8000'; 
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

    try {
        // Por el momento, si suben archivo, lo integramos con nuestro upload de PDF existente
        if (form.value.file) {
            const formData = new FormData();
            formData.append('file', form.value.file);

            const fileRes = await fetch(`${API_URL}/upload`, {
                method: 'POST',
                body: formData,
            });

            if (!fileRes.ok) throw new Error('Fallo al adjuntar el archivo.');
        }

        // Simulación: aquí en el futuro enviaríamos los datos textuales a otra ruta de DB
        console.log("Inscripción recibida: ", form.value);
        successMsg.value = '¡Inscripción enviada correctamente! Nos pondremos en contacto contigo.';
        
        // Reset
        form.value.name = '';
        form.value.dog = '';
        form.value.grade = '';
        form.value.file = null;
        
    } catch (e) {
        errorMsg.value = e.message || 'Error en el servidor al enviar la inscripción.';
    } finally {
        isSubmitting.value = false;
    }
};
</script>

<style scoped>
.page-container {
    padding-top: 120px;
    min-height: calc(100vh - 100px);
}
.form-card {
    background: rgba(30, 41, 59, 0.7);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 3rem;
}
.title {
    margin: 0;
    font-size: 2rem;
    color: var(--text-main);
}
.subtitle {
    color: var(--brand-green);
    font-weight: 600;
    margin-top: 0.5rem;
    margin-bottom: 1.5rem;
}
.accent-bar {
    width: 60px;
    height: 4px;
    background: var(--brand-blue);
    margin-bottom: 2rem;
    border-radius: 2px;
}

.form-group {
    margin-bottom: 1.5rem;
}
.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    color: var(--text-muted);
    font-size: 0.95rem;
}
.form-group input[type="text"], .form-group select {
    width: 100%;
    padding: 1rem;
    background: rgba(11, 17, 32, 0.5);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: white;
    border-radius: 8px;
    font-size: 1rem;
}
.form-group input[type="file"] {
    width: 100%;
    padding: 1rem;
    background: rgba(11, 17, 32, 0.5);
    border: 1px dashed var(--brand-blue);
    color: white;
    border-radius: 8px;
}

.btn-submit {
    width: 100%;
    padding: 1rem;
    background: var(--brand-green);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1.1rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s;
    margin-top: 1rem;
}
.btn-submit:hover {
    background: #1ca350;
    transform: translateY(-2px);
}
.btn-submit:disabled {
    background: #475569;
    cursor: not-allowed;
    transform: none;
}

.success-toast {
    background: rgba(21, 108, 54, 0.2);
    color: #4ADE80;
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid rgba(21, 108, 54, 0.4);
    margin-bottom: 1rem;
}
.error-toast {
    background: rgba(239, 68, 68, 0.2);
    color: #F87171;
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid rgba(239, 68, 68, 0.4);
    margin-bottom: 1rem;
}
</style>
