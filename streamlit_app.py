import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="¡Feliz Cumpleaños!", page_icon="🎆", layout="centered")

# Fondo oscuro global para que el lienzo se fusione con toda la ventana
st.markdown("""
    <style>
        .stApp { background-color: #07080f; }
        .block-container { padding-top: 1rem; padding-bottom: 0rem; max-width: 100%; }
        header, footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

experiencia_completa = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', system-ui, sans-serif; user-select: none; }

  body {
    width: 100vw;
    height: 580px;
    background: radial-gradient(circle at center, #111428 0%, #07080f 100%);
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    touch-action: none;
  }

  /* Lienzo 1: Fuegos artificiales y estela de partículas */
  #canvas-fondo {
    position: fixed;
    inset: 0;
    width: 100%;
    height: 100%;
    z-index: 1;
  }

  .escenario {
    position: relative;
    z-index: 2;
    perspective: 1100px;
    pointer-events: none; /* Permite que los toques fuera de la tarjeta lleguen al fondo */
  }

  /* Tarjeta holográfica 3D */
  .tarjeta {
    position: relative;
    width: 310px;
    height: 440px;
    border-radius: 26px;
    background: rgba(18, 20, 38, 0.88);
    backdrop-filter: blur(14px);
    border: 2px solid rgba(0, 242, 254, 0.5);
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7), 0 0 25px rgba(0, 242, 254, 0.2);
    padding: 22px 18px;
    text-align: center;
    color: white;
    overflow: hidden;
    transform-style: preserve-3d;
    pointer-events: auto;
    transition: transform 0.4s ease, box-shadow 0.4s ease;
  }

  /* Reflejo iridiscente dinámico */
  .brillo-holo {
    position: absolute;
    inset: 0;
    pointer-events: none;
    background: radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.2), transparent 60%);
    opacity: 0;
    transition: opacity 0.3s;
    z-index: 4;
  }

  .titulo {
    font-size: 25px;
    font-weight: 800;
    background: linear-gradient(90deg, #ff4b8b, #00f2fe, #a855f7);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: fluirTexto 3s linear infinite;
    margin-bottom: 8px;
    transform: translateZ(25px);
  }

  .mensaje {
    font-size: 14px;
    color: #e2e8f0;
    line-height: 1.5;
    min-height: 68px;
    margin-bottom: 12px;
    transform: translateZ(15px);
  }

  .cursor {
    display: inline-block;
    width: 2px;
    height: 15px;
    background: #00f2fe;
    margin-left: 3px;
    vertical-align: middle;
    animation: parpadeo 0.75s infinite;
  }

  .pista-interaccion {
    font-size: 12px;
    color: #94a3b8;
    background: rgba(255, 255, 255, 0.06);
    padding: 6px 12px;
    border-radius: 14px;
    display: inline-block;
    transform: translateZ(20px);
  }

  /* Lienzo 2: Capa metálica raspable */
  #canvas-raspadito {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    z-index: 5;
    cursor: grab;
    transition: opacity 0.7s ease, transform 0.7s ease;
  }

  #canvas-raspadito.revelado {
    opacity: 0;
    transform: scale(1.08);
    pointer-events: none;
  }

  @keyframes fluirTexto {
    to { background-position: 200% center; }
  }
  @keyframes parpadeo {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
  }
</style>
</head>
<body>

<canvas id="canvas-fondo"></canvas>

<div class="escenario">
  <div class="tarjeta" id="tarjeta">
    <div class="brillo-holo" id="brillo"></div>

    <lottie-player 
        src="https://lottie.host/4b9a8ad7-204f-4f37-82e9-763145543601/x5kQU0nePB.json" 
        background="transparent" 
        speed="1" 
        style="width: 195px; height: 195px; margin: 0 auto;" 
        loop 
        autoplay>
    </lottie-player>

    <div class="titulo">¡Feliz Cumpleaños!</div>
    <p class="mensaje"><span id="texto-tipeado"></span><span class="cursor"></span></p>
    <div class="pista-interaccion">🎆 Toca el fondo para lanzar pirotecnia</div>

    <canvas id="canvas-raspadito" width="310" height="440"></canvas>
  </div>
</div>

<script>
  // =========================================================
  // 1. MOTOR DE FÍSICAS: PARTÍCULAS Y FUEGOS ARTIFICIALES
  // =========================================================
  const canvasBg = document.getElementById('canvas-fondo');
  const ctxBg = canvasBg.getContext('2d');
  let particulas = [];

  function ajustarCanvasBg() {
    canvasBg.width = window.innerWidth;
    canvasBg.height = window.innerHeight;
  }
  window.addEventListener('resize', ajustarCanvasBg);
  ajustarCanvasBg();

  class Particula {
    constructor(x, y, color, velocidadX, velocidadY, radio, decaimiento) {
      this.x = x;
      this.y = y;
      this.color = color;
      this.vx = velocidadX;
      this.vy = velocidadY;
      this.radio = radio;
      this.alfa = 1;
      this.decaimiento = decaimiento;
    }
    actualizar() {
      this.vx *= 0.96; // Fricción del aire
      this.vy *= 0.96;
      this.vy += 0.08; // Gravedad
      this.x += this.vx;
      this.y += this.vy;
      this.alfa -= this.decaimiento;
    }
    dibujar() {
      ctxBg.save();
      ctxBg.globalAlpha = Math.max(0, this.alfa);
      ctxBg.beginPath();
      ctxBg.arc(this.x, this.y, this.radio, 0, Math.PI * 2);
      ctxBg.fillStyle = this.color;
      ctxBg.shadowBlur = 10;
      ctxBg.shadowColor = this.color;
      ctxBg.fill();
      ctxBg.restore();
    }
  }

  function detonarFuegoArtificial(x, y) {
    const colores = ['#ff4b8b', '#00f2fe', '#facc15', '#a855f7', '#4ade80'];
    const colorBase = colores[Math.floor(Math.random() * colores.length)];
    for (let i = 0; i < 48; i++) {
      const angulo = (Math.PI * 2 / 48) * i;
      const fuerza = Math.random() * 5 + 2;
      particulas.push(new Particula(
        x, y,
        Math.random() > 0.3 ? colorBase : '#ffffff',
        Math.cos(angulo) * fuerza,
        Math.sin(angulo) * fuerza,
        Math.random() * 2.5 + 1.5,
        Math.random() * 0.015 + 0.012
      ));
    }
  }

  function animarFondo() {
    // Estela suave en lugar de borrar por completo
    ctxBg.fillStyle = 'rgba(7, 8, 15, 0.22)';
    ctxBg.fillRect(0, 0, canvasBg.width, canvasBg.height);

    for (let i = particulas.length - 1; i >= 0; i--) {
      particulas[i].actualizar();
      particulas[i].dibujar();
      if (particulas[i].alfa <= 0) particulas.splice(i, 1);
    }
    requestAnimationFrame(animarFondo);
  }
  animarFondo();

  // Estela al mover dedo/mouse por cualquier parte
  window.addEventListener('pointermove', (e) => {
    for (let i = 0; i < 2; i++) {
      particulas.push(new Particula(
        e.clientX, e.clientY, '#00f2fe',
        (Math.random() - 0.5) * 1.5,
        (Math.random() - 0.5) * 1.5,
        2, 0.03
      ));
    }
  });

  // Detonar pirotecnia al tocar el fondo
  canvasBg.addEventListener('pointerdown', (e) => {
    detonarFuegoArtificial(e.clientX, e.clientY);
  });

  // =========================================================
  // 2. MECÁNICA DE RASPADITO (CANVAS PIXEL ERASER)
  // =========================================================
  const canvasRasp = document.getElementById('canvas-raspadito');
  const ctxRasp = canvasRasp.getContext('2d');
  let raspando = false;
  let desbloqueado = false;
  let contadorChequeo = 0;

  function prepararCapaRaspable() {
    const grad = ctxRasp.createLinearGradient(0, 0, 310, 440);
    grad.addColorStop(0, '#1e1b4b');
    grad.addColorStop(0.5, '#312e81');
    grad.addColorStop(1, '#1e1e2f');
    ctxRasp.fillStyle = grad;
    ctxRasp.fillRect(0, 0, 310, 440);

    // Patrón decorativo de puntos
    ctxRasp.fillStyle = 'rgba(255, 255, 255, 0.06)';
    for (let x = 15; x < 310; x += 22) {
      for (let y = 15; y < 440; y += 22) {
        ctxRasp.beginPath();
        ctxRasp.arc(x, y, 2, 0, Math.PI * 2);
        ctxRasp.fill();
      }
    }

    // Texto indicador sobre la cubierta
    ctxRasp.fillStyle = '#ffffff';
    ctxRasp.font = 'bold 20px sans-serif';
    ctxRasp.textAlign = 'center';
    ctxRasp.fillText('🪙 RASPA AQUÍ 🪙', 155, 205);
    ctxRasp.font = '14px sans-serif';
    ctxRasp.fillStyle = '#a5b4fc';
    ctxRasp.fillText('Desliza tu dedo para descubrir', 155, 235);
  }
  prepararCapaRaspable();

  function raspar(clientX, clientY) {
    if (desbloqueado) return;
    const rect = canvasRasp.getBoundingClientRect();
    const x = clientX - rect.left;
    const y = clientY - rect.top;

    // 'destination-out' convierte los trazos en transparencia pura
    ctxRasp.globalCompositeOperation = 'destination-out';
    ctxRasp.beginPath();
    ctxRasp.arc(x, y, 28, 0, Math.PI * 2);
    ctxRasp.fill();

    // Verifica el porcentaje raspado cada 8 movimientos para no saturar el CPU
    contadorChequeo++;
    if (contadorChequeo % 8 === 0) {
      const pixeles = ctxRasp.getImageData(0, 0, 310, 440).data;
      let transparentes = 0;
      const totalMuestra = pixeles.length / 64; // Muestreo rápido 1 de cada 16 píxeles
      for (let i = 3; i < pixeles.length; i += 64) {
        if (pixeles[i] === 0) transparentes++;
      }
      if ((transparentes / totalMuestra) > 0.45) {
        completarRevelacion();
      }
    }
  }

  canvasRasp.addEventListener('pointerdown', (e) => { raspando = true; raspar(e.clientX, e.clientY); });
  window.addEventListener('pointerup', () => { raspando = false; });
  canvasRasp.addEventListener('pointermove', (e) => { if (raspando) raspar(e.clientX, e.clientY); });

  // =========================================================
  // 3. REVELACIÓN, MÁQUINA DE ESCRIBIR Y EFECTO 3D
  // =========================================================
  const tarjeta = document.getElementById('tarjeta');
  const brillo = document.getElementById('brillo');
  const textoObjetivo = "Que este nuevo año venga lleno de grandes momentos, proyectos increíbles y mucha salud. ¡Disfruta tu día al máximo!";
  let indiceLetra = 0;

  function escribirMensaje() {
    if (indiceLetra < textoObjetivo.length) {
      document.getElementById('texto-tipeado').textContent += textoObjetivo.charAt(indiceLetra);
      indiceLetra++;
      setTimeout(escribirMensaje, 35);
    }
  }

  function completarRevelacion() {
    if (desbloqueado) return;
    desbloqueado = true;
    canvasRasp.classList.add('revelado');
    escribirMensaje();

    // Ráfaga automática de 5 fuegos artificiales alrededor de la tarjeta
    for (let i = 0; i < 5; i++) {
      setTimeout(() => {
        const rx = Math.random() * (canvasBg.width * 0.8) + canvasBg.width * 0.1;
        const ry = Math.random() * (canvasBg.height * 0.5) + 60;
        detonarFuegoArtificial(rx, ry);
      }, i * 320);
    }
  }

  // Inclinación 3D activa únicamente después de raspar
  tarjeta.addEventListener('pointermove', (e) => {
    if (!desbloqueado) return;
    const rect = tarjeta.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const rotX = ((y - rect.height / 2) / (rect.height / 2)) * -15;
    const rotY = ((x - rect.width / 2) / (rect.width / 2)) * 15;

    tarjeta.style.transition = 'transform 0.08s ease-out';
    tarjeta.style.transform = `rotateX(${rotX}deg) rotateY(${rotY}deg)`;
    brillo.style.opacity = '1';
    brillo.style.background = `radial-gradient(circle at ${x}px ${y}px, rgba(255, 255, 255, 0.25), transparent 60%)`;
  });

  tarjeta.addEventListener('pointerleave', () => {
    if (!desbloqueado) return;
    tarjeta.style.transition = 'transform 0.5s ease';
    tarjeta.style.transform = 'rotateX(0deg) rotateY(0deg)';
    brillo.style.opacity = '0';
  });
</script>

</body>
</html>
"""

components.html(experiencia_completa, height=580)