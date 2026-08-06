"""Sustituye las iniciales del sello de cera del sobre: A&F -> M&J.

El sello es cera vino oscura y las iniciales estan GRABADAS EN RELIEVE (mismo
color que la cera, se leen solo por la sombra y el filo de luz), no impresas en
dorado. Por eso no se pinta relleno: se reconstruye el relieve.

El color de la cera (#5a0e0e aprox.) ya cae dentro de la paleta del cliente
(#730e00 vino), asi que no se recolorea.

Se usa tanto para envelope.jpg como para cada frame de envelope-open.mp4.
"""
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageFilter

FONT = "C:/Users/aleja/boda-jovana-y-margarito/_src/Cinzel.ttf"
FONT_WEIGHT = 600


def detect_seal(rgb):
    """Devuelve (cx, cy, r) del sello de cera, o None si no aparece.

    La cera es lo unico realmente oscuro sobre el papel crema; el OPEN eliptico
    descarta el pliegue central y los relieves florales, que son lineas finas.
    """
    m = (rgb.astype(int).max(axis=2) < 110).astype(np.uint8) * 255
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN,
                         cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))
    n, lab, st, ct = cv2.connectedComponentsWithStats(m, 8)
    if n < 2:
        return None
    i = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    if st[i, cv2.CC_STAT_AREA] < 3000:
        return None
    x, y, w, h = st[i, :4]
    r = w / 2.0
    return (x + w / 2.0, y + r, r)


def erase_initials(rgb, cx, cy, r, r_in=0.50):
    """Borra el grabado del disco interior y reconstruye la superficie de cera.

    Las letras no tienen color propio: se detectan como desviacion de alta
    amplitud respecto a la iluminacion suave de la cera.
    """
    yy, xx = np.mgrid[0:rgb.shape[0], 0:rgb.shape[1]]
    rad = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / max(r, 1e-6)
    inner = rad < r_in
    if inner.sum() < 50:
        return rgb

    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY).astype(np.float32)
    smooth = cv2.GaussianBlur(gray, (0, 0), max(2.0, r * 0.20))
    dev = np.abs(gray - smooth)
    thr = max(4.0, float(np.percentile(dev[inner], 66)))

    m = ((dev > thr) & inner).astype(np.uint8) * 255
    if m.sum() == 0:
        return rgb
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    m = cv2.dilate(m, np.ones((3, 3), np.uint8), iterations=max(2, int(r * 0.022)))
    m[~inner] = 0
    out = cv2.inpaint(cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR), m,
                      max(3, int(r * 0.05)), cv2.INPAINT_NS)
    out = cv2.cvtColor(out, cv2.COLOR_BGR2RGB)

    # El inpaint deja un fantasma del trazo antiguo. Una mediana de radio amplio
    # sobre el disco lo borra conservando el gradiente direccional del brillo
    # (un promedio radial lo aplanaria). Se mezcla con borde suave para no
    # marcar el corte del disco.
    k = max(3, int(r * 0.11)) | 1
    med = cv2.medianBlur(out, k if k <= 5 else 5)
    for _ in range(3):
        med = cv2.medianBlur(med, 5)
    w = np.clip((r_in - rad) / max(r_in * 0.25, 1e-6), 0, 1)[..., None]
    return (out * (1 - w) + med * w).astype(np.uint8)


def _glyph_alpha(ch, font_path, target_h):
    """Alpha del glifo escalado para que su altura real sea target_h px."""
    probe = 200
    f = ImageFont.truetype(font_path, probe)
    try:
        f.set_variation_by_axes([FONT_WEIGHT])
    except Exception:
        pass
    bb = f.getbbox(ch)
    h = max(1, bb[3] - bb[1])
    px = max(8, int(probe * target_h / h))
    f = ImageFont.truetype(font_path, px)
    try:
        f.set_variation_by_axes([FONT_WEIGHT])
    except Exception:
        pass
    bb = f.getbbox(ch)
    w, h = max(1, bb[2] - bb[0]), max(1, bb[3] - bb[1])
    pad = 10
    lay = Image.new("L", (w + pad * 2, h + pad * 2), 0)
    ImageDraw.Draw(lay).text((pad - bb[0], pad - bb[1]), ch, font=f, fill=255)
    return lay


def draw_initials(rgb, cx, cy, r, left="M", right="J", amp="&", font_path=FONT,
                  strength=1.0):
    """Graba las iniciales en relieve: hueco con sombra propia y filo de luz.

    strength escala la intensidad para seguir el desvanecido del sello en el
    video (donde la cera casi no se ve, el grabado tampoco debe verse).
    """
    base = Image.fromarray(rgb).convert("RGBA")
    mask = Image.new("L", base.size, 0)

    letters = (
        (_glyph_alpha(left, font_path, r * 0.40), (cx - r * 0.22, cy - r * 0.19)),
        (_glyph_alpha(amp, font_path, r * 0.20), (cx - r * 0.01, cy + r * 0.02)),
        (_glyph_alpha(right, font_path, r * 0.40), (cx + r * 0.22, cy + r * 0.20)),
    )
    for g, (px, py) in letters:
        pos = (int(px - g.width / 2), int(py - g.height / 2))
        cur = mask.crop((pos[0], pos[1], pos[0] + g.width, pos[1] + g.height))
        mask.paste(ImageChops.lighter(cur, g), pos)

    off = max(2, int(round(r * 0.028)))
    blur = max(0.8, r * 0.016)

    # hueco: la letra rebajada oscurece levemente toda su superficie
    hollow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    hollow.putalpha(mask.point(lambda v: int(v * 0.45 * strength))
                    .filter(ImageFilter.GaussianBlur(blur * 0.6)))
    base.alpha_composite(hollow)

    # sombra interior arriba-izquierda (la luz entra desde arriba-izq)
    sh_mask = ImageChops.subtract(mask, ImageChops.offset(mask, off, off))
    sh = Image.new("RGBA", base.size, (0, 0, 0, 0))
    sh.putalpha(sh_mask.point(lambda v: int(v * 0.95 * strength))
                .filter(ImageFilter.GaussianBlur(blur)))
    base.alpha_composite(sh)

    # filo de luz en el canto inferior-derecho del hueco
    hi_mask = ImageChops.subtract(mask, ImageChops.offset(mask, -off, -off))
    hi = Image.new("RGBA", base.size, (255, 214, 196, 0))
    hi.putalpha(hi_mask.point(lambda v: int(v * 0.42 * strength))
                .filter(ImageFilter.GaussianBlur(blur)))
    base.alpha_composite(hi, (off, off))

    return np.asarray(base.convert("RGB"))


def process(rgb, initials=("M", "J"), seal=None, r_in=0.50, strength=1.0):
    s = seal or detect_seal(rgb)
    if s is None:
        return rgb, None
    cx, cy, r = s
    out = erase_initials(rgb, cx, cy, r, r_in)
    out = draw_initials(out, cx, cy, r, initials[0], initials[1], strength=strength)
    return out, s


if __name__ == "__main__":
    import sys
    src = sys.argv[1] if len(sys.argv) > 1 else "../assets/envelope.jpg"
    dst = sys.argv[2] if len(sys.argv) > 2 else "envelope_new.jpg"
    rgb = np.asarray(Image.open(src).convert("RGB"))
    out, s = process(rgb)
    print("seal:", s)
    Image.fromarray(out).save(dst, quality=95)
