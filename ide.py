import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow,
    QMenu, QToolBar, QComboBox, QPushButton,
    QTabWidget, QPlainTextEdit, QTextEdit,
    QDockWidget, QLabel
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt


class WandiIDE(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Wandi IDE")
        self.resize(1200, 800)

        self._create_menu()
        self._create_toolbar()
        self._create_central()
        self._create_console_dock()
        self._create_simulation_dock()
        self._create_statusbar()
        self._apply_style()


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
            "void setup() {\n"
            "    // setup\n"
            "}\n\n"
            "void loop() {\n"
            "    // loop\n"
            "}"
        )

        self.editor_tabs.addTab(editor, "wandicode.py")
        self.setCentralWidget(self.editor_tabs)

    # ─ CONSOLE (DOCK INFERIOR) ─
    def _create_console_dock(self):
        dock = QDockWidget("Console", self)
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

        placeholder = QLabel(
            "Área de Simulação 3D\n(OpenGL / PyBullet / Three.js futuramente)"
        )
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.simulation_dock.setWidget(placeholder)

        # posição inicial à direita
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

    def _apply_style(self):
        self.setStyleSheet("""
            /* ===== GERAL ===== */
            QMainWindow {
                background-color: #1e1e1e;
            }

            /* ===== MENU ===== */
            QMenuBar {
                background-color: #252526;
                color: #ffffff;
            }

            QMenuBar::item:selected {
                background-color: #3c3c3c;
            }

            QMenu {
                background-color: #252526;
                color: #ffffff;
                border: 1px solid #333;
            }

            QMenu::item:selected {
                background-color: #007acc;
            }

            /* ===== TOOLBAR ===== */
            QToolBar {
                background-color: #2d2d30;
                border-bottom: 1px solid #3c3c3c;
                spacing: 6px;
            }

            QToolButton {
                background-color: transparent;
                color: #ffffff;
                padding: 6px;
            }

            QToolButton:hover {
                background-color: #3c3c3c;
            }

            /* ===== EDITOR ===== */
            QPlainTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                font-family: Consolas, Courier New, monospace;
                font-size: 13px;
                selection-background-color: #264f78;
                border: none;
            }

            /* ===== TABS ===== */
            QTabWidget::pane {
                border-top: 1px solid #3c3c3c;
            }

            QTabBar::tab {
                background-color: #2d2d30;
                color: #cccccc;
                padding: 6px 12px;
                border: 1px solid #3c3c3c;
                border-bottom: none;
            }

            QTabBar::tab:selected {
                background-color: #1e1e1e;
                color: #ffffff;
            }

            /* ===== DOCK ===== */
            QDockWidget {
                titlebar-close-icon: none;
                titlebar-normal-icon: none;
            }

            QDockWidget::title {
                background-color: #2d2d30;
                color: #ffffff;
                padding: 6px;
            }

            /* ===== STATUS BAR ===== */
            QStatusBar {
                background-color: #007acc;
                color: white;
            }

            /* ===== COMBO / BUTTON ===== */
            QComboBox, QPushButton {
                background-color: #3c3c3c;
                color: white;
                border: 1px solid #555;
                padding: 4px;
            }

            QComboBox:hover, QPushButton:hover {
                background-color: #505050;
            }
        """)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WandiIDE()
    window.show()
    sys.exit(app.exec())
