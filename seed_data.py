# Ayllu · quy_Latn · núcleo v3 · aula bilingüe con dos roles · ver CAMBIOS_V3_0.txt
#!/usr/bin/env python3
"""Siembra Supabase con los datos demo de Ayllu.

    python seed_data.py --check     # muestra el estado sin qillqay
    python seed_data.py --write     # inserta la muhu en Supabase
    python seed_data.py --reset     # reinicia el almacén en memoria

Requiere SUPABASE_URL y SUPABASE_KEY en el entorno para ``--write``.
"""

from __future__ import annotations

import argparse
import sys

from core.db import SupabaseStore, get_store, reset_store
from core.services import get_service


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Semilla de datos de Ayllu")
    parser.add_argument("--check", action="store_true", help="estado actual")
    parser.add_argument("--write", action="store_true", help="escribe en Supabase")
    parser.add_argument("--reset", action="store_true", help="reinicia el almacén")
    args = parser.parse_args(argv)

    if args.reset:
        reset_store()
        get_service().reset()
        print("Almacén reiniciado con la semilla embebida.")
        return 0

    store = get_store()
    if args.write:
        if not isinstance(store, SupabaseStore):
            print("Sin SUPABASE_URL/SUPABASE_KEY: uso el modo degradado en memoria.")
            return 1
        service = get_service()
        from core import seed

        for row in seed.LANGUAGES:
            store.insert("languages", row)
        for row in service.list_communities():
            pass
        for row in seed.COMMUNITIES:
            store.insert("communities", row)
        for row in seed.STUDENTS:
            store.insert("students", row)
        for row in seed.GLOSSARY:
            store.insert("glossary", row)
        for row in seed.MATERIALS:
            store.insert("materials", row)
        for row in seed.USERS:
            store.insert("users", row)
        # v5 · mensajería: primero las conversaciones, luego sus mensajes.
        for row in seed.build_threads():
            store.insert("threads", row)
        for row in seed.build_messages():
            store.insert("messages", row)
        print("Semilla escrita en Supabase (cuentas de dos roles, aula bilingüe y mensajería).")
        return 0

    info = store.info()
    print("modo:", info.get("mode"))
    for table, count in sorted((info.get("tables") or {}).items()):
        print("  %-12s %3d filas" % (table, count))
    return 0


if __name__ == "__main__":
    sys.exit(main())
