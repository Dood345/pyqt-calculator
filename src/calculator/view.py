from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class CalculatorView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aperture Science Quantum Number Cruncher")
        self.setMinimumSize(800, 500)  # Expanded for maximum data throughput!

        # Cave Johnson mandated QSS stylesheet soup
        import os

        style_path = os.path.join(os.path.dirname(__file__), "style.qss")
        if os.path.exists(style_path):
            with open(style_path, "r", encoding="utf-8") as f:
                self.base_style = f.read()
        else:
            self.base_style = ""

        # Inject Engineer Drawer specific styling
        self.base_style += """
        #engDrawer QPushButton {
            font-size: {font_14}px;
            padding: 2px;
        }
        """

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Computer Engineer Drawer
        self.drawer_widget = QWidget()
        self.drawer_widget.setObjectName("engDrawer")
        drawer_layout = QVBoxLayout(self.drawer_widget)
        main_layout.addWidget(self.drawer_widget, stretch=1)
        self.drawer_widget.setVisible(False)  # Collapsed by default

        drawer_label = QLabel("ENG DRAWER")
        drawer_label.setObjectName("drawerLabel")
        drawer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        drawer_layout.addWidget(drawer_label)

        self.radix_indicator = QLabel("RADIX: DEC")
        self.radix_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.radix_indicator.setStyleSheet(
            "color: #ff9900; font-weight: bold; margin-bottom: 10px;"
        )
        drawer_layout.addWidget(self.radix_indicator)

        drawer_grid = QGridLayout()
        drawer_layout.addLayout(drawer_grid)

        eng_btn_map = [
            ("HEX", 0, 0, 1, 1),
            ("DEC", 0, 1, 1, 1),
            ("OCT", 1, 0, 1, 1),
            ("BIN", 1, 1, 1, 1),
            ("AND", 2, 0, 1, 1),
            ("OR", 2, 1, 1, 1),
            ("XOR", 3, 0, 1, 1),
            ("<<", 3, 1, 1, 1),
            (">>", 4, 0, 1, 1),
            ("0x", 4, 1, 1, 1),
            ("0b", 5, 0, 1, 1),
            ("0o", 5, 1, 1, 1),
            ("A", 6, 0, 1, 1),
            ("B", 6, 1, 1, 1),
            ("C_hex", 7, 0, 1, 1),
            ("D", 7, 1, 1, 1),
            ("E", 8, 0, 1, 1),
            ("F", 8, 1, 1, 1),
        ]

        self.buttons = {}

        for item in eng_btn_map:
            key, row, col, row_span, col_span = item
            text = "C" if key == "C_hex" else key
            btn = QPushButton(text)
            btn.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )
            self.buttons[key] = btn
            drawer_grid.addWidget(btn, row, col, row_span, col_span)

        # Left Column for the standard calculator pad
        left_layout = QVBoxLayout()
        main_layout.addLayout(left_layout, stretch=2)

        # Branding and Toggle
        branding_layout = QHBoxLayout()

        self.btn_toggle_drawer = QPushButton("<")
        self.btn_toggle_drawer.setToolTip("Toggle Engineer Drawer")
        self.btn_toggle_drawer.setFixedSize(50, 50)
        self.btn_toggle_drawer.setStyleSheet(
            "font-size: 20px; font-weight: bold;"
        )
        branding_layout.addWidget(self.btn_toggle_drawer)

        branding = QLabel("APERTURE LABORATORIES\nQUANTUM CALCULATOR")
        branding.setObjectName("brandingLabel")
        branding.setAlignment(Qt.AlignmentFlag.AlignCenter)
        branding_layout.addWidget(branding)

        left_layout.addLayout(branding_layout)

        # Display screen
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        left_layout.addWidget(self.display)

        # Grid for buttons
        grid_layout = QGridLayout()
        left_layout.addLayout(grid_layout)

        # Right Column for History Logs
        right_layout = QVBoxLayout()
        main_layout.addLayout(right_layout, stretch=4)

        history_label = QLabel("EXPERIMENTAL LOG:")
        right_layout.addWidget(history_label)

        self.history_table = QTableWidget(0, 2)
        self.history_table.horizontalHeader().setVisible(False)
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.setShowGrid(False)
        self.history_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectItems
        )
        self.history_table.horizontalHeader().setStretchLastSection(True)
        self.history_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )
        self.history_table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        right_layout.addWidget(self.history_table)

        # Button matrix: (text, row, col, row_span, col_span)
        btn_map = [
            ("MC", 0, 0, 1, 1),
            ("MR", 0, 1, 1, 1),
            ("M+", 0, 2, 1, 1),
            ("(", 0, 3, 1, 1),
            (")", 0, 4, 1, 1),
            ("7", 1, 0, 1, 1),
            ("8", 1, 1, 1, 1),
            ("9", 1, 2, 1, 1),
            ("/", 1, 3, 1, 1),
            ("C", 1, 4, 1, 1),
            ("4", 2, 0, 1, 1),
            ("5", 2, 1, 1, 1),
            ("6", 2, 2, 1, 1),
            ("*", 2, 3, 1, 1),
            ("+", 2, 4, 1, 1),
            ("1", 3, 0, 1, 1),
            ("2", 3, 1, 1, 1),
            ("3", 3, 2, 1, 1),
            ("-", 3, 3, 1, 1),
            ("=", 3, 4, 2, 1),
            ("0", 4, 0, 1, 2),
            (".", 4, 2, 1, 1),
            ("√", 4, 3, 1, 1),
        ]

        for item in btn_map:
            text, row, col, row_span, col_span = item
            btn = QPushButton(text)
            btn.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )
            self.buttons[text] = btn
            if text == "=":
                btn.setObjectName("btnCalculate")
            elif text == "C":
                btn.setObjectName("btnClear")
            grid_layout.addWidget(btn, row, col, row_span, col_span)

        self._apply_scaled_style()

    def update_display(self, text: str):
        """Updates the text on the calculator screen."""
        self.display.setText(text)

    def update_history(self, history_list):
        """Updates the experimental logs on the side panel."""
        self.history_table.setRowCount(len(history_list))
        for row, (eq, ans) in enumerate(history_list):
            self.history_table.setItem(row, 0, QTableWidgetItem(eq))
            self.history_table.setItem(row, 1, QTableWidgetItem(f" = {ans}"))
        self.history_table.resizeRowsToContents()
        self.history_table.scrollToBottom()

    def _apply_scaled_style(self):
        """Applies quantum scaling to visual data parameters."""
        if getattr(self, "base_style", None):
            scale_w = self.width() / 800.0
            scale_h = self.height() / 500.0
            scale = min(scale_w, scale_h)

            qss = self.base_style.replace(
                "{font_14}", str(max(10, int(14 * scale)))
            )
            qss = qss.replace("{font_18}", str(max(10, int(18 * scale))))
            qss = qss.replace("{font_22}", str(max(12, int(22 * scale))))
            qss = qss.replace("{font_24}", str(max(14, int(24 * scale))))
            qss = qss.replace("{font_32}", str(max(18, int(32 * scale))))
            self.setStyleSheet(qss)

            if hasattr(self, "history_table"):
                self.history_table.resizeRowsToContents()

    def resizeEvent(self, event):
        """Mandatory visual re-calibration triggered by Lab Boy interference."""
        super().resizeEvent(event)
        self._apply_scaled_style()
