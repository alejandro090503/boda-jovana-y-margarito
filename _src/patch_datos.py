import io

p = "../index.html"
s = io.open(p, encoding="utf-8").read()


def rep(o, n):
    global s
    if o not in s:
        raise SystemExit("NO ENCONTRADO: " + o[:70])
    s = s.replace(o, n, 1)


# 1. madre del novio
rep('      <p class="fam-role">Padres del Novio</p>\n      <p class="fam-names">Por confirmar</p>',
    '      <p class="fam-role">Madre del Novio</p>\n      <p class="fam-names">María de los Santos de Dios Bárcenas</p>')

# 2. no habra padrinos: fuera el titulo y el carrusel
ini = s.index('  <h2 class="ttl" style="margin-top:32px">Nuestros Padrinos</h2>')
fin = s.index("</section>", ini)
s = s[:ini] + s[fin:]

# 3. itinerario confirmado por el cliente
ini = s.index('    <div class="tl-row" data-side="left">')
fin = s.index('  </div>\n</section>', ini)
filas = [("left", "6:00 PM", "Ceremonia Civil", "MAERE Salón &amp; Jardín"),
         ("right", "7:30 PM", "Cena", "Servicio en mesa"),
         ("left", "8:30 PM", "Nuestro Vals", "Primer baile de esposos"),
         ("right", "9:00 PM", "Apertura de Pista", "¡Todos a bailar!")]
s = s[:ini] + "".join(
    '    <div class="tl-row" data-side="%s">\n'
    '      <div class="tl-orn"></div><div class="tl-pulse"></div><div class="tl-dot"></div>\n'
    '      <div class="tl-row-inner"><p class="tl-t">%s</p><p class="tl-ev">%s</p><p class="tl-de">%s</p></div>\n'
    '    </div>\n' % f for f in filas) + s[fin:]

# 4. vestimenta
rep('<div class="dc-fig-hint">Traje formal<br>Corbata o moño</div>',
    '<div class="dc-fig-hint">Traje formal<br>Corbata o moño opcional</div>')

# 5. mensaje de evento solo para adultos (texto del cliente)
rep('<p class="rsvp-adults-msg">Con todo cariño, hemos reservado esta celebración para los adultos. Agradecemos su comprensión.</p>',
    '<p class="rsvp-adults-msg">Queremos que esta noche sea una oportunidad para relajarse, bailar y disfrutar. Por eso nuestra boda será solo para adultos.</p>')

# la seccion de ubicaciones anunciaba "Recepcion"; el evento abre con la civil
rep('<p class="loc-type">✦  Recepción</p>', '<p class="loc-type">✦  Ceremonia Civil y Recepción</p>')
rep('&details=Recepci%C3%B3n+6:00+PM+en+MAERE',
    '&details=Ceremonia+Civil+6:00+PM+en+MAERE')

io.open(p, "w", encoding="utf-8").write(s)
print("datos actualizados")
