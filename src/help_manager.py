from PyQt6.QtWidgets import QMessageBox


class HelpManager:
    @staticmethod
    def show_help(parent=None):
        from help_content import HELP_CONTENT

        QMessageBox.information(
            parent,
            "Справка по комбинациям клавиш",
            HELP_CONTENT
        )
