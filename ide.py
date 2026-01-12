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

        self._create_menu()
        self._create_toolbar()
        self._create_central()
        self._create_console_dock()
        self._create_simulation_dock()
        self._create_statusbar()


        # ⚠️ Ajuste deve vir DEPOIS de tudo criado
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

    # ─ CONSOLE (DOCK INFERIOR) ─
    def _create_console_dock(self):
        dock = QDockWidget("Mensageiro", self)
        dock.setAllowedAreas(Qt.DockWidgetArea.BottomDockWidgetArea)

        tabs = QTabWidget()

        output = QTextEdit()
        output.setReadOnly(True)
        output.setPlainText("Output do compilador...")

        serial = QTextEdit()
        serial.setReadOnly(True)
        serial.setPlainText("Serial Monitor...")

        tabs.addTab(output, "Output")
        tabs.addTab(serial, "Serial")

        dock.setWidget(tabs)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, dock)

    # ─ SIMULAÇÃO 3D (DOCK LIVRE) ─
    def _create_simulation_dock(self):
        self.simulation_dock = QDockWidget("Simulação 3D", self)

        self.simulation_dock.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea |
            Qt.DockWidgetArea.RightDockWidgetArea |
            Qt.DockWidgetArea.TopDockWidgetArea |
            Qt.DockWidgetArea.BottomDockWidgetArea
        )

        self.simulation_dock.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable |
            QDockWidget.DockWidgetFeature.DockWidgetFloatable |
            QDockWidget.DockWidgetFeature.DockWidgetClosable
        )

        # 🔹 ÁREA REAL DE SIMULAÇÃO (SEPARADA)
        self.simulation_view = QWebEngineView()
        self.simulation_view.load(QUrl("https://wandi3d.vercel.app"))
        self.simulation_dock.setWidget(self.simulation_view)


        self.addDockWidget(
            Qt.DockWidgetArea.RightDockWidgetArea,
            self.simulation_dock
        )

    # ─ AJUSTE 50% / 50% ─
    def _adjust_initial_layout(self):
        # Divide horizontalmente editor (central) e simulação
        self.resizeDocks(
            [self.simulation_dock],
            [self.width() // 2],
            Qt.Orientation.Horizontal
        )

    # ─ STATUS BAR ─
    def _create_statusbar(self):
        self.statusBar().showMessage("Pronto")

# -- TEMA --
def load_style(app):
    with open("style/dark.qss", "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WandiIDE()
    app.setFont(QFont("Consolas", 12))

    load_style(app)
    window.showMaximized()
    sys.exit(app.exec())
