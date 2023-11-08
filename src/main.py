import sys
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import Qt
from gui.windows import MainWindow
from gui.dialogs import OpenDialog, ChoseFileDialog

if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    
    app = QApplication(sys.argv)

    malware_sample = None
    old_analysis = None
    
    open_dialog = OpenDialog()

    while malware_sample is None and old_analysis is None:
        result = open_dialog.exec_()
        
        if result == QDialog.Accepted:
            if open_dialog.new_analysis:

                new_analysis_dialog = ChoseFileDialog("Chose malware sample", "Binary Files (*.bin);;Executable Files (*.exe);;Text Files (*.txt);;All Files (*)")
                result = new_analysis_dialog.exec_()

                if result == QDialog.Accepted and new_analysis_dialog.file_name != "":
                    print("new analysis")
                    malware_sample = new_analysis_dialog.file_name
            
            else:
                open_analysis_dialog = ChoseFileDialog("Chose analysis", "Malware Analysis Supporter Files (*.masup)")
                result = open_analysis_dialog.exec_()

                if result == QDialog.Accepted and open_analysis_dialog.file_name != "":
                    print("open analysis")
                    old_analysis = open_analysis_dialog.file_name
        else:
            break

    if malware_sample or old_analysis:
        main_window = MainWindow(malware_sample=malware_sample, analysis_file=old_analysis)
        main_window.show()

        sys.exit(app.exec_())
