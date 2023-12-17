import sys

sys.path.append('..')

from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6.QtGui import QIcon
from gui.windows import MainWindow
from gui.dialogs import MainDialog, ChoseFileDialog

if __name__ == '__main__':
    app = QApplication(sys.argv)

    malware_sample = None
    analysis_file = None
    
    main_dialog = MainDialog()
    main_dialog.setWindowIcon(QIcon('gui/assets/app_icon.png'))

    while malware_sample is None and analysis_file is None:
        result = main_dialog.exec_()
        
        if result == QDialog.Accepted:
            if main_dialog.new_analysis:

                new_analysis_dialog = ChoseFileDialog("Chose malware sample", "Binary Files (*.bin);;Executable Files (*.exe);;Text Files (*.txt);;All Files (*)")
                new_analysis_dialog.setWindowIcon(QIcon('gui/assets/app_icon.png'))
                result = new_analysis_dialog.exec_()

                if result == QDialog.Accepted and new_analysis_dialog.file_name != "":
                    malware_sample = new_analysis_dialog.file_name
            
            else:
                open_analysis_dialog = ChoseFileDialog("Chose analysis", "JSON Files (*.json)")
                open_analysis_dialog.setWindowIcon(QIcon('gui/assets/app_icon.png'))
                result = open_analysis_dialog.exec_()

                if result == QDialog.Accepted and open_analysis_dialog.file_name != "":
                    analysis_file = open_analysis_dialog.file_name
        else:
            break

    if malware_sample or analysis_file:
        main_window = MainWindow(malware_sample=malware_sample, analysis_file=analysis_file)
        main_window.setWindowIcon(QIcon('gui/assets/app_icon.png'))
        main_window.show()

        app.setWindowIcon(QIcon('./gui/assets/app_icon.png'))
        sys.exit(app.exec_())
