"""Sustituye Lato por Cormorant Garamond en toda la invitacion.

Cormorant aparenta mas fino y mas pequeno que Lato al mismo tamano, asi que
donde se cambia hay que subir peso y ~2px para no perder legibilidad.
Los digitos de la CLABE pasan a Playfair Display, que si tiene cifras solidas.
"""
import io
import re

p = "../index.html"
s = io.open(p, encoding="utf-8").read()

# --- ajustes puntuales ANTES del reemplazo global (usan el texto con Lato) ---
puntuales = [
    # body: es de quien heredan .lbl y todos los textos sin familia propia
    ("font-family:'Lato',sans-serif;font-weight:400;\n  overflow-x:hidden;margin:0 auto;",
     "font-family:'Cormorant Garamond',serif;font-weight:500;\n  overflow-x:hidden;margin:0 auto;"),

    # .btn — CTA
    ("font-family:'Lato',sans-serif;font-size:13px;letter-spacing:2.5px;text-transform:uppercase;font-weight:600;",
     "font-family:'Cormorant Garamond',serif;font-size:15px;letter-spacing:2.5px;text-transform:uppercase;font-weight:700;"),

    # .loc-med-tag
    ("  font-size:13px;letter-spacing:3px;text-transform:uppercase;\n  color:var(--gold);font-weight:700;text-align:center;\n  font-family:'Lato',sans-serif;",
     "  font-size:14px;letter-spacing:3px;text-transform:uppercase;\n  color:var(--gold);font-weight:700;text-align:center;\n  font-family:'Cormorant Garamond',serif;"),

    # .rsvp-pases-label
    (".rsvp-pases-label{font-family:'Lato',sans-serif;font-size:12px;font-weight:700;",
     ".rsvp-pases-label{font-family:'Cormorant Garamond',serif;font-size:14px;font-weight:700;"),

    # .rsvp-input
    ("font-family:'Lato',sans-serif;font-size:15px;font-weight:500;color:var(--cream);letter-spacing:.02em;",
     "font-family:'Cormorant Garamond',serif;font-size:17px;font-weight:600;color:var(--cream);letter-spacing:.02em;"),

    # .rsvp-btn
    ("font-family:'Lato',sans-serif;font-size:12px;font-weight:700;letter-spacing:.3em;text-transform:uppercase;color:#fff;",
     "font-family:'Cormorant Garamond',serif;font-size:15px;font-weight:700;letter-spacing:.3em;text-transform:uppercase;color:#fff;"),

    # .rsvp-deadline
    (".rsvp-deadline{display:inline-flex;align-items:center;gap:8px;margin-top:26px;font-family:'Lato',sans-serif;font-size:11px;",
     ".rsvp-deadline{display:inline-flex;align-items:center;gap:8px;margin-top:26px;font-family:'Cormorant Garamond',serif;font-size:13px;"),

    # .finput — venia en weight 300 (thin), prohibido
    ("font-family:'Lato',sans-serif;font-size:15px;font-weight:300;",
     "font-family:'Cormorant Garamond',serif;font-size:17px;font-weight:600;"),

    # CLABE: cifras -> Playfair Display (la excepcion permitida para digitos)
    (".gf-bk-clabe{font-family:'Lato',monospace;",
     ".gf-bk-clabe{font-family:'Playfair Display',serif;"),

    # .cal-dow
    ("  font-family:'Lato',sans-serif;\n  font-size:11px;letter-spacing:1.5px;text-transform:uppercase;font-weight:700;",
     "  font-family:'Cormorant Garamond',serif;\n  font-size:13px;letter-spacing:1.5px;text-transform:uppercase;font-weight:700;"),

    # .env-tap-hint (regla del template)
    ("  font-family:'Lato',sans-serif;\n  font-size:13px;letter-spacing:3px;text-transform:uppercase;font-weight:700;",
     "  font-family:'Cormorant Garamond',serif;\n  font-size:14px;letter-spacing:3px;text-transform:uppercase;font-weight:700;"),

    # .env-tap-hint (la que agregue con el sobre interactivo)
    (".env-tap-hint{font-family:'Lato',sans-serif;font-size:12px;font-weight:700;",
     ".env-tap-hint{font-family:'Cormorant Garamond',serif;font-size:14px;font-weight:700;"),
]

for viejo, nuevo in puntuales:
    if viejo not in s:
        raise SystemExit("NO ENCONTRADO: " + viejo[:70])
    s = s.replace(viejo, nuevo)

# --- red de seguridad: cualquier Lato que quede ---
s = s.replace("'Lato',sans-serif", "'Cormorant Garamond',serif")
s = s.replace("'Lato',monospace", "'Playfair Display',serif")
s = s.replace("'Lato'", "'Cormorant Garamond'")

# --- ya no se descarga Lato ---
s = s.replace("&family=Lato:wght@400;500;700", "")

io.open(p, "w", encoding="utf-8").write(s)

restantes = len(re.findall(r"Lato", s))
print("Lato restantes:", restantes)
print("sans genericas sueltas:", len(re.findall(r"(?i)Montserrat|Helvetica|Arial|system-ui", s)))
