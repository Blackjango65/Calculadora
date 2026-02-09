# Manual de Usuario — Calculadora Científica

**Visión general**

Esta aplicación es una calculadora científica con interfaz gráfica (Tkinter). Permite realizar operaciones aritméticas básicas y funciones científicas comunes (trigonometría, logaritmos, factorial, potencias, raíces), además de contar con funciones de memoria.

**Requisitos**

- Python 3.x (Tkinter incluido en la instalación estándar)
- No se requieren dependencias externas adicionales

**Instalación y ejecución**

1. Abrir una terminal en la carpeta del proyecto (donde está `Calculadora.py`).
2. Ejecutar:

```bash
python Calculadora.py
```

La ventana de la calculadora se abrirá con tamaño por defecto `420x520`.

**Descripción de la interfaz**

- Pantalla (display): muestra la expresión en construcción o el resultado.
- Botones organizados en una cuadrícula con las siguientes filas (de arriba abajo):
  - MC, MR, M+, M-, ←, C
  - sin, cos, tan, ln, log, √
  - 7, 8, 9, /, %, (
  - 4, 5, 6, *, x^y, )
  - 1, 2, 3, -, n!, 1/x
  - ±, 0, ., +, π, =

**Funciones y botones (resumen)**

- MC: borrado de memoria (pone memoria a 0.0).
- MR: recupera el valor de memoria y lo muestra en pantalla.
- M+: suma el valor actual a la memoria.
- M-: resta el valor actual de la memoria.
- ← (Backspace): elimina el último carácter de la expresión.
- C: borra la expresión y reinicia la pantalla a 0.
- `sin`, `cos`, `tan`: añade la llamada a la función trigonométrica (`sin(`, `cos(`, `tan(`).
- `ln`: añade `log(` (logaritmo natural).
- `log`: añade `log10(` (logaritmo base 10).
- `√`: añade `sqrt(` (raíz cuadrada).
- `%`: operador módulo.
- `x^y`: inserta el operador de potencia `**`.
- `n!`: inserta `factorial(` (factorial; requiere entero no negativo).
- `1/x`: calcula la reciprocidad del valor mostrado (1/valor).
- `±`: cambia el signo del número actual.
- `π`: inserta la constante `pi`.
- `=`: evalúa la expresión y muestra el resultado.

**Atajos de teclado**

- Enter: equivale a `=` (calcular).
- Backspace: equivalente al botón `←`.

**Comportamiento importante**

- La calculadora construye una expresión en texto (`self.expr`) y la evalúa con `eval()` cuando se pulsa `=` u operaciones directas como `1/x`.
- Muchas funciones matemáticas están disponibles porque el módulo importa `from math import *`.
- Si `eval()` falla por entrada inválida o error (ej.: división por cero), la pantalla mostrará `ERROR`.

**Ejemplos de uso**

- Calcular (7 + 3) * 2:
  - Pulsar `7`, `+`, `3`, `*`, `2`, `=` → resultado `20`
- Calcular seno de 30 grados (convertir a radianes manualmente):
  - Escribir `sin(30*pi/180)` → `=` → resultado `0.5`
- Factorial de 5:
  - `5`, `n!`, `=` → resultado `120`

**Notas de seguridad y limitaciones**

- La aplicación usa `eval()` sobre la cadena de entrada; por tanto, no es seguro ejecutar entradas proporcionadas por usuarios no confiables en entornos sensibles.
- No hay sandboxing ni filtrado estricto de la expresión. Evitar introducir código arbitrario.

**Sugerencias y mantenimiento**

- Para añadir validación de entrada o evitar `eval()`, considere implementar un parser matemático (por ejemplo, `ast` con restricciones o una librería como `sympy` o `asteval`).
- Para internacionalización, extraer textos y etiquetas a un archivo de recursos.

**Contacto / Contribuciones**

- Este proyecto no incluye actualmente un sistema de issues; para cambios, editar el archivo `Calculadora.py` directamente.

---

Archivo: `Calculadora.py` — interfaz y lógica principal. Ejecutar para usar.
