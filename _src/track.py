"""Sigue el sello a lo largo del video del sobre y graba M&J frame a frame.

La deteccion global (seal.detect_seal) solo sirve mientras el sobre esta cerrado:
al abrirse aparecen sombras y el interior del sobre, que ganan el
connected-components. A partir de ahi se sigue el sello por correlacion con el
sello del primer frame, dentro de una ROI y probando varias escalas — el sello
se aleja de la camara conforme la solapa gira, asi que su radio se reduce y un
template de tamano fijo deja de enganchar.
"""
import glob
import os
import numpy as np
import cv2
from PIL import Image

import seal

FRAMES = sorted(glob.glob("in/*.png"))
OUT = "out"
# la escala se lleva en absoluto respecto al frame 1 y solo puede derivar un
# poco por frame; si se compusiera escala sobre escala, el radio decaeria
# exponencialmente y el seguimiento se cortaria solo
STEPS = (1.06, 1.03, 1.0, 0.975, 0.95)
SCALE_MIN = 0.28
THR = 0.25


def match_in_roi(rgb, cx, cy, scale, tmpl0):
    """Mejor (x, y, escala, score) del sello dentro de la ROI."""
    h, w = rgb.shape[:2]
    pad = int(tmpl0.shape[0] * scale * 1.3)
    x0, y0 = max(0, int(cx - pad)), max(0, int(cy - pad))
    x1, y1 = min(w, int(cx + pad)), min(h, int(cy + pad))
    roi = cv2.cvtColor(rgb[y0:y1, x0:x1], cv2.COLOR_RGB2GRAY)
    best = None
    for st in STEPS:
        sc = scale * st
        if sc < SCALE_MIN or sc > 1.15:
            continue
        n = max(8, int(tmpl0.shape[0] * sc))
        if roi.shape[0] < n or roi.shape[1] < n:
            continue
        t = cv2.resize(tmpl0, (n, n), interpolation=cv2.INTER_AREA)
        res = cv2.matchTemplate(roi, t, cv2.TM_CCOEFF_NORMED)
        _, mx, _, loc = cv2.minMaxLoc(res)
        if best is None or mx > best[3]:
            best = (x0 + loc[0] + n / 2.0, y0 + loc[1] + n / 2.0, sc, mx)
    return best


def main():
    os.makedirs(OUT, exist_ok=True)
    first = np.asarray(Image.open(FRAMES[0]).convert("RGB"))
    s0 = seal.detect_seal(first)
    if s0 is None:
        raise SystemExit("no se detecto el sello en el frame 1")
    cx, cy, R0 = s0
    print(f"frame 1: cx={cx:.1f} cy={cy:.1f} r={R0:.1f}")

    t = int(R0 * 0.92)
    tmpl0 = cv2.cvtColor(
        first[int(cy) - t:int(cy) + t, int(cx) - t:int(cx) + t], cv2.COLOR_RGB2GRAY)

    # El umbral es laxo y quien valida es la continuidad: al primer frame que
    # falla se deja de buscar, porque mas alla el sello ya salio de cuadro o
    # se lo comio el flash final, y cualquier reenganche seria un falso positivo.
    track = []
    px, py, scale = cx, cy, 1.0
    for f in FRAMES:
        rgb = np.asarray(Image.open(f).convert("RGB"))
        m = match_in_roi(rgb, px, py, scale, tmpl0)
        lim = R0 * scale * 0.6
        if m is None or m[3] < THR or abs(m[0] - px) > lim or abs(m[1] - py) > lim:
            break
        px, py, scale = m[0], m[1], m[2]
        track.append((px, py, R0 * scale))
    track += [None] * (len(FRAMES) - len(track))
    ok = [i for i, p in enumerate(track) if p is not None]
    print(f"sello seguido en {len(ok)}/{len(track)} frames (hasta f{ok[-1]+1})")

    # suavizado: mediana movil de 5 (el sello se traslada y escala de forma
    # continua; sin esto el radio da saltos entre escalas discretas)
    arr = np.array([p if p else (np.nan,) * 3 for p in track], float)
    sm = arr.copy()
    for i in range(len(arr)):
        w = arr[max(0, i - 2):i + 3]
        w = w[~np.isnan(w[:, 0])]
        if len(w):
            sm[i] = np.median(w, axis=0)

    yy, xx = np.mgrid[0:first.shape[0], 0:first.shape[1]]
    done = 0
    for i, f in enumerate(FRAMES):
        dst = os.path.join(OUT, os.path.basename(f))
        rgb = np.asarray(Image.open(f).convert("RGB"))
        if track[i] is None:
            Image.fromarray(rgb).save(dst)
            continue
        cx, cy, r = (float(v) for v in sm[i])
        disc = ((xx - cx) ** 2 + (yy - cy) ** 2) <= (r * 0.5) ** 2
        # el sello se lava con el flash final: el grabado se atenua con el,
        # si no las letras quedarian flotando sobre el blanco
        if disc.sum() < 50:
            Image.fromarray(rgb).save(dst)
            continue
        dark = 1.0 - float(rgb[disc].mean()) / 255.0   # 1 = cera plena, 0 = blanco
        strength = float(np.clip((dark - 0.20) / 0.35, 0.0, 1.0))
        if strength < 0.08:
            Image.fromarray(rgb).save(dst)
            continue
        out, _ = seal.process(rgb, seal=(cx, cy, r), strength=strength)
        Image.fromarray(out).save(dst)
        done += 1
    print(f"grabados {done} frames")


if __name__ == "__main__":
    main()
