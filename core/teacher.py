# Ayllu · v7 · módulo del PANEL DOCENTE
"""Tareas con estado real, estadísticas y últimas entregas en una sola llamada.

El docente no debe aprender el mapa de módulos: el panel le dice qué hacer
hoy, guarda lo que ya hizo y le muestra el resultado de lo que envió.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.db import get_store
from core.seed import now_iso as _now

TAREA_SEED = [
    {
        "id": 1,
        "key": "aviso",
        "title": "Enviar un aviso a tu clase",
        "detail": "Escribe un mensaje en castellano y Ayllu lo entrega traducido a la lengua de cada estudiante.",
        "action": "Abrir Mensajes",
        "route": "mensajeria",
        "done": False,
        "doneAt": None,
    },
    {
        "id": 2,
        "key": "documento",
        "detail": "Sube una ficha o un PDF y elige a quién se entrega ya traducido.",
        "title": "Compartir un documento con la clase",
        "action": "Subir documento",
        "route": "scan",
        "done": False,
        "doneAt": None,
    },
    {
        "id": 3,
        "key": "palabras",
        "title": "Revisar las palabras clave de tu materia",
        "detail": "El glosario decide cómo se traducen los términos difíciles: revísalo una vez y gana precisión todo el año.",
        "action": "Abrir Palabras clave",
        "route": "glossary",
        "done": False,
        "doneAt": None,
    },
]


def _account(store, user_id: Any) -> Optional[dict]:
    for row in store.select("users"):
        if str(row.get("id")) == str(user_id):
            return row
    return None


def _board_payload(store, user: Optional[dict]) -> dict:
    languages = store.select("languages")
    msgs = store.select("messages")
    threads = store.select("threads")
    tasks = store.select("tasks")
    tasks.sort(key=lambda r: r.get("id") or 0)
    deliveries = []
    for row in reversed(msgs[-6:]):
        deliveries.append(
            {
                "src": row.get("src"),
                "tgt": row.get("tgt"),
                "preview": (row.get("outText") or "")[:120],
                "createdAt": row.get("createdAt"),
                "kind": row.get("kind"),
            }
        )
    return {
        "user": {"name": (user or {}).get("name"), "role": (user or {}).get("role")},
        "stats": {
            "students": store.count("students"),
            "languages": len({m.get("tgt") for m in msgs if m.get("tgt")}),
            "languagesCatalog": len(languages),
            "glossaryTerms": store.count("glossary"),
            "messages": len(msgs),
            "threads": len(threads),
        },
        "tasks": [
            {
                "id": t.get("id"),
                "key": t.get("key"),
                "title": t.get("title"),
                "detail": t.get("detail"),
                "action": t.get("action"),
                "route": t.get("route"),
                "done": bool(t.get("done")),
            }
            for t in tasks
        ],
        "lastDeliveries": deliveries,
        "nextActions": [
            {"route": "mensajeria", "label": "Escribir a la clase", "hint": "El mensaje llega traducido a cada lengua"},
            {"route": "adapt", "label": "Traducir un texto", "hint": "Pega un fragmento y cópialo traducido"},
            {"route": "glossary", "label": "Revisar palabras clave", "hint": "Decide cómo se traducen los términos difíciles"},
            {"route": "ia", "label": "Ver la IA por dentro", "hint": "Motores usados, licencias y prueba rápida"},
        ],
    }


def board(user_id: Any = None) -> dict:
    """Todo lo que el docente necesita en una sola respuesta."""
    store = get_store()
    user = _account(store, user_id)
    return _board_payload(store, user)


def task_done(task_id: Any, user_id: Any = None) -> dict:
    """Marca una tarea como hecha (estado persistente) y devuelve el panel."""
    store = get_store()
    row = store.get("tasks", task_id)
    if not row:
        raise KeyError("tarea desconocida: %s" % task_id)
    store.update("tasks", task_id, {"done": True, "doneAt": _now()})
    return board(user_id)


def reset_tasks() -> None:
    """Vuelve a la lista inicial de tareas (útil para la demo y el selftest)."""
    store = get_store()
    for row in TAREA_SEED:
        store.update("tasks", row["id"], {"done": False, "doneAt": None})
