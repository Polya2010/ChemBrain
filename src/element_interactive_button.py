from PyQt6.QtWidgets import QPushButton

class ElementInteractiveButton(QPushButton):
    def __init__(self, chemical_element, parent=None):
        super().__init__(parent)
        self.chemical_element = chemical_element
        self._initialize_button_ui()
    
    def _initialize_button_ui(self):
        self.setFixedSize(45, 45)
        self.setText(f"{self.chemical_element.symbol}\n{self.chemical_element.atomic_num}")
        self.setToolTip(f"{self.chemical_element.full_name}")