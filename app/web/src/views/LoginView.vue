<template>
  <div class="page-container py-5">
    <div class="container py-lg-5">
        <div class="row justify-content-center">
            <div class="col-12 col-md-6 col-lg-5">
                <div class="form-card shadow-lg">
                    <h2 class="display-6 fw-bold mb-4 text-center">Identificación</h2>
                    <div class="accent-bar mx-auto mb-4"></div>

                    <form @submit.prevent="handleLogin">
                        <div class="mb-4">
                            <label class="form-label text-muted">Email Institucional</label>
                            <input type="email" class="form-control custom-input" required v-model="email" placeholder="email@ejemplo.com">
                        </div>
                        <div class="mb-4">
                            <label class="form-label text-muted">Contraseña</label>
                            <input type="password" class="form-control custom-input" required v-model="password" placeholder="••••••••">
                        </div>

                        <div v-if="errorMsg" class="alert alert-danger custom-danger mb-4">{{ errorMsg }}</div>

                        <button type="submit" class="btn btn-primary-custom w-100 py-3 mb-3" :disabled="isLoading">
                            {{ isLoading ? 'Accediendo...' : 'Iniciar Sesión' }}
                        </button>
                        
                        <div class="text-center">
                            <p class="mb-0">¿No tienes cuenta? <router-link to="/registro" class="text-brand">Regístrate aquí</router-link></p>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const API_URL = `${window.location.protocol}//${window.location.hostname}:8000`;
const email = ref('');
const password = ref('');
const errorMsg = ref('');
const isLoading = ref(false);

const handleLogin = async () => {
    isLoading.value = true;
    errorMsg.value = '';
    
    try {
        const formData = new FormData();
        formData.append('username', email.value);
        formData.append('password', password.value);
        
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Error al iniciar sesión');
        }
        
        // Guardar sesión
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('agrupacion', data.agrupacion);
        localStorage.setItem('user_email', email.value);
        
        router.push('/');
        window.location.reload(); // Recargar para actualizar App.vue
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
    padding: 0.8rem 1rem;
}
.custom-danger {
    background: rgba(239, 68, 68, 0.2);
    color: #F87171;
    border: 1px solid rgba(239, 68, 68, 0.4);
}
</style>
