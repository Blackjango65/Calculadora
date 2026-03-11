"""
Fixtures compartidos para los tests de Playwright de la Calculadora Científica.
"""

import pytest
import threading
import http.server
from pathlib import Path


@pytest.fixture(scope="session")
def calculator_url():
    """Arranca un servidor HTTP local que sirve calculadora_web.html."""
    root_dir = str(Path(__file__).parent.parent)

    class _Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=root_dir, **kwargs)

        def log_message(self, format, *args):
            pass  # suprimir logs del servidor

    server = http.server.HTTPServer(("127.0.0.1", 0), _Handler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{port}/calculadora_web.html"
    server.shutdown()


@pytest.fixture
def calc_page(page, calculator_url):
    """Navega a la calculadora y devuelve la página Playwright lista."""
    page.goto(calculator_url)
    return page
