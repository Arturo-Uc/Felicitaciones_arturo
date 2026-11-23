import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Simulación 3D en Código", page_icon="🌹", layout="centered")

st.markdown("""
    <style>
        .stApp { background-color: #05050a; }
        .block-container { padding-top: 1rem; padding-bottom: 0rem; max-width: 100%; }
        header, footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

simulacion_rosa = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }

  body {
    width: 100vw;
    height: 600px;
    background: radial-gradient(circle at 50% 45%, #120918 0%, #05050a 100%);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    font-family: 'Courier New', monospace;
    touch-action: none;
  }

  canvas {
    width: 100%;
    height: 100%;
    cursor: grab;
  }

  canvas:active {
    cursor: grabbing;
  }

  /* Controles flotantes minimalistas */
  .controles {
    position: fixed;
    bottom: 18px;
    display: flex;
    gap: 10px;
    z-index: 10;
  }

  .btn {
    background: rgba(255, 255, 255, 0.07);
    border: 1px solid rgba(255, 75, 139, 0.45);
    color: #f8fafc;
    padding: 8px 14px;
    border-radius: 20px;
    font-family: 'Segoe UI', sans-serif;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    backdrop-filter: blur(8px);
    transition: all 0.2s;
  }

  .btn:hover {
    background: rgba(255, 75, 139, 0.25);
    border-color: #ff4b8b;
  }

  .btn:active {
    transform: scale(0.94);
  }
</style>
</head>
<body>

<canvas id="lienzo"></canvas>

<div class="controles">
  <button class="btn" onclick="reiniciarCrecimiento()">🌱 Volver a florecer</button>
  <button class="btn" id="btn-texto" onclick="alternarModoTexto()">💻 Modo: Palabras</button>
</div>

<script>
  const canvas = document.getElementById('lienzo');
  const ctx = canvas.getContext('2d');

  // Textos que formarán la estructura de la rosa
  const FRASE_PALABRAS = "PARA TI • ERES ESPECIAL • ";
  const FRASE_CODIGO = "if(smile){return true;} 01 ";
  let modoCodigo = false;

  let ancho, alto;
  function redimensionar() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    ancho = window.innerWidth;
    alto = window.innerHeight;
    canvas.width = ancho * dpr;
    canvas.height = alto * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  window.addEventListener('resize', redimensionar);
  redimensionar();

  // =========================================================
  // 1. GENERACIÓN DE PUNTOS 3D (TALLO, HOJAS Y PÉTALOS)
  // =========================================================
  let puntosBase = [];

  function construirGeometriaRosa() {
    puntosBase = [];
    const cadena = modoCodigo ? FRASE_CODIGO : FRASE_PALABRAS;
    let idxChar = 0;

    const siguienteCaracter = () => {
      const c = cadena[idxChar % cadena.length];
      idxChar++;
      return c === " " ? "•" : c;
    };

    // A) Tallo (crece primero: umbral 0.0 -> 0.32)
    const totalTallo = 75;
    for (let i = 0; i < totalTallo; i++) {
      const t = i / totalTallo;
      const y = 175 - t * 195; // De abajo (+175) hacia la base de la flor (-20)
      const x = Math.sin(t * Math.PI) * 10;
      const z = Math.cos(t * Math.PI) * 6;
      puntosBase.push({
        x, y, z,
        tipo: 'tallo',
        char: modoCodigo ? (i % 2 === 0 ? "1" : "0") : "|",
        umbral: t * 0.32,
        u: 0
      });
    }

    // B) Dos hojas laterales (umbral 0.16 -> 0.36)
    const crearHoja = (lado, alturaY, umbralInicio) => {
      const filas = 8;
      const cols = 6;
      for (let i = 1; i <= filas; i++) {
        const u = i / filas;
        const anchoHoja = Math.sin(u * Math.PI) * 24;
        for (let j = -cols / 2; j <= cols / 2; j++) {
          const v = j / (cols / 2);
          const x = lado * (u * 58 + 6);
          const y = alturaY - u * 22 + Math.abs(v) * 4;
          const z = v * anchoHoja;
          puntosBase.push({
            x, y, z,
            tipo: 'hoja',
            char: siguienteCaracter(),
            umbral: umbralInicio + u * 0.16,
            u: 0
          });
        }
      }
    };
    crearHoja(1, 75, 0.15);
    crearHoja(-1, 115, 0.12);

    // C) Pétalos de la rosa (Ecuación paramétrica espiral: umbral 0.30 -> 1.0)
    const totalPetalos = 500;
    const vueltas = 13;
    for (let i = 0; i < totalPetalos; i++) {
      const u = i / totalPetalos; // 0 = centro del capullo, 1 = pétalos exteriores
      const theta = u * vueltas * Math.PI * 2;

      // Modulación matemática que forma los bordes curvos de cada pétalo
      const mod = ((3.6 * theta) % (Math.PI * 2)) / Math.PI;
      const a = (5 / 4) * Math.pow(1 - mod, 2) - 0.25;
      const formaPetalo = 1 - 0.5 * Math.pow(a, 2);

      const radio = (6 + u * 98) * formaPetalo;
      const x = radio * Math.cos(theta);
      const z = radio * Math.sin(theta);
      // Perfil de copa: el centro sube y los pétalos externos se abren hacia abajo
      const y = -62 + Math.pow(u, 1.55) * 48 - Math.sin(u * Math.PI) * 18 * formaPetalo;

      puntosBase.push({
        x, y, z,
        tipo: 'petalo',
        char: siguienteCaracter(),
        umbral: 0.30 + u * 0.65,
        u: u
      });
    }
  }

  construirGeometriaRosa();

  // =========================================================
  // 2. VARIABLES DE ANIMACIÓN E INTERACCIÓN TÁCTIL
  // =========================================================
  let progresoCrecimiento = 0;
  let anguloY = 0;
  let inclinacionX = 0.28; // Ligera vista superior para apreciar la espiral
  let arrastrando = false;
  let ultimoX = 0;
  let ultimoY = 0;

  function reiniciarCrecimiento() {
    progresoCrecimiento = 0;
  }

  function alternarModoTexto() {
    modoCodigo = !modoCodigo;
    document.getElementById('btn-texto').textContent = modoCodigo ? "💻 Modo: Código" : "💻 Modo: Palabras";
    construirGeometriaRosa();
    reiniciarCrecimiento();
  }

  canvas.addEventListener('pointerdown', (e) => {
    arrastrando = true;
    ultimoX = e.clientX;
    ultimoY = e.clientY;
  });

  window.addEventListener('pointerup', () => { arrastrando = false; });

  window.addEventListener('pointermove', (e) => {
    if (!arrastrando) return;
    const dx = e.clientX - ultimoX;
    const dy = e.clientY - ultimoY;
    anguloY += dx * 0.012;
    inclinacionX = Math.max(-0.5, Math.min(0.85, inclinacionX + dy * 0.008));
    ultimoX = e.clientX;
    ultimoY = e.clientY;
  });

  // =========================================================
  // 3. BUCLE DE RENDERIZADO 3D (60 FPS)
  // =========================================================
  function renderizar() {
    ctx.clearRect(0, 0, ancho, alto);

    // Avanza el crecimiento orgánico hasta llegar a 1.0
    if (progresoCrecimiento < 1) {
      progresoCrecimiento = Math.min(1, progresoCrecimiento + 0.0065);
    }

    // Rotación automática suave cuando el usuario no la está girando
    if (!arrastrando) {
      anguloY += 0.014;
    }

    const cosY = Math.cos(anguloY);
    const sinY = Math.sin(anguloY);
    const cosX = Math.cos(inclinacionX);
    const sinX = Math.sin(inclinacionX);

    const fov = 360; // Distancia focal de la cámara virtual
    const centroX = ancho / 2;
    const centroY = alto / 2 - 15;

    let proyectados = [];

    for (let i = 0; i < puntosBase.length; i++) {
      const p = puntosBase[i];
      if (progresoCrecimiento < p.umbral) continue;

      // Factor de expansión suave al brotar cada punto (0 -> 1)
      const brote = Math.min(1, (progresoCrecimiento - p.umbral) * 14);
      const px = p.x * brote;
      const py = p.y;
      const pz = p.z * brote;

      // Rotación en eje Y (giro horizontal)
      const x1 = px * cosY - pz * sinY;
      const z1 = px * sinY + pz * cosY;

      // Rotación en eje X (inclinación vertical)
      const y2 = py * cosX - z1 * sinX;
      const z2 = py * sinX + z1 * cosX;

      // Proyección 3D a 2D
      const escala = fov / (fov + z2 + 180);
      const pantallaX = x1 * escala + centroX;
      const pantallaY = y2 * escala + centroY;

      proyectados.push({
        x: pantallaX,
        y: pantallaY,
        z: z2,
        escala: escala * brote,
        tipo: p.tipo,
        char: p.char,
        u: p.u
      });
    }

    // Ordenar de atrás hacia adelante (Painter's Algorithm) para dar volumen real
    proyectados.sort((a, b) => b.z - a.z);

    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    for (let i = 0; i < proyectados.length; i++) {
      const pt = proyectados[i];
      // Normaliza la profundidad para calcular luz y sombra
      const luz = Math.max(0.25, Math.min(1, (130 - pt.z) / 220));
      const tamanoFuente = Math.max(7, Math.round(13 * pt.escala));
      ctx.font = `bold ${tamanoFuente}px 'Courier New', monospace`;

      if (pt.tipo === 'petalo') {
        const r = Math.round(140 + 115 * luz);
        const g = Math.round(15 + 65 * luz * pt.u);
        const b = Math.round(55 + 85 * luz);
        ctx.fillStyle = `rgba(${r}, ${g}, ${b}, ${0.35 + 0.65 * luz})`;
      } else {
        const g = Math.round(110 + 135 * luz);
        ctx.fillStyle = `rgba(20, ${g}, 115, ${0.35 + 0.65 * luz})`;
      }

      ctx.fillText(pt.char, pt.x, pt.y);
    }

    requestAnimationFrame(renderizar);
  }

  renderizar();
</script>

</body>
</html>
"""

components.html(simulacion_rosa, height=600)