# Casos de prueba — Calculadora Científica

Fecha: 2026-02-19

Resumen: colección de casos de prueba (manuales y automáticos) para la calculadora implementada en `Calculadora.py`.

Entorno
- Python 3.8+ (se probó en 3.12)
- Ejecutar tests automáticos con `pytest` desde el entorno virtual del proyecto

Cómo ejecutar (automático):

```bash
# activar entorno (Windows PowerShell ejemplo)
& .venv\Scripts\Activate.ps1
python -m pytest -q
```

Convenciones en los casos:
- ID: identificador único (TC###)
- Tipo: Unitario / Integración / Manual
- Prioridad: Alta / Media / Baja
- Precondición: estado inicial necesario
- Pasos: instrucciones para reproducir
- Entrada esperada: resultado esperado y tolerancias (si aplica)
- Automatizado: indica si existe test pytest equivalente

--------------------------------------------------

## Casos de prueba

- TC001 — Suma básica
  - Tipo: Unitario
  - Prioridad: Alta
  - Precondición: calculadora en estado limpio (`C` o `clear_all()`)
  - Pasos: introducir `2`, `+`, `3`, pulsar `=` (o `calculate()`)
  - Resultado esperado: `5`
  - Automatizado: sí (`test_sum`)

- TC002 — Resta básica
  - Tipo: Unitario
  - Prioridad: Alta
  - Pasos: `5 - 7 =`
  - Resultado esperado: `-2`
  - Automatizado: sí (puede añadirse a suite)

- TC003 — Multiplicación básica
  - Tipo: Unitario
  - Prioridad: Alta
  - Pasos: `4 * 2.5 =`
  - Resultado esperado: `10.0`
  - Automatizado: sí

- TC004 — División básica
  - Tipo: Unitario
  - Prioridad: Alta
  - Pasos: `10 / 2 =`
  - Resultado esperado: `5.0` o `5`
  - Automatizado: sí

- TC005 — División por cero
  - Tipo: Unitario
  - Prioridad: Alta
  - Pasos: `1 / 0 =`
  - Resultado esperado: pantalla muestra `ERROR` (operación controlada)
  - Automatizado: sí (`test_division_by_zero`)

- TC006 — Reciprocidad (1/x) con cero
  - Tipo: Unitario
  - Prioridad: Alta
  - Pasos: introducir `0`, pulsar `1/x` (`reciprocal()`)
  - Resultado esperado: `ERROR`
  - Automatizado: sí (`test_reciprocal_zero`)

- TC007 — Precedencia de operadores
  - Tipo: Integración
  - Prioridad: Alta
  - Pasos: `2 + 3 * 4 =`
  - Resultado esperado: `14` (comprobar que `*` tiene precedencia)
  - Automatizado: sí (`test_precedence`)

- TC008 — Precisión flotante
  - Tipo: Unitario
  - Prioridad: Media
  - Pasos: `0.1 + 0.2 =`
  - Resultado esperado: aproximación a `0.3` con tolerancia (ej. 1e-9)
  - Automatizado: sí (`test_float_precision`)

- TC009 — Toggle signo tras resultado
  - Tipo: Unitario
  - Prioridad: Media
  - Pasos: calcular `2 + 3 =` (resultado `5`), pulsar `±`
  - Resultado esperado: pantalla `-5`
  - Automatizado: sí (`test_toggle_sign_after_result`)

- TC010 — Backspace y Clear
  - Tipo: Unitario
  - Prioridad: Media
  - Pasos: introducir `12`, `←` -> resultado `1`; pulsar `C` -> `0`
  - Resultado esperado: comportamiento descrito
  - Automatizado: sí (`test_backspace_and_clear`)

- TC011 — Memoria (M+, MR, MC, M-)
  - Tipo: Integración
  - Prioridad: Alta
  - Precondición: memoria inicial 0
  - Pasos: introducir `10`, `M+`; limpiar, introducir `5`, `M+`; `MR` -> debe mostrar `15`; `MC` -> `MR` -> `0`
  - Resultado esperado: memoria suma/resta y recall correctos
  - Automatizado: sí (`test_memory_operations`)

- TC012 — Factorial (n!)
  - Tipo: Unitario
  - Prioridad: Media
  - Pasos: introducir `5`, pulsar `n!` (o `factorial(5)`), `=` si aplica
  - Resultado esperado: `120`
  - Automatizado: opcional

- TC013 — Potencia (x^y)
  - Tipo: Unitario
  - Prioridad: Media
  - Pasos: `2 x^y 3 =` (o `2 ** 3`)
  - Resultado esperado: `8`

- TC014 — Raíz cuadrada
  - Tipo: Unitario
  - Prioridad: Media
  - Pasos: `√ 9` o `sqrt(9)`
  - Resultado esperado: `3.0`

- TC015 — Funciones trigonométricas
  - Tipo: Unitario
  - Prioridad: Media
  - Pasos: `sin(pi/2)` -> `1` (aceptar tolerancia); `cos(0)` -> `1`
  - Nota: comprobar que `pi` está disponible como constante

- TC016 — Logaritmos
  - Tipo: Unitario
  - Prioridad: Media
  - Pasos: `ln` -> `log` natural; `log10` para base 10
  - Ejemplo: `log(1)` -> `0`

- TC017 — Entradas inválidas
  - Tipo: Unitario / Robustez
  - Prioridad: Alta
  - Pasos: introducir `'a'` o cadena vacía y ejecutar
  - Resultado esperado: mostrar `ERROR`, no bloquear la app

- TC018 — Expresiones con paréntesis
  - Tipo: Integración
  - Prioridad: Media
  - Pasos: `(2 + 3) * 4 =`
  - Resultado esperado: `20`

- TC019 — Números grandes / overflow razonable
  - Tipo: Unitario
  - Prioridad: Baja
  - Pasos: `999999999 * 999999999 =`
  - Resultado esperado: resultado correcto o manejo de excepción limpio

- TC020 — Comportamiento tras error
  - Tipo: Robustez
  - Prioridad: Alta
  - Pasos: provocar `ERROR` (ej. `1/0`), después intentar nueva operación `2+2=` 
  - Resultado esperado: la calculadora permite reiniciar y calcular correctamente (no queda bloqueada)

--------------------------------------------------

## Mapeo a tests automáticos
- Los tests actuales en `tests/test_calculadora.py` cubren una selección de los TC listados (suma, precedencia, división por cero, reciprocidad, precisión, toggle signo, backspace/clear, memoria).
- Test adicionales recomendados: factorial, potencia, funciones trig/log, entradas inválidas adicionales, números grandes.

## Criterios de aceptación de la suite
- Todos los casos de prioridad Alta deben pasar. 
- Errores deben mostrar `ERROR` y no provocar crash de la aplicación.

## Notas
- El módulo usa `eval()` con `from math import *` — evitar ejecutar entradas no confiables durante pruebas manuales.
- Para pruebas headless, la suite incluye un fixture que emula componentes Tk cuando Tcl/Tk no está disponible.

*** Fin del documento
