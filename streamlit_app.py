import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="¡Feliz Cumpleaños!", page_icon="🎂", layout="centered")

st.markdown("""
    <style>
        .block-container { padding-top: 1.5rem; padding-bottom: 0rem; }
    </style>
""", unsafe_allow_html=True)

tarjeta_interactiva = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.2/dist/confetti.browser.min.js"></script>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', system-ui, sans-serif; }
  
  body {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 520px;
    background: transparent;
    overflow: hidden;
  }

  /* La perspectiva habilita el espacio 3D real para los elementos hijos */
  .escenario {
    position: relative;
    width: 320px;
    height: 460px;
    display: flex;
    justify-content: center;
    align-items: center;
    perspective: 1000px;
  }

  /* ESTADO 1: Caja flotante */
  .caja-regalo {
    position: absolute;
    width: 240px;
    height: 240px;
    background: linear-gradient(145deg, #1e1e2f, #2a2a45);
    border: 2px solid #ff4b8b;
    border-radius: 28px;
    box-shadow: 0 15px 35px rgba(255, 75, 139, 0.35);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    user-select: none;
    animation: levitar 2.8s ease-in-out infinite;
    transition: all 0.6s cubic-bezier(0.68, -0.55, 0.27, 1.55);
    z-index: 2;
  }

  .icono-regalo {
    font-size: 75px;
    margin-bottom: 12px;
    filter: drop-shadow(0 5px 15px rgba(0,0,0,0.4));
  }

  .texto-tocar {
    color: #ffffff;
    font-size: 15px;
    font-weight: 600;
    background: rgba(255, 75, 139, 0.2);
    padding: 6px 16px;
    border-radius: 20px;
    border: 1px solid rgba(255, 75, 139, 0.5);
  }

  .caja-regalo.abierta {
    transform: scale(1.4) translateY(-60px);
    opacity: 0;
    pointer-events: none;
  }

  /* ESTADO 2: Tarjeta 3D interactiva */
  .tarjeta-final {
    position: absolute;
    width: 100%;
    padding: 25px 20px;
    text-align: center;
    background: rgba(25, 25, 40, 0.94);
    backdrop-filter: blur(12px);
    border-radius: 28px;
    border: 2px solid #00f2fe;
    box-shadow: 0 15px 35px rgba(0, 242, 254, 0.25);
    color: white;
    opacity: 0;
    transform: scale(0.7);
    transform-style: preserve-3d;
    pointer-events: none;
    touch-action: none; /* Evita que el navegador haga scroll al deslizar el dedo */
    transition: opacity 0.7s ease, transform 0.7s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    z-index: 1;
    overflow: hidden;
  }

  .tarjeta-final.visible {
    opacity: 1;
    transform: scale(1);
    pointer-events: auto;
  }

  /* Capa de reflejo luminoso que sigue al dedo/cursor */
  .brillo-3d {
    position: absolute;
    inset: 0;
    pointer-events: none;
    background: radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.18), transparent 65%);
    opacity: 0;
    transition: opacity 0.3s ease;
  }

  .titulo-neon {
    font-size: 26px;
    font-weight: 800;
    background: linear-gradient(90deg, #ff4b8b, #00f2fe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
    transform: translateZ(25px); /* Eleva el texto en el eje Z */
  }

  /* Contenedor fijo para evitar saltos de altura mientras se escribe */
  .mensaje {
    font-size: 14px;
    color: #e2e8f0;
    line-height: 1.5;
    min-height: 66px;
    margin-bottom: 16px;
    transform: translateZ(15px);
  }

  /* Cursor parpadeante de la máquina de escribir */
  .cursor {
    display: inline-block;
    width: 2px;
    height: 15px;
    background-color: #00f2fe;
    margin-left: 3px;
    vertical-align: middle;
    animation: parpadear 0.75s infinite;
  }

  .btn-confeti {
    background: linear-gradient(90deg, #ff4b8b, #ff758c);
    border: none;
    color: white;
    padding: 10px 22px;
    border-radius: 20px;
    font-weight: bold;
    font-size: 14px;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(255, 75, 139, 0.4);
    transition: transform 0.15s;
    transform: translateZ(30px);
  }

  .btn-confeti:active {
    transform: translateZ(30px) scale(0.92);
  }

  @keyframes levitar {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-14px); }
  }

  @keyframes parpadear {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
  }
</style>
</head>
<body>

<div class="escenario">
  <div class="caja-regalo" id="caja" onclick="abrirRegalo()">
    <div class="icono-regalo">🎁</div>
    <div class="texto-tocar">Toca para abrir</div>
  </div>

  <div class="tarjeta-final" id="tarjeta">
    <div class="brillo-3d" id="brillo"></div>
    <lottie-player 
        src="https://lottie.host/4b9a8ad7-204f-4f37-82e9-763145543601/x5kQU0nePB.json" 
        background="transparent" 
        speed="1" 
        style="width: 190px; height: 190px; margin: 0 auto;" 
        loop 
        autoplay>
    </lottie-player>
    <div class="titulo-neon">¡Feliz Cumpleaños!</div>
    <p class="mensaje"><span id="texto-tipeado"></span><span class="cursor" id="cursor"></span></p>
    <button class="btn-confeti" onclick="dispararConfeti()">🎉 Más confeti</button>
  </div>
</div>

<script>
  const tarjeta = document.getElementById('tarjeta');
  const brillo = document.getElementById('brillo');
  const textoObjetivo = "Que este nuevo año venga cargado de excelentes momentos, salud y metas cumplidas. ¡Pásala increíble hoy!";
  let indiceLetra = 0;

  function dispararConfeti() {
    confetti({ particleCount: 55, angle: 60, spread: 55, origin: { x: 0, y: 0.7 } });
    confetti({ particleCount: 55, angle: 120, spread: 55, origin: { x: 1, y: 0.7 } });
  }

  // Lógica de máquina de escribir
  function escribirMensaje() {
    if (indiceLetra < textoObjetivo.length) {
      document.getElementById('texto-tipeado').textContent += textoObjetivo.charAt(indiceLetra);
      indiceLetra++;
      setTimeout(escribirMensaje, 38); // Velocidad en milisegundos por letra
    }
  }

  function abrirRegalo() {
    document.getElementById('caja').classList.add('abierta');
    tarjeta.classList.add('visible');
    dispararConfeti();
    setTimeout(escribirMensaje, 450); // Espera a que termine de aparecer la tarjeta
  }

  // Lógica de rotación 3D para mouse y pantalla táctil
  function aplicarInclinacion(clientX, clientY) {
    const rect = tarjeta.getBoundingClientRect();
    const x = clientX - rect.left; // Posición X dentro de la tarjeta
    const y = clientY - rect.top;  // Posición Y dentro de la tarjeta

    const centroX = rect.width / 2;
    const centroY = rect.height / 2;

    // Calcula el ángulo máximo de inclinación (±16 grados)
    const rotarX = ((y - centroY) / centroY) * -16;
    const rotarY = ((x - centroX) / centroX) * 16;

    tarjeta.style.transition = 'transform 0.08s ease-out';
    tarjeta.style.transform = `rotateX(${rotarX}deg) rotateY(${rotarY}deg) scale(1)`;

    // Mueve el reflejo de luz exactamente hacia donde está el dedo/cursor
    brillo.style.opacity = '1';
    brillo.style.background = `radial-gradient(circle at ${x}px ${y}px, rgba(255, 255, 255, 0.22), transparent 65%)`;
  }

  function resetearInclinacion() {
    tarjeta.style.transition = 'transform 0.5s ease';
    tarjeta.style.transform = 'rotateX(0deg) rotateY(0deg) scale(1)';
    brillo.style.opacity = '0';
  }

  // Eventos para PC (Mouse)
  tarjeta.addEventListener('mousemove', (e) => aplicarInclinacion(e.clientX, e.clientY));
  tarjeta.addEventListener('mouseleave', resetearInclinacion);

  // Eventos para Celular (Touch)
  tarjeta.addEventListener('touchmove', (e) => {
    const toque = e.touches[0];
    aplicarInclinacion(toque.clientX, toque.clientY);
  }, { passive: true });
  tarjeta.addEventListener('touchend', resetearInclinacion);
</script>

</body>
</html>
"""

components.html(tarjeta_interactiva, height=540)