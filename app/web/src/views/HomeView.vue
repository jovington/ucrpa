<template>
  <div>
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

    <!-- Sección Noticias / Convocatoria -->
    <section class="news-section">
        <div class="container text-center">
            <div class="news-card">
              <div class="news-icon">📅</div>
              <h3>Convocatoria Oficial</h3>
              <p>Certificación Grado A, B y C para equipos K9 en grandes áreas y escombros. Del 19 al 21 de Junio de 2026. ¡Asegura tu plaza!</p>
              <router-link to="/inscripcion" class="btn-primary" style="display:inline-block; margin-top:20px;">
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
  background: linear-gradient(to bottom, rgba(11,17,32,0.4) 0%, var(--bg-color) 100%);
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
  background: var(--brand-green);
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
  border: 4px solid var(--brand-blue);
  border-radius: 16px;
  z-index: 1;
}

/* CARDS DE NOTICIAS */
.news-section {
    padding: 2rem 0 6rem 0;
    background: var(--bg-color);
}
.news-card {
    background: rgba(32, 136, 194, 0.1);
    border: 1px solid rgba(32, 136, 194, 0.3);
    border-radius: 20px;
    padding: 3rem;
    max-width: 800px;
    margin: 0 auto;
}
.news-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}
.text-center { text-align: center; }
</style>
