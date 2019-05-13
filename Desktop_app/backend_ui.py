
from PyQt5 import QtCore
from PyQt5 import QtWidgets, QtGui

import json

from meat_curing_mw import Ui_MeatCuringChamberMW
from pref_dialog import Ui_Preferences
import sys

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.ui = Ui_MeatCuringChamberMW()
        self.setFixedSize(538, 337)
        self.ui.setupUi(self)

        self.ui.labelConnVal.setStyleSheet("color: red")
        self.ui.labelDataLogStatVal.setStyleSheet("color: red")

        self.ui.lcdNumberCurTmp.setStyleSheet("color: red")
        self.ui.lcdNumberCurHum.setStyleSheet("color: red")

        self.ui.lcdNumberSetTmpVal.setStyleSheet("color: green")
        self.ui.lcdNumberSetHumVal.setStyleSheet("color: green")

        ''' Signals '''
        self.ui.actionQuit.triggered.connect(self.exitApp)
        self.ui.actionPref.triggered.connect(self.handle_pref)
        self.ui.pushButtonSetSetpointApply.clicked.connect(self.applySettings)
        self.ui.pushButtonExit.clicked.connect(self.exitApp)
        
    def applySettings(self):
        self.valTempSetPoint = self.ui.doubleSpinBoxSetSetPointTmp.value()
        self.valHumSetPoint = self.ui.doubleSpinBoxSetSetPointHum.value()
        self.ui.lcdNumberSetTmpVal.setProperty("value", self.valTempSetPoint)
        self.ui.lcdNumberSetHumVal.setProperty("value", self.valHumSetPoint)
    
    def handle_pref(self):
        self.pref = Preference()
        self.pref.show()
        self.pref.exec_()

    def exitApp(self):
        sys.exit()

class Dialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)

class FileDialog(QtWidgets.QFileDialog):
    def __init__(self, parent=None):
        QtWidgets.QFileDialog.__init__(self, parent)

class Preference(Dialog, FileDialog):
    def __init__(self, parent=None):
        Dialog.__init__(self, parent)
        FileDialog.__init__(self, parent)
        self.ui = Ui_Preferences()
        self.setFixedSize(361, 193)
        self.ui.setupUi(self)

        try:
            with open("pref.json", "rb") as pref_val:
                self.pref_data = json.load(pref_val)
                print(self.pref_data)
                
            self.ui.lineEditBrokerIP.setText(self.pref_data["mqtt_broker_ip"])
            self.ui.lineEditBrokerPort.setText(str(self.pref_data["mqtt_broker_port"]))

            if(self.pref_data["data_log_stat"]):
                self.ui.radioButtonDataLogEnable.setChecked(True)
            else:
                self.ui.radioButtonDataLogDisable.setChecked(True)

            self.ui.lineEditLogFileName.setText(self.pref_data["log_file_name"])
            self.ui.lineEditLogFilePath.setText(self.pref_data["log_file_path"])
            
        except:
            print("File not found !")
            pass
        # self.ui.toolButtonBrowseLogFilePath.clicked.connect(self.getPath)
        self.ui.pushButtonExitPref.clicked.connect(self.prefExit)
        self.ui.pushButtonSavePref.clicked.connect(self.prefApply)

        '''  Preference dictonary '''
        self.dict_pref = {
            "mqtt_broker_ip":None,
            "mqtt_broker_port": None,
            "data_log_stat": None,
            "log_file_name": None,
            "log_file_path": None            
        }
    # def getPath(self):
    #     self.init_backup_dir =  FileDialog.getExistingDirectory(None,
    #                                                      'Select initial backup directory.',
    #                                                      '/', QtGui.QFileDialog.ShowDirsOnly)
        # print(self.init_backup_dir)
        print("Pressed get dir !!")

    def prefExit(self):
        self.close()
        pass
    
    def prefApply(self):

        # self.mqtt_broker_ip_text = self.ui.lineEditBrokerIP.text()
        # self.mqtt_broker_port_text = self.ui.lineEditBrokerPort.text()
        # self.log_filename_text = self.ui.lineEditLogFileName.text()        
        # self.log_filepath_text = self.ui.lineEditLogFilePath.text()

        if(self.ui.radioButtonDataLogEnable.isChecked() == True):
            self.log_enable_status = True
        else:
            self.log_enable_status = False
        
        if(self.ui.radioButtonDataLogEnable.isChecked() == False):
            self.log_enable_status = False

        self.dict_pref["mqtt_broker_ip"] = self.ui.lineEditBrokerIP.text()
        self.dict_pref["mqtt_broker_port"] = int(self.ui.lineEditBrokerPort.text())
        self.dict_pref["data_log_stat"] = self.log_enable_status
        self.dict_pref["log_file_name"] = self.ui.lineEditLogFileName.text()
        self.dict_pref["log_file_path"] = self.ui.lineEditLogFilePath.text()

        with open("pref.json", 'w') as pref_json:
            json.dump(self.dict_pref, pref_json)
            pref_json.close()     
        pass

        
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()