import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow,
    QMenu, QToolBar, QComboBox, QPushButton,
    QTabWidget, QPlainTextEdit, QTextEdit,
    QDockWidget, QListWidget, QStackedWidget
)
from PyQt6.QtGui import QAction, QIcon, QFont
from PyQt6.QtCore import Qt

from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl

from wandi_lib_manager import WandiLibManager

class WandiIDE(QMainWindow):
    def __init__(self):
        super().__init__()

        caminho_icone = os.path.join(os.path.dirname(__file__), "wandi.png")
        self.setWindowIcon(QIcon(caminho_icone))

        self.setWindowTitle("Wandi IDE")
        self.resize(1200, 800)

        self.setCorner(Qt.Corner.BottomRightCorner, Qt.DockWidgetArea.RightDockWidgetArea)

        self._create_menu()
        self._create_toolbar()
        self._create_central()
        self._create_console_dock()
        self._create_unified_dock()
        
        self._create_statusbar()
        self._adjust_initial_layout()

        # --- ESTILO: PROJETO (AZUL) E MENSAGEIRO (CINZA) ---
        
        # Borda na lateral (Projeto)
        self.project_dock.setStyleSheet("""
            QDockWidget > QWidget {
                border-left: 1px solid #0078d4; 
                background-color: #1e1e1e;
            }
            QDockWidget::title {
                background-color: #1e1e1e;
                border-left: 1px solid #0078d4;
                border-bottom: 1px solid #333;
                padding-left: 10px;
                color: #888;
            }
        """)

        # Borda cinza no topo (Mensageiro) - AGORA FIXO
        self.console_dock.setStyleSheet("""
            QDockWidget > QWidget {
                border-top: 1px solid #555555; 
                background-color: #1e1e1e;
            }
            QDockWidget::title {
                background-color: #1e1e1e;
                border-top: 1px solid #555555;
                border-bottom: 1px solid #333;
                padding-left: 10px;
                color: #888;
            }
        """)

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
        
        self.btn_3d = QPushButton("3D")
        self.btn_3d.clicked.connect(lambda: self._switch_view(0, "Simulação 3D"))
        toolbar.addWidget(self.btn_3d)

        self.btn_lib = QPushButton("Biblioteca")
        self.btn_lib.clicked.connect(lambda: self._switch_view(1, "Biblioteca"))
        toolbar.addWidget(self.btn_lib)

    # ─ CENTRAL (EDITOR) ─
    def _create_central(self):
        self.editor_tabs = QTabWidget()
        editor = QPlainTextEdit()
        editor.setPlainText("def setup():\n    pass\n\ndef loop():\n    pass")
        self.editor_tabs.addTab(editor, "wandicode.py")
        self.setCentralWidget(self.editor_tabs)

    # ─ CONSOLE (MENSAGEIRO) ─
    def _create_console_dock(self):
        self.console_dock = QDockWidget("Mensageiro", self)
        
        # AJUSTE: Removido 'Movable' para ele não sair da base (não voar)
        self.console_dock.setAllowedAreas(Qt.DockWidgetArea.BottomDockWidgetArea)
        self.console_dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetClosable)

        tabs = QTabWidget()
        output = QTextEdit()
        output.setReadOnly(True)
        serial = QTextEdit()
        serial.setReadOnly(True)
        tabs.addTab(output, "Output")
        tabs.addTab(serial, "Serial")
        self.console_dock.setWidget(tabs)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.console_dock)
        self.console_dock.hide()

    # ─ UNIFIED DOCK ─
    def _create_unified_dock(self):
        self.project_dock = QDockWidget("Simulação 3D", self)
        self.project_stack = QStackedWidget()
        
        self.simulation_view = QWebEngineView()
        self.simulation_view.load(QUrl("https://simulation-one.vercel.app/"))
        
        self.library_manager = WandiLibManager()

        self.project_stack.addWidget(self.simulation_view)
        self.project_stack.addWidget(self.library_manager)

        self.project_dock.setWidget(self.project_stack)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.project_dock)

    def _switch_view(self, index, title):
        self.project_stack.setCurrentIndex(index)
        self.project_dock.setWindowTitle(title)
        self.project_dock.show()

    def _adjust_initial_layout(self):
        largura_projeto = int(self.width() * 0.6)
        self.resizeDocks([self.project_dock], [largura_projeto], Qt.Orientation.Horizontal)

    def _create_statusbar(self):
        self.statusBar().showMessage("Pronto")

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