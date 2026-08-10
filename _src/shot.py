"""Capturas de la invitacion a 375px, saltando el sobre y forzando el estado
final de las animaciones de entrada (GSAP no llega a correr en headless)."""
import sys
from playwright.sync_api import sync_playwright

URL = "http://localhost:8141/index.html"

ABRIR = """() => {
  document.getElementById('envelope-screen').style.display='none';
  const f=document.getElementById('env-flash'); if(f)f.style.display='none';
  document.querySelector('.main-wrap').classList.add('visible');
  if (typeof launchPage==='function') launchPage();
  document.querySelectorAll('.lbl,.ttl,.gline,.dc-sub,.dc-figures,.palette,.pal-item,.dc-note,.wheel-scene,.gal-hint,.gf-sub,.gbx,.env-wrap,.cd-ring-item,.loc-card,.cal-month,.cal-sub,.tl-row,.tl-t,.tl-ev,.tl-de,.fam-node,.rsvp-card,.rsvp-inner,.alb-sub,.alb-qr-wrap,.alb-hint')
    .forEach(x=>{x.style.opacity=1;x.style.transform='none';});
}"""

def main():
    objetivos = [(a.split("=")[0], int(a.split("=")[1])) for a in sys.argv[1:]]
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 375, "height": 812}, device_scale_factor=2)
        pg.goto(URL, wait_until="load")
        pg.evaluate(ABRIR)
        pg.wait_for_timeout(2000)
        for nombre, offset in objetivos:
            sec = nombre.split(":")[0]
            pg.evaluate(
                "([id,off]) => { const e=document.getElementById(id); window.scrollTo(0, e.offsetTop + off); }",
                [sec, offset],
            )
            pg.wait_for_timeout(2200)
            pg.screenshot(path=f"shot_{nombre.replace(':','_')}.png")
            print("shot_" + nombre.replace(":", "_") + ".png")
        b.close()

main()
