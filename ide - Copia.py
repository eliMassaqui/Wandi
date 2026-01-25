import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow,
    QMenu, QToolBar, QComboBox, QPushButton,
    QTabWidget, QPlainTextEdit, QTextEdit,
    QDockWidget, QLabel
)
from PyQt6.QtGui import QAction, QIcon, QFont
from PyQt6.QtCore import Qt

from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl


class WandiIDE(QMainWindow):
    def __init__(self):
        super().__init__()

        caminho_icone = os.path.join(os.path.dirname(__file__), "wandi.png")
        self.setWindowIcon(QIcon(caminho_icone))

        self.setWindowTitle("Wandi IDE")
        self.resize(1200, 800)

        # Garante que os docks laterais (Simulação) ocupem a altura total da janela
        self.setCorner(Qt.Corner.BottomRightCorner, Qt.DockWidgetArea.RightDockWidgetArea)

        self._create_menu()
        self._create_toolbar()
        self._create_central()
        self._create_console_dock()
        self._create_simulation_dock()
        self._create_statusbar()

        # Ajuste inicial de proporções
        self._adjust_initial_layout()

    # ─ MENU BAR ─
    def _create_menu(self):
        menu = self.menuBar()
        menu.addMenu(QMenu("Ficheiro", self))
        menu.addMenu(QMenu("Editar", self))
        menu.addMenu(QMenu("Wandi", self))
        menu.addMenu(QMenu("Mais", self))

    # ─ TOOLBAR ─
    def _create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        toolbar.addAction(QAction("Compilar", self))
        toolbar.addAction(QAction("Enviar", self))
        toolbar.addSeparator()

        board = QComboBox()
        board.addItems(["Arduino Uno", "Arduino Mega", "ESP32"])
        toolbar.addWidget(board)

        port = QComboBox()
        port.addItems(["COM3", "COM4", "/dev/ttyUSB0"])
        toolbar.addWidget(port)

        toolbar.addSeparator()
        toolbar.addWidget(QPushButton("Biblioteca"))

    # ─ CENTRAL (EDITOR) ─
    def _create_central(self):
        self.editor_tabs = QTabWidget()
        editor = QPlainTextEdit()
        editor.setPlainText(
            "def setup():\n"
            "    pass\n\n"
            "def loop():\n"
            "    pass"
        )
        self.editor_tabs.addTab(editor, "wandicode.py")
        self.setCentralWidget(self.editor_tabs)

    # ─ CONSOLE (DOCK ABAIXO DO EDITOR) ─
    def _create_console_dock(self):
        self.console_dock = QDockWidget("Mensageiro", self)
        
        tabs = QTabWidget()
        output = QTextEdit()
        output.setReadOnly(True)
        output.setPlainText("Output do compilador...")
        serial = QTextEdit()
        serial.setReadOnly(True)
        serial.setPlainText("Serial Monitor...")

        tabs.addTab(output, "Output")
        tabs.addTab(serial, "Serial")
        self.console_dock.setWidget(tabs)

        # Adiciona o dock na área inferior
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.console_dock)
        
        # Oculta por padrão conforme solicitado
        self.console_dock.hide()

    # ─ SIMULAÇÃO 3D (DOCK DIREITO) ─
    def _create_simulation_dock(self):
        self.simulation_dock = QDockWidget("Simulação 3D", self)
        self.simulation_dock.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable |
            QDockWidget.DockWidgetFeature.DockWidgetFloatable |
            QDockWidget.DockWidgetFeature.DockWidgetClosable
        )

        self.simulation_view = QWebEngineView()
        self.simulation_view.load(QUrl("https://simulation-one.vercel.app/"))
        self.simulation_dock.setWidget(self.simulation_view)

        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.simulation_dock)

    # ─ AJUSTE DE PROPORÇÃO ─
    def _adjust_initial_layout(self):
        # Aumentamos a largura da simulação para 60% da janela
        largura_simulacao = int(self.width() * 0.6)
        
        self.resizeDocks(
            [self.simulation_dock],
            [largura_simulacao],
            Qt.Orientation.Horizontal
        )

    def _create_statusbar(self):
        self.statusBar().showMessage("Pronto")

# -- TEMA --
def load_style(app):
    try:
        if os.path.exists("style/dark.qss"):
            with open("style/dark.qss", "r", encoding="utf-8") as f:
                app.setStyleSheet(f.read())
    except Exception as e:
        print(f"Erro ao carregar estilo: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WandiIDE()
    app.setFont(QFont("Consolas", 12))

    load_style(app)
    window.showMaximized()
    sys.exit(app.exec())