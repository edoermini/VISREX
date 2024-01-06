import sys

#sys.path.append('..')

from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6.QtGui import QIcon
from gui.windows import MainWindow
from gui.dialogs import MainDialog, ChoseFileDialog, ChangePathsDialog
from gui.utils import is_dark_theme_active
from analysis import Analysis

from constants import SET_MALWARE_SAMPLE_ACTIVITY
import pathlib
import resources_rc

if __name__ == '__main__':
    app = QApplication(sys.argv)

    malware_sample = None
    analysis = None
    analysis_file = ""
    
    main_dialog = MainDialog()
    main_dialog.setWindowIcon(QIcon(':/gui/assets/app_icon.png'))

    while malware_sample is None and analysis is None:
        result = main_dialog.exec_()
        
        if result == QDialog.Accepted:
            if main_dialog.new_analysis:

                new_analysis_dialog = ChoseFileDialog("Chose malware sample", "Binary Files (*.bin);;Executable Files (*.exe);;Text Files (*.txt);;All Files (*)")
                new_analysis_dialog.setWindowIcon(QIcon(':/gui/assets/app_icon.png'))
                result = new_analysis_dialog.exec_()

                if result == QDialog.Accepted and new_analysis_dialog.file_name != "":
                    malware_sample = new_analysis_dialog.file_name
            
            else:
                open_analysis_dialog = ChoseFileDialog("Chose analysis", "JSON Files (*.json)")
                open_analysis_dialog.setWindowIcon(QIcon(':/gui/assets/app_icon.png'))
                result = open_analysis_dialog.exec_()

                if result == QDialog.Accepted and open_analysis_dialog.file_name != "":
                    analysis_file = open_analysis_dialog.file_name
                    
                    analysis = Analysis.import_analysis(analysis_file)
                    paths = [entry.arguments[0] for entry in analysis.get_activity_log() if entry.activity == "Set malware sample"]

                    change_path_dialog = ChangePathsDialog(paths, is_dark_theme_active(open_analysis_dialog))
                    result = change_path_dialog.exec_()

                    if result == QDialog.Accepted:
                        path_index = 0
                        new_paths = change_path_dialog.getPaths()

                        for index, entry in enumerate(analysis.get_activity_log()):
                            if entry.activity == SET_MALWARE_SAMPLE_ACTIVITY:
                                entry.arguments = [str(pathlib.Path(new_paths[path_index]))]
                                analysis.update_log_entry(index, entry)
                                path_index += 1
                    else:
                        analysis = None
        else:
            break

    if malware_sample or analysis:
        main_window = MainWindow(malware_sample=malware_sample, analysis=analysis, analysis_file=analysis_file)
        main_window.setWindowIcon(QIcon(':/gui/assets/app_icon.png'))
        main_window.show()

        app.setWindowIcon(QIcon(':/gui/assets/app_icon.png'))
        sys.exit(app.exec_())
