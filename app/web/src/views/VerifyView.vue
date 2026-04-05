<template>
  <div class="page-container py-5">
    <div class="container py-lg-5">
        <div class="row justify-content-center">
            <div class="col-12 col-md-6 col-lg-5">
                <div class="form-card shadow-lg text-center">
                    <h2 class="display-6 fw-bold mb-4">Validación de Cuenta</h2>
                    <div class="accent-bar mx-auto mb-4"></div>
                    
                    <p class="text-muted mb-4">Introduzca el código de 6 dígitos que se le ha asignado.</p>

                    <form @submit.prevent="handleVerify">
                        <div class="mb-4">
                            <input 
                                type="text" 
                                class="form-control custom-input text-center fs-2 fw-bold tracking-widest" 
                                required 
                                v-model="code" 
                                maxlength="6" 
                                placeholder="000000"
                            >
                        </div>

                        <div v-if="errorMsg" class="alert alert-danger custom-danger mb-4">{{ errorMsg }}</div>
                        <div v-if="successMsg" class="alert alert-success custom-success mb-4">{{ successMsg }}</div>

                        <button type="submit" class="btn btn-primary-custom w-100 py-3 mb-3" :disabled="isLoading">
                            {{ isLoading ? 'Validando...' : 'Verificar Cuenta' }}
                        </button>
                        
                        <div class="text-center mt-3">
                            <p class="mb-0">¿Algún error? <router-link to="/registro" class="text-brand">Volver al registro</router-link></p>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();
const API_URL = `${window.location.protocol}//${window.location.hostname}:8000`;
const email = ref(route.query.email || '');
const code = ref('');
const errorMsg = ref('');
const successMsg = ref('');
const isLoading = ref(false);

onMounted(() => {
    if (!email.value) {
        errorMsg.value = "Falta el email de referencia. Por favor, regístrese de nuevo.";
    }
});

const handleVerify = async () => {
    isLoading.value = true;
    errorMsg.value = '';
    
    try {
        const response = await fetch(`${API_URL}/auth/verify`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: email.value,
                code: code.value
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Código incorrecto');
        }
        
        successMsg.value = "¡Cuenta activada con éxito! Redirigiendo al login...";
        setTimeout(() => {
            router.push('/login');
        }, 2000);
    } catch (e) {
        errorMsg.value = e.message;
    } finally {
        isLoading.value = false;
    }
};
</script>

<style scoped>
.page-container {
    padding-top: 100px;
    min-height: 100vh;
}
.form-card {
    background: rgba(30, 41, 59, 0.7);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 2.5rem;
}
.accent-bar {
    width: 50px;
    height: 4px;
    background: var(--brand-blue);
    border-radius: 2px;
}
.text-brand {
    color: var(--brand-blue);
    text-decoration: none;
    font-weight: 600;
}
.custom-input {
    background-color: rgba(11, 17, 32, 0.6) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: white !important;
    letter-spacing: 0.5rem;
    padding: 1rem;
}
.custom-danger {
    background: rgba(239, 68, 68, 0.2);
    color: #F87171;
    border: 1px solid rgba(239, 68, 68, 0.4);
}
.custom-success {
    background: rgba(21, 108, 54, 0.2);
    color: #4ADE80;
    border: 1px solid rgba(21, 108, 54, 0.4);
}
</style>
