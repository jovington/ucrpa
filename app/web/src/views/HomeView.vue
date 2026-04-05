<template>
  <div>
    <!-- Hero Section -->
    <header id="inicio" class="hero-section">
      <div class="hero-overlay"></div>
      <div class="container position-relative z-2 h-100 d-flex align-items-center justify-content-center text-center">
        <div class="hero-content">
          <h1 class="hero-title mb-4">Unidad Canina de Rescate<br>del Principado de Asturias</h1>
          <p class="hero-subtitle mb-5">Salvar vidas es nuestra misión. Lealtad, valor y trabajo en equipo.</p>
          <a href="#mision" class="btn btn-outline-light px-4 py-2 fs-5 fw-bold">Conocer Más</a>
        </div>
      </div>
    </header>

    <!-- Sección Institucional -->
    <section id="mision" class="mission-section py-5">
        <div class="container py-lg-5">
            <div class="row align-items-center gy-5">
                <div class="col-12 col-lg-6">
                    <h2 class="display-5 fw-bold mb-3">Especialistas en Búsqueda K9</h2>
                    <div class="accent-bar mb-4"></div>
                    <p class="fs-5 text-muted mb-4">
                    La asociación <strong>UCRPA</strong> se dedica incansablemente a la formación, certificación y operatividad de equipos cinológicos (binomios compuestos por guía y perro) para la localización de personas desaparecidas en grandes áreas, zonas de montaña y estructuras colapsadas.
                    </p>
                    <p class="fs-5 text-muted">
                    Nuestros ejemplares caninos, fundamentados en un entrenamiento exhaustivo, el respeto mutuo y un agudo sentido del olfato, se convierten en la herramienta más valiosa y precisa en el terreno cuando cada minuto es crítica.
                    </p>
                </div>
                <div class="col-12 col-lg-6 position-relative">
                    <img src="/team.png" alt="Equipo de Rescate K9 en acción" class="img-fluid rounded-4 shadow-lg w-100 position-relative z-2" />
                    <div class="image-accent"></div>
                </div>
            </div>
        </div>
    </section>

    <!-- Sección Noticias / Convocatoria -->
    <section class="news-section py-5 bg-soft">
        <div class="container text-center py-5">
            <div class="news-card mx-auto p-4 p-md-5">
              <div class="display-3 mb-3">📅</div>
              <h3 class="fw-bold mb-3">Convocatoria Oficial</h3>
              <p class="fs-5 text-muted mb-4">Certificación Grado A, B y C para equipos K9 en grandes áreas y escombros. Del 19 al 21 de Junio de 2026. ¡Asegura tu plaza!</p>
              <router-link to="/inscripcion" class="btn btn-primary-custom btn-lg w-100 w-md-auto d-inline-block">
                Inscripción Certificación 2026 Asturias
              </router-link>
            </div>
        </div>
    </section>
  </div>
</template>

<style scoped>
/* HERO SECTION */
.hero-section {
  height: 100vh;
  position: relative;
  background-image: url('/hero.png');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
}
.hero-overlay {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: linear-gradient(to bottom, rgba(11,17,32,0.4) 0%, var(--bg-color) 100%);
}
.hero-title {
  font-size: clamp(2rem, 5vw, 4rem);
  font-weight: 800;
  text-shadow: 0 4px 20px rgba(0,0,0,0.5);
  line-height: 1.2;
}
.btn-outline-light {
    border-width: 2px;
}
.btn-outline-light:hover {
    color: var(--bg-color);
}

/* INSTITUCIONAL / MISION */
.accent-bar {
  width: 80px;
  height: 5px;
  background: var(--brand-green);
  border-radius: 3px;
}
.image-accent {
  position: absolute;
  top: -15px;
  right: -5px;
  width: 100%;
  height: 100%;
  border: 4px solid var(--brand-blue);
  border-radius: 1rem;
  z-index: 1;
}
@media (min-width: 992px) {
    .image-accent { right: -20px; top: -20px; }
}

/* CARDS DE NOTICIAS */
.news-section {
    background-color: var(--bg-color);
}
.news-card {
    background: rgba(32, 136, 194, 0.1);
    border: 1px solid rgba(32, 136, 194, 0.3);
    border-radius: 20px;
    max-width: 800px;
}

/* UTILITARIA CUSTOM */
.bg-soft {
    background-color: var(--bg-soft);
}
@media (max-width: 768px) {
    .w-md-auto { width: 100% !important; }
}
@media (min-width: 769px) {
    .w-md-auto { width: auto !important; }
}
</style>
