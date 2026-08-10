import io

p = "../index.html"
s = io.open(p, encoding="utf-8").read()

css = """
/* -- MESA DE REGALOS: caja que se abre con confeti -------
   Mismo componente que venimos usando en las invitaciones recientes.     */
.gbx{position:relative;text-align:center;margin-top:6px}
.gbx-present{width:150px;height:150px;margin:0 auto;display:block;padding:0;border:none;background:none;cursor:pointer;position:relative;-webkit-tap-highlight-color:transparent}
.gbx-present svg{width:100%;height:100%;display:block;transform-origin:50% 100%}
.gbx-lid{transform-origin:50% 100%;transition:transform .5s var(--spring)}
.gbx-present.shake{animation:gbxShake .5s ease-in-out}
@keyframes gbxShake{0%,100%{transform:rotate(0)}15%{transform:rotate(-5deg)}30%{transform:rotate(4deg)}45%{transform:rotate(-3deg)}60%{transform:rotate(2deg)}75%{transform:rotate(-1deg)}}
.gbx.opened .gbx-present{animation:gbxTopple .7s cubic-bezier(.6,-.2,.7,1) forwards;pointer-events:none}
@keyframes gbxTopple{0%{transform:scale(1);opacity:1}40%{transform:scale(1.06)}100%{transform:scale(.86) translateY(-12px);opacity:0}}
.gbx.opened .gbx-lid{transform:translateY(-30px) rotate(-18deg)}
.gbx-tap{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:16px;letter-spacing:1px;color:var(--gold-dark);opacity:.95;margin-top:10px;transition:opacity .3s,max-height .3s;overflow:hidden}
.gbx.opened .gbx-tap{opacity:0;max-height:0;margin:0}
.gbx-confetti{position:absolute;top:38%;left:50%;width:0;height:0;pointer-events:none;z-index:10}
.gbx-confetti-piece{position:absolute;opacity:0}
.gift-links{margin-top:18px}

/* -- LLUVIA DE SOBRES: sobre que se abre al tocarlo ----- */
.env-wrap{margin:34px auto 0;display:flex;flex-direction:column;align-items:center}
.env-interactive{display:flex;flex-direction:column;align-items:center;cursor:pointer;-webkit-tap-highlight-color:transparent;outline:none;border:none;background:none;padding:0}
.env-body{perspective:700px;position:relative;width:260px;height:200px;animation:envBreathe 3.6s ease-in-out infinite}
@keyframes envBreathe{0%,100%{transform:scale(1)}50%{transform:scale(1.03)}}
.env-body svg.env-svg{width:100%;height:100%}
.env-flap-wrap{position:absolute;top:46px;left:18px;width:224px;height:86px;transform-origin:top center;transform-style:preserve-3d;backface-visibility:hidden;-webkit-backface-visibility:hidden;transition:transform .65s cubic-bezier(.4,0,.2,1);pointer-events:none;z-index:2}
.env-interactive.open .env-flap-wrap{transform:rotateX(-175deg)}
.env-open-content{overflow:hidden;max-height:0;opacity:0;transition:max-height .55s .3s ease,opacity .4s .38s ease;display:flex;flex-direction:column;align-items:center;gap:8px;padding:0 20px;text-align:center;pointer-events:none}
.env-interactive.open .env-open-content{max-height:260px;opacity:1;pointer-events:auto}
.env-mailbox-icon{width:40px;height:40px;color:var(--gold);margin-top:10px}
.env-title{font-family:'Cormorant Garamond',serif;font-size:26px;color:var(--cream);letter-spacing:.5px;line-height:1.2}
.env-desc{font-family:'Cormorant Garamond',serif;font-size:16px;font-style:italic;color:var(--cream);opacity:.9;line-height:1.75}
.env-tap-hint{font-family:'Lato',sans-serif;font-size:12px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:var(--gold-dark);opacity:.9;margin-top:8px;transition:opacity .3s}
.env-interactive.open ~ .env-tap-hint{opacity:0;pointer-events:none}
@media(prefers-reduced-motion:reduce){.env-body{animation:none}}

/* -- DRESS CODE: figuras de dama y caballero ------------ */
.dc-figures{display:flex;align-items:stretch;justify-content:center;gap:0;margin-top:18px;max-width:420px;margin-left:auto;margin-right:auto}
.dc-fig{flex:1;display:flex;flex-direction:column;align-items:center;padding:14px 8px}
.dc-divider{width:1px;flex-shrink:0;margin:10px 0;background:linear-gradient(to bottom,transparent,var(--gold) 18%,var(--gold) 82%,transparent)}
.dc-svg{height:190px;width:auto;object-fit:contain;filter:drop-shadow(0 6px 14px rgba(70,82,0,.22))}
.dc-fig-name{font-family:'Cormorant Garamond',serif;font-size:16px;font-weight:600;color:var(--cream);letter-spacing:3px;margin-top:14px;text-transform:uppercase}
.dc-fig-hint{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:15px;color:var(--gold-dark);margin-top:6px;text-align:center;line-height:1.5}

/* -- PALETA: circulos mas pequenos con brillo que recorre */
.palette{gap:14px}
.pal-sw{
  width:44px;height:44px;border-radius:50%;position:relative;overflow:hidden;
  box-shadow:0 3px 10px rgba(70,82,0,.28), inset 0 -3px 7px rgba(0,0,0,.22), inset 0 2px 5px rgba(255,255,255,.3);
  border:1px solid rgba(255,255,255,.35);
}
.pal-sw::before{
  content:'';position:absolute;top:-60%;left:-120%;width:80%;height:260%;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.65),transparent);
  transform:rotate(22deg);
  animation:palShine 4.2s ease-in-out infinite;
}
.pal-item:nth-child(2) .pal-sw::before{animation-delay:.5s}
.pal-item:nth-child(3) .pal-sw::before{animation-delay:1s}
.pal-item:nth-child(4) .pal-sw::before{animation-delay:1.5s}
.pal-item:nth-child(5) .pal-sw::before{animation-delay:2s}
@keyframes palShine{
  0%,72%{left:-120%}
  100%{left:150%}
}
.pal-sw::after{
  content:'';position:absolute;top:14%;left:20%;width:34%;height:24%;
  border-radius:50%;background:rgba(255,255,255,.42);filter:blur(2px);
}
@media(prefers-reduced-motion:reduce){.pal-sw::before{animation:none;opacity:0}}
"""

assert "  </style>" in s
s = s.replace("  </style>", css + "  </style>")

js = """
/* -- MESA DE REGALOS: la caja se abre con confeti ------- */
(function(){
  var box   = document.getElementById('giftBox');
  var btn   = document.getElementById('giftBtn');
  var conf  = document.getElementById('giftConfetti');
  var links = document.getElementById('giftLinks');
  if(!box || !btn || !links) return;

  function abrir(){
    if(box.classList.contains('opened')) return;
    btn.classList.add('shake');
    btn.setAttribute('aria-expanded','true');

    setTimeout(function(){
      box.classList.add('opened');

      var colors = ['#465200','#6c7a43','#a96800','#c88700','#730e00','#D4C5B2','#FAF6E7'];
      var reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
      if(!reduced && window.gsap){
        for(var i=0;i<34;i++){
          var p = document.createElement('div');
          p.className = 'gbx-confetti-piece';
          p.style.background = colors[i % colors.length];
          var sz = 5 + Math.random()*7;
          p.style.width = sz+'px'; p.style.height = sz+'px';
          p.style.borderRadius = Math.random() > .5 ? '50%' : '2px';
          conf.appendChild(p);
          var ang = Math.random()*Math.PI*2;
          var d   = 55 + Math.random()*105;
          gsap.fromTo(p,
            {opacity:1,x:0,y:0,scale:1,rotation:0},
            {x:Math.cos(ang)*d, y:Math.sin(ang)*d - 46, opacity:0, scale:.2,
             rotation:Math.random()*720-360, duration:.9+Math.random()*.5,
             ease:'power2.out', delay:Math.random()*.12,
             onComplete:function(){ var t=this.targets()[0]; if(t && t.remove) t.remove(); }});
        }
      }

      links.hidden = false;
      if(window.gsap){
        gsap.fromTo(links.children,
          {opacity:0,y:22},
          {opacity:1,y:0,duration:.7,stagger:.12,ease:'power2.out',delay:.15});
      }
      if(window.ScrollTrigger) ScrollTrigger.refresh();
    }, 480);

    setTimeout(function(){ btn.style.display = 'none'; }, 1200);
  }

  btn.addEventListener('click', abrir);
})();

/* -- LLUVIA DE SOBRES: abre y cierra el sobre ----------- */
(function(){
  var btn = document.querySelector('.env-interactive');
  if(!btn) return;
  btn.addEventListener('click', function(){
    var isOpen = btn.classList.toggle('open');
    btn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    if(window.ScrollTrigger) ScrollTrigger.refresh();
  });
})();
"""

marca = "</script>\n</body>"
assert marca in s
s = s.replace(marca, js + marca)

io.open(p, "w", encoding="utf-8").write(s)
print("css y js insertados")
