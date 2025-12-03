from PyQt6.QtWidgets import QPushButton


class PeriodicTableButton(QPushButton):
    def __init__(self, element_data, parent_component=None):
        super().__init__(parent_component)
        self.element_data = element_data
        self._setup_button_appearance()

    def _setup_button_appearance(self):
        self.setFixedWidth(45)
        self.setFixedHeight(45)
        self.setText(
            f"{self.element_data.symbol}\n{self.element_data.atomic_number}"
        )
        self.setToolTip(f"{self.element_data.name}")
