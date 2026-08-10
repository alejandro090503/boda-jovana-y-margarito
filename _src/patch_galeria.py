"""Sustituye la galeria de fotos por la rueda 3D de boda-veronica-y-andres
y la coloca justo debajo del codigo de vestimenta.

Ademas da a las figuras del dress code una levitacion sutil con resplandor.
"""
import io

p = "../index.html"
s = io.open(p, encoding="utf-8").read()

# ── 1. quitar la seccion de fotos actual (grid de tarjetas) ──
ini = s.index('<!-- ═══════════════ 12B. FOTOS FINALES ═══════════════ -->')
fin = s.index('<!-- ═══════════════ 13. FOOTER ═══════════════════════ -->')
s = s[:ini] + s[fin:]

# ── 2. insertar la rueda 3D despues del dress code ──
ancla = '<!-- ═══════════════ 10. FAMILIA · CONSTELACIÓN DE MEDALLONES ═══════════════ -->'
galeria = '''<!-- ═══════════════ 9B. GALERÍA · RUEDA 3D ═══════════ -->
<section id="galeria">
  <span class="lbl">Nuestros recuerdos</span>
  <h2 class="ttl">Momentos <em style="font-family:'Great Vibes',cursive;color:var(--gold);font-size:40px;font-style:normal">juntos</em></h2>
  <div class="gline"></div>

  <div class="wheel-scene" id="wheel-scene">
    <div class="wheel-ring" id="wheel-ring">
''' + "".join(
    '      <div class="wheel-card"><img src="assets/fotos/f%d.jpg" alt="Jovana y Margarito" loading="lazy"></div>\n' % i
    for i in range(1, 7)
) + '''    </div>
  </div>

  <p class="gal-hint">Arrastra para girar</p>
</section>


'''
assert ancla in s
s = s.replace(ancla, galeria + ancla, 1)

# ── 3. CSS de la rueda + levitacion de las figuras ──
css = """
/* -- GALERIA: rueda 3D (misma que boda-veronica-y-andres) -- */
#galeria{background:var(--ink2);overflow:hidden}
.wheel-scene{
  position:relative;width:100%;height:420px;margin:34px auto 0;
  perspective:1400px;transform-style:preserve-3d;overflow:visible;
}
.wheel-ring{position:absolute;width:100%;height:100%;transform-style:preserve-3d;cursor:grab}
.wheel-ring.dragging{cursor:grabbing}
.wheel-card{
  position:absolute;width:190px;height:266px;left:50%;top:50%;
  margin-left:-95px;margin-top:-133px;
  border-radius:18px;overflow:hidden;
  border:2px solid rgba(169,104,0,.32);
  box-shadow:0 12px 40px rgba(70,82,0,.24);
  user-select:none;-webkit-user-select:none;
}
.wheel-card img{width:100%;height:100%;object-fit:cover;object-position:center;display:block;pointer-events:none}
.gal-hint{
  font-family:'Cormorant Garamond',serif;font-style:italic;font-size:16px;
  text-align:center;color:var(--gold-dark);margin-top:18px;
}

/* -- DRESS CODE: las figuras levitan con su resplandor -- */
.dc-fig{position:relative}
.dc-fig::before{
  content:'';position:absolute;left:50%;top:34%;
  width:150px;height:150px;transform:translate(-50%,-50%);
  background:radial-gradient(circle,rgba(169,104,0,.20) 0%,rgba(169,104,0,.09) 42%,transparent 70%);
  filter:blur(6px);pointer-events:none;
  animation:dcGlow 5.5s ease-in-out infinite;
}
.dc-fig:nth-of-type(3)::before{animation-delay:-2.7s}
@keyframes dcGlow{
  0%,100%{opacity:.55;transform:translate(-50%,-50%) scale(.94)}
  50%    {opacity:1;  transform:translate(-50%,-50%) scale(1.08)}
}
.dc-svg{
  position:relative;z-index:1;
  animation:dcFloat 5.5s ease-in-out infinite;
  filter:drop-shadow(0 10px 12px rgba(70,82,0,.28));
}
.dc-fig:nth-of-type(3) .dc-svg{animation-delay:-2.7s}
@keyframes dcFloat{
  0%,100%{transform:translateY(0)}
  50%    {transform:translateY(-9px)}
}
/* sombra en el suelo: se encoge cuando la figura sube */
.dc-fig::after{
  content:'';position:absolute;left:50%;bottom:78px;
  width:96px;height:11px;transform:translateX(-50%);
  background:radial-gradient(ellipse,rgba(70,82,0,.30) 0%,transparent 72%);
  filter:blur(3px);pointer-events:none;
  animation:dcShadow 5.5s ease-in-out infinite;
}
.dc-fig:nth-of-type(3)::after{animation-delay:-2.7s}
@keyframes dcShadow{
  0%,100%{opacity:.75;transform:translateX(-50%) scaleX(1)}
  50%    {opacity:.4; transform:translateX(-50%) scaleX(.82)}
}
@media(prefers-reduced-motion:reduce){
  .dc-svg,.dc-fig::before,.dc-fig::after{animation:none}
}
"""
s = s.replace("  </style>", css + "  </style>")

# ── 4. JS de la rueda ──
js = """
/* -- GALERIA: rueda 3D con arrastre e inercia -- */
(function(){
  var ring = document.getElementById('wheel-ring');
  if(!ring) return;
  var cards = ring.querySelectorAll('.wheel-card');
  var n = cards.length;
  if(!n) return;

  var radius = 210;
  var rot = 0, vel = 0, isDrag = false, startX = 0, startRot = 0, lastX = 0, rafId = null;

  cards.forEach(function(card, i){
    card.style.transform = 'rotateY(' + (360 / n * i) + 'deg) translateZ(' + radius + 'px)';
  });

  function setRot(){ if(window.gsap) gsap.set(ring,{rotateY:rot}); else ring.style.transform='rotateY('+rot+'deg)'; }
  setRot();

  function inertia(){
    if(isDrag) return;
    rot += vel; vel *= 0.94; setRot();
    if(Math.abs(vel) > 0.05) rafId = requestAnimationFrame(inertia);
  }
  function pointerDown(x){
    isDrag = true; auto = false;
    ring.classList.add('dragging');
    startX = x; lastX = x; startRot = rot; vel = 0;
    if(rafId) cancelAnimationFrame(rafId);
  }
  function pointerMove(x){
    if(!isDrag) return;
    rot = startRot + (x - startX) * 0.45;
    vel = (x - lastX) * 0.5;
    lastX = x; setRot();
  }
  function pointerUp(){
    if(!isDrag) return;
    isDrag = false;
    ring.classList.remove('dragging');
    rafId = requestAnimationFrame(inertia);
  }

  ring.addEventListener('mousedown', function(e){ e.preventDefault(); pointerDown(e.clientX); });
  window.addEventListener('mousemove', function(e){ pointerMove(e.clientX); });
  window.addEventListener('mouseup', pointerUp);
  ring.addEventListener('touchstart', function(e){ pointerDown(e.touches[0].clientX); }, {passive:true});
  ring.addEventListener('touchmove',  function(e){ pointerMove(e.touches[0].clientX); }, {passive:true});
  ring.addEventListener('touchend', pointerUp);

  /* giro lento automatico hasta el primer arrastre */
  var auto = true;
  (function spin(){
    if(auto && !isDrag){ rot += 0.12; setRot(); }
    requestAnimationFrame(spin);
  })();
})();
"""
marca = "</script>\n</body>"
assert marca in s
s = s.replace(marca, js + marca)

io.open(p, "w", encoding="utf-8").write(s)
print("galeria 3D movida bajo vestimenta; figuras con levitacion")
