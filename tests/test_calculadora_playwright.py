"""
Tests automáticos con Playwright para la Calculadora Científica.

Cubren los 20 casos de prueba (TC001–TC020) definidos en CASOS_DE_PRUEBA.md.

Requisitos:
    pip install pytest-playwright
    playwright install chromium
"""

import pytest

# ── Helpers ──────────────────────────────────────────────────────────

CHAR_BTN = {
    "0": "btn-0", "1": "btn-1", "2": "btn-2", "3": "btn-3", "4": "btn-4",
    "5": "btn-5", "6": "btn-6", "7": "btn-7", "8": "btn-8", "9": "btn-9",
    ".": "btn-dot", "+": "btn-add", "-": "btn-sub", "*": "btn-mul",
    "/": "btn-div", "=": "btn-eq", "(": "btn-lparen", ")": "btn-rparen",
}


def click(page, *testids):
    """Pulsa una secuencia de botones por su data-testid."""
    for tid in testids:
        page.click(f'[data-testid="{tid}"]')


def display(page) -> str:
    """Devuelve el valor actual del display."""
    return page.input_value("#display")


def enter_digits(page, text: str):
    """Introduce dígitos/operadores carácter a carácter."""
    for ch in text:
        click(page, CHAR_BTN[ch])


# ── Suite de tests TC001–TC020 ───────────────────────────────────────

class TestCalculadoraPlaywright:
    """Suite Playwright que cubre los 20 casos de prueba."""

    # ─── Operaciones aritméticas básicas ────────────────────────────

    def test_tc001_suma_basica(self, calc_page):
        """TC001 — 2 + 3 = 5"""
        click(calc_page, "btn-2", "btn-add", "btn-3", "btn-eq")
        assert display(calc_page) == "5"

    def test_tc002_resta_basica(self, calc_page):
        """TC002 — 5 - 7 = -2"""
        click(calc_page, "btn-5", "btn-sub", "btn-7", "btn-eq")
        assert display(calc_page) == "-2"

    def test_tc003_multiplicacion_basica(self, calc_page):
        """TC003 — 4 × 2.5 = 10"""
        click(calc_page, "btn-4", "btn-mul", "btn-2", "btn-dot", "btn-5", "btn-eq")
        assert display(calc_page) == "10"

    def test_tc004_division_basica(self, calc_page):
        """TC004 — 10 / 2 = 5"""
        click(calc_page, "btn-1", "btn-0", "btn-div", "btn-2", "btn-eq")
        assert display(calc_page) == "5"

    # ─── Control de errores en división ─────────────────────────────

    def test_tc005_division_por_cero(self, calc_page):
        """TC005 — 1 / 0 = ERROR"""
        click(calc_page, "btn-1", "btn-div", "btn-0", "btn-eq")
        assert display(calc_page) == "ERROR"

    def test_tc006_reciprocidad_cero(self, calc_page):
        """TC006 — 0 → 1/x = ERROR"""
        click(calc_page, "btn-0", "btn-recip")
        assert display(calc_page) == "ERROR"

    # ─── Precedencia de operadores ──────────────────────────────────

    def test_tc007_precedencia_operadores(self, calc_page):
        """TC007 — 2 + 3 * 4 = 14 (multiplicación tiene precedencia)"""
        click(calc_page, "btn-2", "btn-add", "btn-3", "btn-mul", "btn-4", "btn-eq")
        assert display(calc_page) == "14"

    # ─── Precisión flotante ─────────────────────────────────────────

    def test_tc008_precision_flotante(self, calc_page):
        """TC008 — 0.1 + 0.2 ≈ 0.3 (tolerancia 1e-9)"""
        click(calc_page,
              "btn-0", "btn-dot", "btn-1", "btn-add",
              "btn-0", "btn-dot", "btn-2", "btn-eq")
        result = float(display(calc_page))
        assert abs(result - 0.3) < 1e-9

    # ─── Toggle de signo ────────────────────────────────────────────

    def test_tc009_toggle_signo_tras_resultado(self, calc_page):
        """TC009 — 2 + 3 = 5 → ± → -5"""
        click(calc_page, "btn-2", "btn-add", "btn-3", "btn-eq")
        assert display(calc_page) == "5"
        click(calc_page, "btn-sign")
        assert display(calc_page) == "-5"

    # ─── Backspace y Clear ──────────────────────────────────────────

    def test_tc010_backspace_y_clear(self, calc_page):
        """TC010 — 12 ← → 1 ; C → 0"""
        click(calc_page, "btn-1", "btn-2")
        assert display(calc_page) == "12"
        click(calc_page, "btn-backspace")
        assert display(calc_page) == "1"
        click(calc_page, "btn-clear")
        assert display(calc_page) == "0"

    # ─── Operaciones de memoria ─────────────────────────────────────

    def test_tc011_memoria(self, calc_page):
        """TC011 — 10 M+, C, 5 M+, MR → 15 ; MC, MR → 0"""
        # 10 → M+
        click(calc_page, "btn-1", "btn-0")
        click(calc_page, "btn-mplus")
        click(calc_page, "btn-clear")

        # 5 → M+
        click(calc_page, "btn-5")
        click(calc_page, "btn-mplus")

        # MR → debe mostrar 15
        click(calc_page, "btn-mr")
        assert display(calc_page) == "15"

        # MC → MR → debe mostrar 0
        click(calc_page, "btn-mc")
        click(calc_page, "btn-mr")
        assert display(calc_page) == "0"

    # ─── Funciones científicas ──────────────────────────────────────

    def test_tc012_factorial(self, calc_page):
        """TC012 — factorial(5) = 120"""
        click(calc_page, "btn-fact", "btn-5", "btn-rparen", "btn-eq")
        assert display(calc_page) == "120"

    def test_tc013_potencia(self, calc_page):
        """TC013 — 2 ^ 3 = 8"""
        click(calc_page, "btn-2", "btn-pow", "btn-3", "btn-eq")
        assert display(calc_page) == "8"

    def test_tc014_raiz_cuadrada(self, calc_page):
        """TC014 — √9 = 3"""
        click(calc_page, "btn-sqrt", "btn-9", "btn-rparen", "btn-eq")
        assert display(calc_page) == "3"

    def test_tc015_funciones_trigonometricas(self, calc_page):
        """TC015 — sin(π/2) ≈ 1 ; cos(0) ≈ 1"""
        # sin(π/2)
        click(calc_page, "btn-sin", "btn-pi", "btn-div", "btn-2", "btn-rparen", "btn-eq")
        assert abs(float(display(calc_page)) - 1.0) < 1e-9

        # cos(0)
        click(calc_page, "btn-clear")
        click(calc_page, "btn-cos", "btn-0", "btn-rparen", "btn-eq")
        assert abs(float(display(calc_page)) - 1.0) < 1e-9

    def test_tc016_logaritmos(self, calc_page):
        """TC016 — ln(1) = 0 ; log10(10) = 1"""
        # ln(1) → log(1) = 0
        click(calc_page, "btn-ln", "btn-1", "btn-rparen", "btn-eq")
        assert display(calc_page) == "0"

        # log10(10) = 1
        click(calc_page, "btn-clear")
        click(calc_page, "btn-log", "btn-1", "btn-0", "btn-rparen", "btn-eq")
        assert abs(float(display(calc_page)) - 1.0) < 1e-9

    # ─── Robustez ───────────────────────────────────────────────────

    def test_tc017_entradas_invalidas(self, calc_page):
        """TC017 — expresión inválida → ERROR, sin bloquear la app"""
        # Inyectar expresión inválida y evaluar
        calc_page.evaluate("calculator.expr = 'abc'")
        click(calc_page, "btn-eq")
        assert display(calc_page) == "ERROR"

    # ─── Paréntesis ─────────────────────────────────────────────────

    def test_tc018_parentesis(self, calc_page):
        """TC018 — (2 + 3) × 4 = 20"""
        click(calc_page,
              "btn-lparen", "btn-2", "btn-add", "btn-3",
              "btn-rparen", "btn-mul", "btn-4", "btn-eq")
        assert display(calc_page) == "20"

    # ─── Números grandes ────────────────────────────────────────────

    def test_tc019_numeros_grandes(self, calc_page):
        """TC019 — 999999999 × 999999999 → resultado numérico válido"""
        enter_digits(calc_page, "999999999")
        click(calc_page, "btn-mul")
        enter_digits(calc_page, "999999999")
        click(calc_page, "btn-eq")
        result = display(calc_page)
        assert result != "ERROR", "No debería dar error con números grandes"
        float(result)  # debe ser convertible a número

    # ─── Comportamiento tras error ──────────────────────────────────

    def test_tc020_comportamiento_tras_error(self, calc_page):
        """TC020 — tras ERROR (1/0), la calculadora permite operar: 2+2=4"""
        # Provocar ERROR
        click(calc_page, "btn-1", "btn-div", "btn-0", "btn-eq")
        assert display(calc_page) == "ERROR"

        # Nueva operación normal
        click(calc_page, "btn-2", "btn-add", "btn-2", "btn-eq")
        assert display(calc_page) == "4"
