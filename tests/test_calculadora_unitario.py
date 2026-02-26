"""
Tests unitarios directos (sin Playwright) para la Calculadora Científica.

Cubren los 20 casos de prueba (TC001–TC020) definidos en CASOS_DE_PRUEBA.md,
ejecutándose directamente contra la clase Calculadora de Calculadora.py.

Se utiliza un shim mínimo de Tkinter para instanciar la clase sin necesidad
de un server gráfico (Display / Tcl/Tk). Esto permite ejecutar los tests en
entornos headless o CI sin dependencias de GUI.

Ejecutar:
    python -m pytest tests/test_calculadora_unitario.py -v
"""

import sys
import types
import pytest
from unittest.mock import MagicMock


# ── Shim mínimo de Tkinter para poder instanciar Calculadora sin GUI ──

class _FakeStringVar:
    """Emula tkinter.StringVar lo justo para los tests."""
    def __init__(self, *a, **kw):
        self._val = ''
    def set(self, v):
        self._val = str(v)
    def get(self):
        return self._val


class _FakeWidget:
    """Widget fantasma que acepta cualquier llamada de configuración."""
    def __init__(self, *a, **kw):
        pass
    def grid(self, **kw):
        pass
    def configure(self, **kw):
        pass
    def config(self, **kw):
        pass
    def bind(self, *a, **kw):
        pass
    def grid_columnconfigure(self, *a, **kw):
        pass
    def grid_rowconfigure(self, *a, **kw):
        pass


class _FakeRoot(_FakeWidget):
    """Emula la ventana Tk raíz."""
    def title(self, *a):
        pass
    def resizable(self, *a):
        pass
    def geometry(self, *a):
        pass
    def mainloop(self):
        pass


class _FakeFont:
    """Emula tkinter.font.Font."""
    def __init__(self, *a, **kw):
        pass


def _install_tk_shim():
    """Instala módulos falsos de tkinter para que Calculadora.py se importe
    sin necesitar un entorno gráfico real."""

    fake_tk = types.ModuleType('tkinter')
    # Constantes y clases necesarias
    fake_tk.Tk = _FakeRoot
    fake_tk.StringVar = _FakeStringVar
    fake_tk.Entry = _FakeWidget
    fake_tk.Button = _FakeWidget
    fake_tk.RIDGE = 'ridge'
    fake_tk.RIGHT = 'right'
    # Wildcard imports de tkinter (from tkinter import *)
    fake_tk.__all__ = ['Tk', 'StringVar', 'Entry', 'Button', 'RIDGE', 'RIGHT']
    # Para que `from tkinter import *` funcione
    for name in fake_tk.__all__:
        pass  # ya están arriba

    fake_tkfont = types.ModuleType('tkinter.font')
    fake_tkfont.Font = _FakeFont

    sys.modules['tkinter'] = fake_tk
    sys.modules['tkinter.font'] = fake_tkfont


# Instalar shim antes de importar Calculadora
_install_tk_shim()

# Ahora sí importamos la clase
sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent.parent))
from Calculadora import Calculadora  # noqa: E402


# ── Fixture ──────────────────────────────────────────────────────────

@pytest.fixture
def calc():
    """Crea una instancia limpia de Calculadora para cada test."""
    root = _FakeRoot()
    c = Calculadora(root)
    return c


def display(c) -> str:
    """Devuelve el valor actual de la pantalla."""
    return c.input_text.get()


# ── Suite de tests TC001–TC020 ───────────────────────────────────────

class TestCalculadoraUnitario:
    """Suite unitaria que cubre los 20 casos de prueba directamente."""

    # ─── Operaciones aritméticas básicas ────────────────────────────

    def test_tc001_suma_basica(self, calc):
        """TC001 — 2 + 3 = 5"""
        calc.add('2')
        calc.add('+')
        calc.add('3')
        calc.calculate()
        assert display(calc) == '5'

    def test_tc002_resta_basica(self, calc):
        """TC002 — 5 - 7 = -2"""
        calc.add('5')
        calc.add('-')
        calc.add('7')
        calc.calculate()
        assert display(calc) == '-2'

    def test_tc003_multiplicacion_basica(self, calc):
        """TC003 — 4 * 2.5 = 10.0"""
        calc.add('4')
        calc.add('*')
        calc.add('2')
        calc.add('.')
        calc.add('5')
        calc.calculate()
        assert display(calc) == '10.0'

    def test_tc004_division_basica(self, calc):
        """TC004 — 10 / 2 = 5.0"""
        calc.add('1')
        calc.add('0')
        calc.add('/')
        calc.add('2')
        calc.calculate()
        result = display(calc)
        assert result in ('5', '5.0')

    # ─── Control de errores en división ─────────────────────────────

    def test_tc005_division_por_cero(self, calc):
        """TC005 — 1 / 0 = ERROR"""
        calc.add('1')
        calc.add('/')
        calc.add('0')
        calc.calculate()
        assert display(calc) == 'ERROR'

    def test_tc006_reciprocidad_cero(self, calc):
        """TC006 — 0 → 1/x = ERROR"""
        calc.add('0')
        calc.reciprocal()
        assert display(calc) == 'ERROR'

    # ─── Precedencia de operadores ──────────────────────────────────

    def test_tc007_precedencia_operadores(self, calc):
        """TC007 — 2 + 3 * 4 = 14 (multiplicación tiene precedencia)"""
        calc.add('2')
        calc.add('+')
        calc.add('3')
        calc.add('*')
        calc.add('4')
        calc.calculate()
        assert display(calc) == '14'

    # ─── Precisión flotante ─────────────────────────────────────────

    def test_tc008_precision_flotante(self, calc):
        """TC008 — 0.1 + 0.2 ≈ 0.3 (tolerancia 1e-9)"""
        calc.add('0')
        calc.add('.')
        calc.add('1')
        calc.add('+')
        calc.add('0')
        calc.add('.')
        calc.add('2')
        calc.calculate()
        result = float(display(calc))
        assert abs(result - 0.3) < 1e-9

    # ─── Toggle de signo ────────────────────────────────────────────

    def test_tc009_toggle_signo_tras_resultado(self, calc):
        """TC009 — 2 + 3 = 5 → ± → -5"""
        calc.add('2')
        calc.add('+')
        calc.add('3')
        calc.calculate()
        assert display(calc) == '5'
        calc.toggle_sign()
        assert display(calc) == '-5'

    # ─── Backspace y Clear ──────────────────────────────────────────

    def test_tc010_backspace_y_clear(self, calc):
        """TC010 — 12 ← → 1 ; C → 0"""
        calc.add('1')
        calc.add('2')
        assert display(calc) == '12'
        calc.backspace()
        assert display(calc) == '1'
        calc.clear_all()
        assert display(calc) == '0'

    # ─── Operaciones de memoria ─────────────────────────────────────

    def test_tc011_memoria(self, calc):
        """TC011 — 10 M+, C, 5 M+, MR → 15 ; MC, MR → 0"""
        # 10 → M+
        calc.add('1')
        calc.add('0')
        calc.mem_add()
        calc.clear_all()

        # 5 → M+
        calc.add('5')
        calc.mem_add()

        # MR → 15
        calc.mem_recall()
        assert display(calc) == '15.0'

        # MC → MR → 0
        calc.mem_clear()
        calc.mem_recall()
        assert display(calc) == '0.0'

    # ─── Funciones científicas ──────────────────────────────────────

    def test_tc012_factorial(self, calc):
        """TC012 — factorial(5) = 120"""
        calc.add('factorial(')
        calc.add('5')
        calc.add(')')
        calc.calculate()
        assert display(calc) == '120'

    def test_tc013_potencia(self, calc):
        """TC013 — 2 ** 3 = 8"""
        calc.add('2')
        calc.add('**')
        calc.add('3')
        calc.calculate()
        assert display(calc) == '8'

    def test_tc014_raiz_cuadrada(self, calc):
        """TC014 — sqrt(9) = 3.0"""
        calc.add('sqrt(')
        calc.add('9')
        calc.add(')')
        calc.calculate()
        assert display(calc) == '3.0'

    def test_tc015_funciones_trigonometricas(self, calc):
        """TC015 — sin(pi/2) ≈ 1 ; cos(0) ≈ 1"""
        # sin(pi/2)
        calc.add('sin(')
        calc.add('pi')
        calc.add('/')
        calc.add('2')
        calc.add(')')
        calc.calculate()
        assert abs(float(display(calc)) - 1.0) < 1e-9

        # cos(0)
        calc.clear_all()
        calc.add('cos(')
        calc.add('0')
        calc.add(')')
        calc.calculate()
        assert abs(float(display(calc)) - 1.0) < 1e-9

    def test_tc016_logaritmos(self, calc):
        """TC016 — log(1) = 0.0 ; log10(10) = 1.0"""
        # ln(1) = 0
        calc.add('log(')
        calc.add('1')
        calc.add(')')
        calc.calculate()
        assert float(display(calc)) == 0.0

        # log10(10) = 1
        calc.clear_all()
        calc.add('log10(')
        calc.add('1')
        calc.add('0')
        calc.add(')')
        calc.calculate()
        assert abs(float(display(calc)) - 1.0) < 1e-9

    # ─── Robustez ───────────────────────────────────────────────────

    def test_tc017_entradas_invalidas(self, calc):
        """TC017 — expresión inválida → ERROR, sin bloquear"""
        calc.expr = 'abc'
        calc.calculate()
        assert display(calc) == 'ERROR'

    # ─── Paréntesis ─────────────────────────────────────────────────

    def test_tc018_parentesis(self, calc):
        """TC018 — (2 + 3) * 4 = 20"""
        calc.add('(')
        calc.add('2')
        calc.add('+')
        calc.add('3')
        calc.add(')')
        calc.add('*')
        calc.add('4')
        calc.calculate()
        assert display(calc) == '20'

    # ─── Números grandes ────────────────────────────────────────────

    def test_tc019_numeros_grandes(self, calc):
        """TC019 — 999999999 * 999999999 → resultado válido"""
        for ch in '999999999':
            calc.add(ch)
        calc.add('*')
        for ch in '999999999':
            calc.add(ch)
        calc.calculate()
        result = display(calc)
        assert result != 'ERROR'
        assert int(result) == 999999999 * 999999999

    # ─── Comportamiento tras error ──────────────────────────────────

    def test_tc020_comportamiento_tras_error(self, calc):
        """TC020 — tras ERROR (1/0), la calculadora permite operar: 2+2=4"""
        # Provocar ERROR
        calc.add('1')
        calc.add('/')
        calc.add('0')
        calc.calculate()
        assert display(calc) == 'ERROR'

        # Nueva operación normal
        calc.add('2')
        calc.add('+')
        calc.add('2')
        calc.calculate()
        assert display(calc) == '4'
