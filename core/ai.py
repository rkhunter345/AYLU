# Ayllu · v7 · transparencia de la IA
"""Catálogo de motores de IA de repositorios abiertos + explicación de resultados.

Todos los repositorios fueron verificados (existencia, licencia y lenguas).
La explicación usa SIEMPRE el glosario validado: funciona sin internet y
sin claves, para que el docente entienda el resultado aun en modo degradado.
"""

from __future__ import annotations

from typing import Any, Dict, List

from core.db import get_store
from core.seed import LEXICON
import translator

# Verificados en GitHub / Hugging Face (octubre 2026).
ENGINE_CATALOG = [
    {
        "code": "nllb",
        "name": "NLLB-200 (Meta AI · fairseq)",
        "url": "https://github.com/facebookresearch/fairseq/tree/nllb",
        "license": "código MIT · pesos CC-BY-NC 4.0 (no comercial)",
        "what": "Traduce directamente entre 200+ lenguas, incluidas las de bajos recursos. Es el único que cubre aimara y guaraní de forma nativa.",
        "coverage": "aimara · guaraní · quechua (quy) · inglés · portugués · y 9 más del catálogo",
        "connect": "NLLB_API_URL o HF_API_URL",
    },
    {
        "code": "dl-translate",
        "name": "dl-translate (envoltorio de NLLB)",
        "url": "https://github.com/xhluca/dl-translate",
        "license": "MIT",
        "what": "Tres líneas de Python para usar NLLB-200 / m2m100 / mBART. La forma más corta de conectar el motor real a Ayllu.",
        "coverage": "las mismas lenguas del modelo elegido (NLLB = 200)",
        "connect": "pip install dl-translate",
    },
    {
        "code": "opus-mt",
        "name": "OPUS-MT (Helsinki-NLP)",
        "url": "https://github.com/Helsinki-NLP/Opus-MT",
        "license": "modelos CC-BY 4.0",
        "what": "Modelos Marian autoalojables con servicio web propio. Buen respaldo para las lenguas internacionales.",
        "coverage": "español · inglés · portugués · francés · alemán · italiano · ruso (no las originarias)",
        "connect": "servicio local services.json",
    },
    {
        "code": "argos",
        "name": "Argos Translate",
        "url": "https://github.com/argosopentech/argos-translate",
        "license": "MIT o CC0 (dual)",
        "what": "Traducción sin internet. Ideal para escuelas rurales sin conexión estable.",
        "coverage": "español · inglés · portugués y más (sin lenguas originarias)",
        "connect": "pip install argostranslate",
    },
    {
        "code": "libretranslate",
        "name": "LibreTranslate",
        "url": "https://github.com/LibreTranslate/LibreTranslate",
        "license": "AGPL-3.0 (exige publicar cambios)",
        "what": "API REST autoalojada sobre Argos, con Docker listo para el servidor de la escuela.",
        "coverage": "las de Argos (es/en/pt…)",
        "connect": "docker run libretranslate/libretranslate",
    },
    {
        "code": "americas",
        "name": "AmericasNLP (datos y baselines)",
        "url": "https://github.com/AmericasNLP/americasnlp2024",
        "license": "ver LICENSE del repositorio",
        "what": "Corpus y modelos de referencia para lenguas americanas: la base para afinar el quechua con hablantes nativos.",
        "coverage": "quechua · aimara · guaraní y 15 lenguas más",
        "connect": "entrenamiento propio",
    },
]


def engines_status() -> dict:
    """Estado real de la cadena de motores + catálogo verificado."""
    status = translator.engine_status()
    connected = []
    for row in ENGINE_CATALOG:
        code = row["code"]
        connected_flag = bool(status.get(code, {}).get("available")) if code in status else False
        if code == "dl-translate":
            connected_flag = bool(status.get("nllb", {}).get("localModel"))
        connected.append(
            dict(
                row,
                connected=connected_flag,
                status=("conectado" if connected_flag else "disponible para conectar"),
            )
        )
    return {"engines": connected, "chain": status}


def reverse_lexicon(target: str) -> Dict[str, str]:
    """lengua → castellano, para explicar las palabras del resultado."""
    inv: Dict[str, str] = {}
    for spa, other in LEXICON.get(target, {}).items():
        if other and other not in inv:
            inv[other] = spa
    return inv


def explain(text: str, tgt: str = "quy_Latn") -> dict:
    """Explica cómo Ayllu tradujo un texto: motor, cobertura y palabras usadas.

    Funciona sin internet: se apoya en el glosario validado (120 términos).
    """
    text = (text or "").strip()
    if not text:
        return {"bullets": [], "note": "Escribe un texto primero."}
    result = translator.translate(text, "spa_Latn", tgt)
    out_text = result.get("text") or ""
    inv = reverse_lexicon(tgt)
    hits: List[dict] = []
    for word in out_text.split():
        clean = word.strip(".,;:!?()«»\"'")
        spa = inv.get(clean)
        if spa and all(h["word"] != clean for h in hits):
            hits.append({"word": clean, "means": spa})
        if len(hits) >= 3:
            break
    engine = result.get("engine") or result.get("provider") or "glosario"
    coverage = result.get("coverage")
    bullets = [
        "Motor usado: %s." % engine,
        "Cobertura del léxico validado: %s." % (
            (
                "%d %%" % round(float(coverage) if float(coverage) > 1.5 else 100 * float(coverage))
            ) if coverage is not None else "sin dato"
        ),
    ]
    if hits:
        bullets.append(
            "Palabras tomadas del glosario validado: "
            + ", ".join("%s = %s" % (h["word"], h["means"]) for h in hits)
            + "."
        )
    if result.get("degraded"):
        bullets.append(
            "Modo degradado: sin motor neuronal conectado la salida es una glosa "
            "de vocabulario. Conéctalo en la sección «Motores de IA conectados»."
        )
    else:
        bullets.append("Motor neuronal conectado: la salida es una traducción completa.")
    store = get_store()
    bullets.append(
        "El glosario activo tiene %d términos revisables en «Palabras clave»."
        % store.count("glossary")
    )
    return {
        "bullets": bullets,
        "engine": engine,
        "degraded": bool(result.get("degraded")),
        "hits": hits,
        "note": "Explicación generada con el glosario validado de la escuela (offline).",
    }
