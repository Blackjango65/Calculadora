#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Calculadora científica (interfaz Tkinter)

Este módulo implementa una calculadora científica básica con interfaz
gráfica usando Tkinter. Soporta operaciones aritméticas, funciones
trigonométricas y logarítmicas (usando las funciones importadas de
`math`), memoria simple (MC, MR, M+, M-) y operaciones como factorial,
raíz, potencia y reciprocidad.

Uso:
        Ejecutar directamente el archivo para abrir la ventana de la
        calculadora:

                python Calculadora.py

Notas de implementación:
        - La expresión se evalúa mediante `eval()` aprovechando las
            funciones importadas de `math`. No se realizan sanitizaciones
            avanzadas; evitar evaluar entradas no confiables.
        - Los textos y comentarios están en español.
"""

from tkinter import *
from math import *
import tkinter.font as tkfont

# Calculadora científica básica con apariencia similar a la de Windows

class Calculadora:
    """Clase principal de la calculadora.

    Parametros:
        root: instancia de `Tk` que actúa como ventana principal.
    """
    def __init__(self, root):
        self.root = root
        root.title("Calculadora Científica")
        root.resizable(False, False)
        self.expr = ""
        self.memory = 0.0
        self.last_result = False
        self.operators = {'+', '-', '*', '/', '%', '**'}

        # Estilos
        self.bg = "#f3f3f3"
        # Color para botones de operador: azul claro
        self.op_color = "#5bc0de"  # azul claro
        self.func_color = "#d9d9d9"
        self.digit_color = "#ffffff"
        root.configure(bg=self.bg)

        # Fuente
        self.font_display = tkfont.Font(family='Segoe UI', size=24, weight='bold')
        self.font_small = tkfont.Font(family='Segoe UI', size=10)
        self.font_button = tkfont.Font(family='Segoe UI', size=11)

        # Display
        self.input_text = StringVar()
        self.input_text.set('0')
        # Mostrar la expresión / resultado. Añadimos borde para crear un recuadro.
        self.display = Entry(root, font=self.font_display, textvariable=self.input_text,
                     bd=2, bg='#ffffff', justify='right', relief=RIDGE)
        self.display.grid(row=0, column=0, columnspan=6, sticky='nsew', padx=8, pady=(8,4))

        # Botones: fila por fila (label, command, color)
        rows = [
            [('MC', self.mem_clear, self.func_color), ('MR', self.mem_recall, self.func_color), ('M+', self.mem_add, self.func_color), ('M-', self.mem_sub, self.func_color), ('←', self.backspace, self.func_color), ('C', self.clear_all, self.func_color)],
            [('sin', lambda: self.add('sin('), self.func_color), ('cos', lambda: self.add('cos('), self.func_color), ('tan', lambda: self.add('tan('), self.func_color), ('ln', lambda: self.add('log('), self.func_color), ('log', lambda: self.add('log10('), self.func_color), ('√', lambda: self.add('sqrt('), self.func_color)],
            [('7', lambda: self.add('7'), self.digit_color), ('8', lambda: self.add('8'), self.digit_color), ('9', lambda: self.add('9'), self.digit_color), ('/', lambda: self.add('/'), self.op_color), ('%', lambda: self.add('%'), self.func_color), ('(', lambda: self.add('('), self.func_color)],
            [('4', lambda: self.add('4'), self.digit_color), ('5', lambda: self.add('5'), self.digit_color), ('6', lambda: self.add('6'), self.digit_color), ('*', lambda: self.add('*'), self.op_color), ('x^y', lambda: self.add('**'), self.func_color), (')', lambda: self.add(')'), self.func_color)],
            [('1', lambda: self.add('1'), self.digit_color), ('2', lambda: self.add('2'), self.digit_color), ('3', lambda: self.add('3'), self.digit_color), ('-', lambda: self.add('-'), self.op_color), ('n!', lambda: self.add('factorial('), self.func_color), ('1/x', lambda: self.reciprocal(), self.func_color)],
            [('±', lambda: self.toggle_sign(), self.func_color), ('0', lambda: self.add('0'), self.digit_color), ('.', lambda: self.add('.'), self.digit_color), ('+', lambda: self.add('+'), self.op_color), ('π', lambda: self.add('pi'), self.func_color), ('=', lambda: self.calculate(), self.op_color)],
        ]

        # Crear botones en grid
        for r, row in enumerate(rows, start=1):
            for c, (text, cmd, color) in enumerate(row):
                # Todos los botones tendrán un recuadro (borde) consistente
                b = Button(root, text=text, command=cmd, bg=color, fg='black', bd=2,
                           font=self.font_button, relief=RIDGE)
                b.grid(row=r, column=c, sticky='nsew', padx=4, pady=4)

        # Configurar pesos para que los botones mantengan forma
        for i in range(6):
            root.grid_columnconfigure(i, weight=1)
        for i in range(len(rows)+1):
            root.grid_rowconfigure(i, weight=1)

        # Bind teclado básico
        root.bind('<Return>', lambda e: self.calculate())
        root.bind('<BackSpace>', lambda e: self.backspace())

    # Operaciones sobre expr
    def add(self, s):
        """Añade texto a la expresión actual mostrada.

        Si el último valor mostrado fue el resultado de una operación y
        el usuario pulsa un operador, ese resultado se utiliza como
        primer operando. Si se pulsa un dígito o función, se inicia una
        nueva expresión.

        Argumentos:
            s: cadena a añadir (por ejemplo '7', '+', 'sin(')
        """
        # Si el último valor mostrado fue un resultado y se pulsa un operador,
        # usamos ese resultado como operando 1.
        if self.last_result:
            disp = self.input_text.get()
            if s in self.operators and disp not in ('ERROR', ''):
                self.expr = disp + str(s)
            else:
                # si se pulsa un dígito u otra función, empezamos nueva expresión
                self.expr = str(s)
            self.last_result = False
        else:
            self.expr += str(s)
        self.input_text.set(self.expr)

    def clear_all(self):
        """Limpia la expresión y resetea la pantalla."""
        self.expr = ''
        self.input_text.set('0')
        self.last_result = False

    def backspace(self):
        """Elimina el último carácter de la expresión actual."""
        self.expr = self.expr[:-1]
        self.input_text.set(self.expr if self.expr else '0')
        self.last_result = False

    def toggle_sign(self):
        """Invierte el signo del número actual.

        Si el último valor fue un resultado, se aplica el cambio sobre el
        valor mostrado; en caso contrario, se manipula la expresión
        actualmente en construcción.
        """
        if self.last_result:
            # aplicar signo al valor mostrado
            val = self.input_text.get()
            if val and val != 'ERROR':
                if val.startswith('-'):
                    val = val[1:]
                else:
                    val = '-' + val
                self.input_text.set(val)
                self.expr = val
                self.last_result = False
            return
        if not self.expr:
            return
        if self.expr.startswith('-'):
            self.expr = self.expr[1:]
        else:
            self.expr = '-' + self.expr
        self.input_text.set(self.expr)

    def reciprocal(self):
        """Calcula la reciprocidad (1/x) del valor actual.

        Muestra 'ERROR' si la operación falla (ej. división por cero o
        expresión inválida).
        """
        try:
            val = eval(self.expr)
            self.expr = str(1.0 / val)
            self.input_text.set(self.expr)
            self.last_result = True
        except Exception:
            self.input_text.set('ERROR')
            self.expr = ''
            self.last_result = False

    def mem_clear(self):
        """Borra la memoria (MC)."""
        self.memory = 0.0

    def mem_recall(self):
        """Recupera el valor de memoria y lo muestra en pantalla (MR)."""
        # muestra el valor de memoria en la pantalla
        self.input_text.set(str(self.memory))
        self.expr = str(self.memory)
        self.last_result = True

    def mem_add(self):
        """Suma el valor actual a la memoria (M+).

        Si la expresión es vacía se suma 0. Ignora errores silenciosamente.
        """
        try:
            val = eval(self.expr) if self.expr else 0.0
            self.memory += float(val)
        except Exception:
            pass

    def mem_sub(self):
        """Resta el valor actual de la memoria (M-)."""
        try:
            val = eval(self.expr) if self.expr else 0.0
            self.memory -= float(val)
        except Exception:
            pass

    def calculate(self):
        """Evalúa la expresión actual y muestra el resultado.

        Se utiliza `eval()` para evaluar la expresión; las funciones de
        `math` están disponibles gracias al `from math import *`.
        En caso de error se muestra 'ERROR'.
        """
        try:
            # Usamos eval con funciones de math ya importadas
            result = eval(self.expr)
            self.input_text.set(str(result))
            self.expr = ''
            self.last_result = True
        except Exception:
            self.input_text.set('ERROR')
            self.expr = ''
            self.last_result = False


if __name__ == '__main__':
    root = Tk()
    app = Calculadora(root)
    root.geometry('420x520')
    root.mainloop()