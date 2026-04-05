<template>
  <div class="page-container py-5">
    <div class="container py-lg-4">
      <div class="row justify-content-center">
        <div class="col-12 col-lg-10">
          <div class="wizard-card shadow-lg" v-if="!submitted">
            <!-- Header del Wizard -->
            <div class="wizard-header mb-4 text-center">
              <h2 class="display-6 fw-bold mb-1">Inscripción Oficial K9</h2>
              <p class="text-brand-blue fw-semibold">Asistente de Registro Paso a Paso</p>
              
              <!-- Barra de Progreso -->
              <div class="progress-container mt-4">
                <div class="progress-bar-custom" :style="{ width: (currentStep / 5) * 100 + '%' }"></div>
                <div class="steps-labels d-flex justify-content-between mt-2">
                  <span :class="{ 'active': currentStep >= 1 }">General</span>
                  <span :class="{ 'active': currentStep >= 2 }">Guía</span>
                  <span :class="{ 'active': currentStep >= 3 }">Can</span>
                  <span :class="{ 'active': currentStep >= 4 }">Salud/Nivel</span>
                  <span :class="{ 'active': currentStep >= 5 }">Final</span>
                </div>
              </div>
            </div>

            <!-- Paso 1: General -->
            <div v-if="currentStep === 1" class="step-fade">
              <h4 class="mb-4"><i class="bi bi-geo-alt me-2"></i>Detalles de la Convocatoria</h4>
              <div class="row g-3">
                <div class="col-md-8">
                  <label class="form-label text-muted">Lugar de la Prueba</label>
                  <input type="text" class="form-control custom-input" v-model="form.lugar" placeholder="Ej: Polígono de Pruebas UCRPA">
                </div>
                <div class="col-md-4">
                  <label class="form-label text-muted">Fecha</label>
                  <input type="date" class="form-control custom-input" v-model="form.fecha">
                </div>
              </div>
            </div>

            <!-- Paso 2: El Guía -->
            <div v-if="currentStep === 2" class="step-fade">
              <h4 class="mb-4"><i class="bi bi-person me-2"></i>Datos del Conductor (Guía)</h4>
              <div class="row g-3">
                <div class="col-md-12">
                  <label class="form-label text-muted">Nombre y Apellidos</label>
                  <input type="text" class="form-control custom-input" v-model="form.guia_nombre" placeholder="Nombre completo">
                </div>
                <div class="col-md-6">
                  <label class="form-label text-muted">DNI / Pasaporte</label>
                  <input type="text" class="form-control custom-input" v-model="form.guia_dni" placeholder="Documento de identidad">
                </div>
                <div class="col-md-6">
                  <label class="form-label text-muted">Fecha Nacimiento</label>
                  <input type="date" class="form-control custom-input" v-model="form.guia_nacimiento">
                </div>
              </div>
            </div>

            <!-- Paso 3: El Perro -->
            <div v-if="currentStep === 3" class="step-fade">
              <h4 class="mb-4">🐾 Datos del Perro</h4>
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label text-muted">Nombre del Can</label>
                  <input type="text" class="form-control custom-input" v-model="form.perro_nombre">
                </div>
                <div class="col-md-6">
                  <label class="form-label text-muted">Raza</label>
                  <input type="text" class="form-control custom-input" v-model="form.perro_raza">
                </div>
                <div class="col-md-4">
                  <label class="form-label text-muted">Sexo</label>
                  <select class="form-select custom-input" v-model="form.perro_sexo">
                    <option value="Macho">Macho</option>
                    <option value="Hembra">Hembra</option>
                  </select>
                </div>
                <div class="col-md-4">
                  <label class="form-label text-muted">Nº Chip</label>
                  <input type="text" class="form-control custom-input" v-model="form.perro_chip">
                </div>
                <div class="col-md-4">
                  <label class="form-label text-muted">Fecha Nacimiento Can</label>
                  <input type="date" class="form-control custom-input" v-model="form.perro_nacimiento">
                </div>
              </div>
            </div>

            <!-- Paso 4: Salud y Niveles -->
            <div v-if="currentStep === 4" class="step-fade">
              <h4 class="mb-4">🛡️ Salud, Seguro y Niveles Operativos</h4>
              <div class="row g-4">
                <div class="col-md-12">
                   <p class="mb-2 fw-bold small text-brand-blue uppercase">Cotejo de Vacunación / Sanidad</p>
                   <div class="d-flex flex-wrap gap-4">
                      <div class="form-check custom-check">
                        <input class="form-check-input" type="checkbox" v-model="form.vacuna_antirrabica" id="checkRabia">
                        <label class="form-check-label" for="checkRabia">Antirrábica</label>
                      </div>
                      <div class="form-check custom-check">
                        <input class="form-check-input" type="checkbox" v-model="form.vacuna_otras" id="checkOtras">
                        <label class="form-check-label" for="checkOtras">Otras Vacunas</label>
                      </div>
                      <div class="form-check custom-check">
                        <input class="form-check-input" type="checkbox" v-model="form.desparasitacion" id="checkDesp">
                        <label class="form-check-label" for="checkDesp">Desparasitación</label>
                      </div>
                   </div>
                </div>
                <div class="col-md-12">
                  <label class="form-label text-muted">Seguro Responsabilidad Civil (Nº Póliza / Compañía)</label>
                  <input type="text" class="form-control custom-input" v-model="form.seguro_rc">
                </div>
                <!-- Fechas Certificados -->
                <div class="col-md-6">
                  <label class="form-label text-muted">Cert. 1º Auxilios (Humano)</label>
                  <input type="date" class="form-control custom-input" v-model="form.cert_primero_aux_humano">
                </div>
                <div class="col-md-6">
                  <label class="form-label text-muted">Cert. 1º Auxilios (Vet)</label>
                  <input type="date" class="form-control custom-input" v-model="form.cert_primero_aux_vet">
                </div>
                <!-- Niveles -->
                <div class="col-md-4">
                  <label class="form-label text-muted">Nivel Obediencia</label>
                  <input type="text" class="form-control custom-input" v-model="form.nivel_obediencia" placeholder="Grado/Nivel">
                </div>
                <div class="col-md-4">
                  <label class="form-label text-muted">Grandes Áreas</label>
                  <input type="text" class="form-control custom-input" v-model="form.nivel_grandes_areas" placeholder="Grado/Nivel">
                </div>
                <div class="col-md-4">
                  <label class="form-label text-muted">Escombros</label>
                  <input type="text" class="form-control custom-input" v-model="form.nivel_escombros" placeholder="Grado/Nivel">
                </div>
              </div>
            </div>

            <!-- Paso 5: Acompañantes y Finalizar -->
            <div v-if="currentStep === 5" class="step-fade">
              <h4 class="mb-4">👥 Acompañantes y Autorización</h4>
              
              <div class="acompanantes-section mb-4">
                <p class="small text-muted mb-3">Añada los acompañantes que asistirán a la prueba (Opcional):</p>
                <div v-for="(ac, index) in form.acompanantes" :key="index" class="row g-2 mb-2 align-items-end">
                    <div class="col-7">
                        <label class="form-label x-small" v-if="index === 0">Nombre Completo</label>
                        <input type="text" class="form-control custom-input form-control-sm" v-model="ac.nombre">
                    </div>
                    <div class="col-4">
                        <label class="form-label x-small" v-if="index === 0">DNI</label>
                        <input type="text" class="form-control custom-input form-control-sm" v-model="ac.dni">
                    </div>
                    <div class="col-1">
                        <button @click="removeAcompanante(index)" class="btn btn-link text-danger p-0 mb-1"><i class="bi bi-trash"></i></button>
                    </div>
                </div>
                <button @click="addAcompanante" class="btn btn-outline-brand btn-sm mt-2">+ Añadir Acompañante</button>
              </div>

              <div class="authorization-box p-3 rounded bg-dark border-brand mb-4">
                  <div class="form-check custom-check">
                    <input class="form-check-input" type="checkbox" v-model="form.autorizacion_fotos" id="checkFotos">
                    <label class="form-check-label small" for="checkFotos">
                      Doy mi conformidad para publicar fotografías de las pruebas en redes sociales tanto de UCRPA como de ANGPS.
                    </label>
                  </div>
              </div>

              <div v-if="errorMsg" class="alert alert-danger custom-danger">{{ errorMsg }}</div>
            </div>

            <!-- Navegación -->
            <div class="wizard-footer d-flex justify-content-between mt-5 pt-3 border-top border-secondary">
              <button @click="prevStep" class="btn btn-outline-light px-4" :disabled="currentStep === 1 || isSubmitting">Anterior</button>
              
              <button v-if="currentStep < 5" @click="nextStep" class="btn btn-primary-custom px-5">Siguiente</button>
              <button v-else @click="submitForm" class="btn btn-success-custom px-5" :disabled="isSubmitting">
                {{ isSubmitting ? 'Guardando Registro...' : 'Finalizar Inscripción' }}
              </button>
            </div>
          </div>

          <!-- Pantalla de Éxito -->
          <div class="wizard-card shadow-lg text-center py-5 step-fade" v-else>
            <div class="success-icon mb-4">✅</div>
            <h2 class="display-6 fw-bold mb-3">Equipo Registrado</h2>
            <p class="fs-5 text-muted mb-5">La inscripción se ha guardado correctamente en la base de datos institucional de UCRPA.</p>
            
            <div class="d-grid gap-3 col-md-6 mx-auto">
              <button @click="resetWizard" class="btn btn-primary-custom py-3 fw-bold">
                <i class="bi bi-plus-circle me-2"></i>Inscribir otro equipo / perro
              </button>
              <router-link to="/directorio" class="btn btn-outline-light py-3">
                Ir al Directorio de Archivos
              </router-link>
              <button @click="logout" class="btn btn-link text-danger mt-2">Salir de la Sesión</button>
            </div>
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
const API_URL = window.location.hostname.includes('ucrpa.local') 
                ? `${window.location.protocol}//api.ucrpa.local:8001`
                : `${window.location.protocol}//${window.location.hostname}:8001`; 

const currentStep = ref(1);
const isSubmitting = ref(false);
const submitted = ref(false);
const errorMsg = ref('');

const form = ref({
    lugar: '',
    fecha: '',
    guia_nombre: '',
    guia_dni: '',
    guia_nacimiento: '',
    perro_nombre: '',
    perro_raza: '',
    perro_sexo: 'Macho',
    perro_chip: '',
    perro_nacimiento: '',
    vacuna_antirrabica: false,
    vacuna_otras: false,
    desparasitacion: false,
    seguro_rc: '',
    cert_primero_aux_humano: '',
    cert_primero_aux_vet: '',
    nivel_obediencia: '',
    nivel_grandes_areas: '',
    nivel_escombros: '',
    acompanantes: [{ nombre: '', dni: '' }],
    autorizacion_fotos: false
});

const addAcompanante = () => form.value.acompanantes.push({ nombre: '', dni: '' });
const removeAcompanante = (index) => form.value.acompanantes.splice(index, 1);

const nextStep = () => {
    if (currentStep.value < 5) currentStep.value++;
};

const prevStep = () => {
    if (currentStep.value > 1) currentStep.value--;
};

const submitForm = async () => {
    isSubmitting.value = true;
    errorMsg.value = '';
    const token = localStorage.getItem('token');

    try {
        const response = await fetch(`${API_URL}/inscripciones/k9`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(form.value),
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || 'Fallo al guardar la inscripción.');
        }

        submitted.value = true;
    } catch (e) {
        errorMsg.value = e.message || 'Error de conexión con el servidor.';
    } finally {
        isSubmitting.value = false;
    }
};

const resetWizard = () => {
    form.value = {
        lugar: '',
        fecha: '',
        guia_nombre: '',
        guia_dni: '',
        guia_nacimiento: '',
        perro_nombre: '',
        perro_raza: '',
        perro_sexo: 'Macho',
        perro_chip: '',
        perro_nacimiento: '',
        vacuna_antirrabica: false,
        vacuna_otras: false,
        desparasitacion: false,
        seguro_rc: '',
        cert_primero_aux_humano: '',
        cert_primero_aux_vet: '',
        nivel_obediencia: '',
        nivel_grandes_areas: '',
        nivel_escombros: '',
        acompanantes: [{ nombre: '', dni: '' }],
        autorizacion_fotos: false
    };
    currentStep.value = 1;
    submitted.value = false;
};

const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('agrupacion');
    window.location.href = '/';
};
</script>

<style scoped>
.page-container {
    padding-top: 80px;
    min-height: 100vh;
    background: linear-gradient(135deg, #0B1120 0%, #080C17 100%);
}

.wizard-card {
    background: rgba(30, 41, 59, 0.7);
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 24px;
    padding: 2.5rem;
}

@media (max-width: 768px) {
    .wizard-card { padding: 1.5rem; }
}

.text-brand-blue { color: #2088c2; }

/* BARRA DE PROGRESO */
.progress-container {
    height: 8px;
    background: rgba(255,255,255,0.05);
    border-radius: 4px;
    overflow: hidden;
    position: relative;
}
.progress-bar-custom {
    height: 100%;
    background: linear-gradient(90deg, #156c36, #2088c2);
    transition: width 0.4s ease;
}
.steps-labels span {
    font-size: 0.75rem;
    color: rgba(255,255,255,0.3);
    font-weight: 600;
    text-transform: uppercase;
}
.steps-labels span.active {
    color: white;
}

/* INPUTS */
.custom-input {
    background: rgba(11, 17, 32, 0.5) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: white !important;
    padding: 0.75rem 1rem;
    border-radius: 10px;
}
.custom-input:focus {
    border-color: #2088c2 !important;
    box-shadow: 0 0 0 0.25rem rgba(32, 136, 194, 0.15) !important;
}

.custom-check .form-check-input {
    background-color: transparent;
    border: 2px solid rgba(255,255,255,0.3);
}
.custom-check .form-check-input:checked {
    background-color: #156c36;
    border-color: #156c36;
}

.border-brand { border: 1px solid rgba(32, 136, 194, 0.3) !important; }

/* ANIMACIONES */
.step-fade {
    animation: fadeIn 0.4s ease;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.success-icon {
    font-size: 5rem;
    color: #4ADE80;
}

.x-small { font-size: 0.7rem; color: #2088c2; font-weight: bold; }
.custom-danger {
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(239, 68, 68, 0.4);
    color: #f87171;
}

.btn-success-custom {
    background: #156c36;
    color: white;
    border: none;
    font-weight: 700;
    border-radius: 8px;
}
</style>
