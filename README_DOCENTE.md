# Ayllu · Guía para el docente

**Ayllu** es la ayudante del aula que traduce: escribes en castellano y tus estudiantes lo leen en su lengua; ellos escriben en su lengua y tú lo lees en castellano. No necesitas saber de computadoras: si sabes usar WhatsApp, sabes usar Ayllu.

---

## ¿Para qué sirve?

1. **Comunicarte con tu clase sin barreras.** Tus avisos, tareas y documentos llegan traducidos a la lengua de cada estudiante.
2. **Adaptar los materiales.** No solo traduce palabras: ajusta el vocabulario, la dificultad y los ejemplos a la comunidad de cada estudiante, y conserva siempre el original.
3. **Medir el progreso.** Ve qué cobertura tiene la traducción en cada lengua y cómo avanza cada estudiante.
4. **Conocer la IA que usa.** Ayllu funciona con motores de IA de repositorios abiertos de GitHub (NLLB-200 de Meta AI, Argos Translate, OPUS-MT, LibreTranslate y más). La app te dice cuál se usó en cada respuesta, qué licencia tiene y qué lenguas del aula cubre.

---

## ¿Cómo funciona por dentro? (en palabras sencillas)

- Escribes un texto → Ayllu lo pasa por una **cadena de motores de IA**: primero el motor neuronal (NLLB-200 si está conectado), luego el glosario validado de la escuela (120 términos), y así la palabra difícil siempre sale traducida igual.
- **Si no hay internet o el motor falla**, Ayllu no se rompe: entrega la versión con glosario y la marca con la etiqueta *glosa* para que sepas que conviene revisarla.
- El botón **«¿Por qué este resultado?»** (módulo Inteligencia artificial) te explica en frases simples qué motor se usó, qué palabras salieron del glosario y si hace falta revisión de un hablante nativo.
- Tus tareas del día quedan **guardadas**: si cierras y vuelves mañana, Ayllu recuerda lo que ya hiciste.

---

## Instalación (la hace una sola vez, la computadora del colegio)

```bash
unzip ayllu_quy_v7_FULL.zip
cd ayllu_quy_v3
pip install -r requirements.txt
python app.py
```

Abre el navegador en `http://127.0.0.1:5000` y listo. Para que toda la escuela entre desde otras computadoras:

```bash
gunicorn -w 2 -b 0.0.0.0:5000 app:app
```

(Con `docker run -p 5000:5000 libretranslate/libretranslate` puedes además activar el motor LibreTranslate y apuntar `NLLB_API_URL`/`HF_API_URL` al servicio de IA que prefieras — la app lo detecta sola.)

---

## Cómo se usa (4 pasos)

1. **Entra con un clic.** En la pantalla de entrada, toca tu nombre (Docente). No hay claves que recordar en la demo.
2. **Mira tu Panel docente.** Es la primera pantalla: te muestra **Tareas de hoy** (con botón «Marcar como hecho»), **cómo va tu clase** (estudiantes, lenguas activas, palabras clave, mensajes), **las últimas entregas al aula** y la sección **«¿Qué hago ahora?»** con 4 botones grandes.
3. **Escribe a tu clase.** Botón *Escribir a la clase* → eliges el estudiante o el aula → escribes en castellano → «Traducir y enviar». Cada quien lo recibe en su lengua.
4. **Prueba la IA cuando quieras.** Menú *Inteligencia artificial* → escribe un texto corto → «Traducir ahora» → «Explicar la última traducción». Verás el resultado y la explicación del motor usado.

Botones de ayuda siempre visibles arriba: **Ayuda** (guía de 5 pasos) y **A+** (letra más grande).

---

## Cuentas de demostración

| Rol | Correo | Clave |
|---|---|---|
| Docente | `docente@ayllu.pe` | `ayllu-docente` |
| Estudiante | `estudiante@ayllu.pe` | `ayllu-estudiante` |

---

## Idiomas

21 lenguas en el catálogo (castellano; quechua ayacuchano, cusqueño, ancashino y quichua ecuatoriano; aimara; guaraní; náhuatl; maya yucateco; inglés, portugués y 10 más). La interfaz se muestra en **Español, English, Português o Runasimi (quechua)** — se cambia en la rueda superior.

## Honestidad ante todo

Sin motor neuronal conectado, la salida es una **glosa de vocabulario**, no una traducción completa, y la app lo declara con la etiqueta *glosa*. Los textos en lenguas originarias son demostrativos y deben ser validados por hablantes nativos. Ayllu nunca inventa: si no puede traducir, lo dice.
