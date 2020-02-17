
from PyQt5 import QtWidgets, QtGui, QtCore
# from PyQt5 import QtWidgets, QtGui

import paho.mqtt.client as mqtt
import json
from meat_curing_mw import Ui_MeatCuringChamberMW
from about import Ui_About
from data_logger_UI import Ui_DataLoggerSetting
import sys
import datetime
import time
import csv

#global CSV header defination 
fieldNames = ['Time Stamp', 'Temperature(degC)', 'Humidity(%)', 
'Operation Mode', 'Freezer', 'Humidifier', 'Dehumidifier', 'Heater', 
'Internal Fan', 'Freshair Fan', 'Device 7', 'Device 8']
log_fileName = None

class MqttClient(QtCore.QObject):
    Disconnected = 0
    Connecting = 1
    Connected = 2

    MQTT_3_1 = mqtt.MQTTv31
    MQTT_3_1_1 = mqtt.MQTTv311

    connected = QtCore.pyqtSignal()
    disconnected = QtCore.pyqtSignal()

    stateChanged = QtCore.pyqtSignal(int)
    hostnameChanged = QtCore.pyqtSignal(str)
    portChanged = QtCore.pyqtSignal(int)
    keepAliveChanged = QtCore.pyqtSignal(int)
    cleanSessionChanged = QtCore.pyqtSignal(bool)
    protocolVersionChanged = QtCore.pyqtSignal(int)

    messageSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(MqttClient, self).__init__(parent)

        self.m_hostname = ""
        self.m_port = 1883
        self.m_keepAlive = 60
        self.m_cleanSession = True
        self.m_protocolVersion = MqttClient.MQTT_3_1

        self.m_state = MqttClient.Disconnected

        self.m_client =  mqtt.Client(clean_session=self.m_cleanSession,
            protocol=self.protocolVersion)

        self.m_client.on_connect = self.on_connect
        self.m_client.on_message = self.on_message
        self.m_client.on_disconnect = self.on_disconnect


    @QtCore.pyqtProperty(int, notify=stateChanged)
    def state(self):
        return self.m_state

    @state.setter
    def state(self, state):
        if self.m_state == state: return
        self.m_state = state
        self.stateChanged.emit(state) 

    @QtCore.pyqtProperty(str, notify=hostnameChanged)
    def hostname(self):
        return self.m_hostname

    @hostname.setter
    def hostname(self, hostname):
        if self.m_hostname == hostname: return
        self.m_hostname = hostname
        self.hostnameChanged.emit(hostname)

    @QtCore.pyqtProperty(int, notify=portChanged)
    def port(self):
        return self.m_port

    @port.setter
    def port(self, port):
        if self.m_port == port: return
        self.m_port = port
        self.portChanged.emit(port)

    @QtCore.pyqtProperty(int, notify=keepAliveChanged)
    def keepAlive(self):
        return self.m_keepAlive

    @keepAlive.setter
    def keepAlive(self, keepAlive):
        if self.m_keepAlive == keepAlive: return
        self.m_keepAlive = keepAlive
        self.keepAliveChanged.emit(keepAlive)

    @QtCore.pyqtProperty(bool, notify=cleanSessionChanged)
    def cleanSession(self):
        return self.m_cleanSession

    @cleanSession.setter
    def cleanSession(self, cleanSession):
        if self.m_cleanSession == cleanSession: return
        self.m_cleanSession = cleanSession
        self.cleanSessionChanged.emit(cleanSession)

    @QtCore.pyqtProperty(int, notify=protocolVersionChanged)
    def protocolVersion(self):
        return self.m_protocolVersion

    @protocolVersion.setter
    def protocolVersion(self, protocolVersion):
        if self.m_protocolVersion == protocolVersion: return
        if protocolVersion in (MqttClient.MQTT_3_1, MQTT_3_1_1):
            self.m_protocolVersion = protocolVersion
            self.protocolVersionChanged.emit(protocolVersion)

    #################################################################
    @QtCore.pyqtSlot()
    def connectToHost(self):
        if self.m_hostname:
            self.m_client.connect(self.m_hostname, 
                port=self.port, 
                keepalive=self.keepAlive)

            self.state = MqttClient.Connecting
            self.m_client.loop_start()

    @QtCore.pyqtSlot()
    def disconnectFromHost(self):
        self.m_client.disconnect()

    def subscribe(self, path):
        if self.state == MqttClient.Connected:
            self.m_client.subscribe(path)

    #################################################################
    # callbacks
    def on_message(self, mqttc, obj, msg):
        mstr = msg.payload.decode("ascii")
        # print("on_message", mstr, obj, mqttc)
        self.messageSignal.emit(mstr)

    def on_connect(self, *args):
        # print("on_connect", args)
        self.state = MqttClient.Connected
        self.connected.emit()

    def on_disconnect(self, *args):
        # print("on_disconnect", args)
        self.state = MqttClient.Disconnected
        self.disconnected.emit()
    
    def publish(self, topc, pylod):
        self.m_client.publish(topic=topc, payload=pylod, qos=0)

class Main(QtWidgets.QMainWindow):
    
    signal_start_background_job = QtCore.pyqtSignal()

    def __init__(self):
        super(Main, self).__init__()
        self.ui = Ui_MeatCuringChamberMW()
        self.setFixedSize(780, 386)
        self.ui.setupUi(self)

        # Class wise global variabels
        self.broker_ip = None
        self.broker_port = None

        # Thread stuffs
        # self.worker = WorkerObject()
        # self.thread = QtCore.QThread()
        # self.worker.moveToThread(self.thread)
        # self.signal_start_background_job.connect(self.worker.background_job)    

        self.ui.lcdNumberCurTmp.setStyleSheet("color: red")
        self.ui.lcdNumberCurHum.setStyleSheet("color: red")

        self.ui.lcdNumberSetTmpVal.setStyleSheet("color: green")
        self.ui.lcdNumberSetHumVal.setStyleSheet("color: green")

        self.ui.checkBoxFreezer.setDisabled(True)
        self.ui.checkBoxHumidifier.setDisabled(True)
        self.ui.checkBoxDehumidifier.setDisabled(True)
        self.ui.checkBoxHeater.setDisabled(True)
        self.ui.checkBoxInternalFan.setDisabled(True)
        self.ui.checkBoxFreshAirFan.setDisabled(True)
        self.ui.checkBoxDevice7.setDisabled(True)
        self.ui.checkBoxDevice8.setDisabled(True)
        self.ui.groupBoxDeviceControl.setDisabled(True)
        
        # About signal 
        self.ui.actionAbout.triggered.connect(self.on_about)
        self.ui.actionData_Logging.triggered.connect(self.on_dataLogger)

        self.storage_file_name = 'dat.json'
        self.log_file_path_main = None
        self.flag_connected = False

        self.client = MqttClient(self)
        # self.client.stateChanged.connect(self.on_stateChanged)
        self.client.connected.connect(self.on_connection)
        self.client.messageSignal.connect(self.on_messageSignal)

        self.redColor = QtGui.QColor(255, 0, 0)
        self.blackColor = QtGui.QColor(0, 0, 0)
        self.greenColor = QtGui.QColor(0, 128, 0)

        # initialize UI with last saved data
        # try:
        with open(self.storage_file_name, 'rb') as config_data:
            self.config_val = json.load(config_data)
            config_data.close()
            print("Data Saved on File : " + str(self.config_val))
        
        self.ui.lineEditBrokerIP.setText(self.config_val["broker_ip"])
        self.ui.lineEditBrokerPort.setText(str(self.config_val["broker_port"]))
        self.ui.lcdNumberSetTmpVal.setProperty("value", self.config_val["lastTmpSetPoint"])
        self.ui.lcdNumberSetHumVal.setProperty("value", self.config_val["lastHumSetPoint"])
        if(self.config_val["lastOpnHtnMde"]):                
            self.ui.radioButtonHeatingMode.setChecked(True)
            if(self.ui.radioButtonCoolingMode.isChecked()):
                self.ui.radioButtonCoolingMode.toggle()
        else:
            self.ui.radioButtonCoolingMode.setChecked(True)
            if(self.ui.radioButtonHeatingMode.isChecked()):
                self.ui.radioButtonHeatingMode.toggle()
        
        self.log_file_path_main = self.config_val["log_path"]
        # except:
        #     print("Could not find the file !")
        #     pass

        ''' Signals '''
        self.ui.actionQuit.triggered.connect(self.exitApp)
        self.ui.pushButtonConnectBroker.clicked.connect(self.connectBroker)
        self.ui.pushButtonSetSetpointApply.clicked.connect(self.applySettings)
        self.ui.pushButtonExit.clicked.connect(self.exitApp)        
        self.ui.radioButtonHeatingMode.toggled.connect(self.changeMode)
        

    def connectBroker(self):

        if self.flag_connected == False:
            self.broker_ip = self.ui.lineEditBrokerIP.text()
            self.broker_port = self.ui.lineEditBrokerPort.text()

            print("IP of the broker to be connected : " + str(self.broker_ip))
            print("PORT of the broker to be connected : " + self.broker_port)

            try:
                self.client.hostname = self.broker_ip
                self.client.connectToHost()
                self.event_log(self.greenColor, "Connected to MQTT Broker")
                self.ui.pushButtonConnectBroker.setText("Disconnect")
                self.ui.lineEditBrokerIP.setDisabled(True)
                self.ui.lineEditBrokerPort.setDisabled(True)
                self.flag_connected = True

                # trigger thread
                # self.thread.start()
                # self.signal_start_background_job.emit()           

                pass
            except TimeoutError:
                print("Timeout Error: Could not connect to the broker! Please check IP and Port and connect again!")
                pass
        else:
            try:
                self.client.disconnectFromHost()
                print("Disconnected from the broker!")
                self.event_log(self.redColor, "Disonnected from MQTT Broker")
                self.ui.lineEditBrokerIP.setDisabled(False)
                self.ui.lineEditBrokerPort.setDisabled(False)
                self.ui.pushButtonConnectBroker.setText("Connect")               
                self.flag_connected = False
            except:
                print("Problem disconnecting")

    def applySettings(self):        
        self.valTempSetPoint = self.ui.doubleSpinBoxSetSetPointTmp.value()
        self.valHumSetPoint = self.ui.doubleSpinBoxSetSetPointHum.value()
        if(self.ui.radioButtonHeatingMode.isChecked()):
            self.valOpnModeHeating = True
        else:
            self.valOpnModeHeating = False
            pass           
         
        self.ui.lcdNumberSetTmpVal.setProperty("value", self.valTempSetPoint)
        self.ui.lcdNumberSetHumVal.setProperty("value", self.valHumSetPoint)
        self.event_log(self.blackColor, str("New Setpoint, T: " + str(self.valTempSetPoint) + " H: " + str(self.valHumSetPoint)))

        self.dict_setpoint = {
            "tmpSetPoint": self.valTempSetPoint,
            "humSetPoint":self.valHumSetPoint,
            "opnHtnMde":self.valOpnModeHeating
        }

        json_set_point = json.dumps(self.dict_setpoint)

        self.client.publish("mcuring/setPoint",json_set_point)

        try:
            with open(self.storage_file_name, "rb") as pref_val:
                self.pref_data = json.load(pref_val)            
            pref_val.close()
            
        except:
            print("Preference file not found !")
            pass

    def exitApp(self):

        if(self.ui.radioButtonHeatingMode.isChecked()):
            self.valOpnModeHeating = True
        else:
            self.valOpnModeHeating = False
            pass            

        with open(self.storage_file_name, 'rb') as last_val_tmp:
            last_val_tmp_json = json.load(last_val_tmp)
            last_val_tmp.close()

        dict_data = {
            "broker_ip":self.ui.lineEditBrokerIP.text(),
            "broker_port":int(self.ui.lineEditBrokerPort.text()),
            "lastTmpSetPoint":self.ui.lcdNumberSetTmpVal.intValue(),
            "lastHumSetPoint":self.ui.lcdNumberSetHumVal.intValue(),
            "lastOpnHtnMde":self.valOpnModeHeating,
            "log_path":last_val_tmp_json["log_path"]
        }
        dict_data_json_dump = json.dumps(dict_data)
        print("Data On exit : " + dict_data_json_dump)
        with open(self.storage_file_name, 'wb') as last_val:
            last_val.write(dict_data_json_dump.encode())
            last_val.close()
        sys.exit()

    def changeMode(self):           
            if(self.ui.radioButtonHeatingMode.isChecked()):
                self.event_log(self.blackColor, "Heating mode selected!")

            if(self.ui.radioButtonCoolingMode.isChecked()):
                self.event_log(self.blackColor, "Cooling mode selected!")

    def event_log(self, color, log_string):
        self.ui.textBrowserDeviceStatus.setTextColor(color)
        self.ui.textBrowserDeviceStatus.append("[" + str(datetime.datetime.now().strftime('%H:%M:%S')) + "]" + log_string)
        pass
    
    def on_about(self):
        tool_about = About()
        tool_about.show()
        tool_about.exec_()
        pass
    def on_dataLogger(self):
        tool_dataLogger = DataLogger()
        tool_dataLogger.show()
        tool_dataLogger.exec_()

    @QtCore.pyqtSlot(str)
    def on_messageSignal(self, msg):
        
        sensorStat = json.loads(msg)
        print(sensorStat)

        #log data :        
        with open(self.storage_file_name, 'rb') as config_data:
            self.config_val = json.load(config_data)
            config_data.close()
            print(self.config_val)
        
        with open(self.config_val["log_path"], 'a') as logFile:
            writer = csv.DictWriter(logFile, fieldnames=fieldNames)
            writer.writerow({'Time Stamp':str(datetime.datetime.now().strftime('%D-%H:%M:%S')), 
            'Temperature(degC)':sensorStat["curTemp"], 
            'Humidity(%)':sensorStat["curHum"], 
            'Operation Mode':None,
            'Freezer':sensorStat["Frez"],
            'Humidifier':sensorStat["Hum"],
            'Dehumidifier':sensorStat["Dhum"],
            'Heater':sensorStat["Htr"], 
            'Internal Fan':sensorStat["IFan"],
            'Freshair Fan':sensorStat["FFan"],
            'Device 7':sensorStat["Dev7"],
            'Device 8':sensorStat["Dev8"]
            })
            logFile.close()

        self.ui.lcdNumberCurTmp.display(sensorStat["curTemp"])
        self.ui.lcdNumberCurHum.display(sensorStat["curHum"])    

        if(sensorStat["Frez"]):            
            self.ui.labellabelFreezerStatusValue.setText("ON")
        else:
            self.ui.labellabelFreezerStatusValue.setText("OFF")

        if(sensorStat["Hum"]):
            self.ui.labelHumidifierStatusValue.setText("ON")
        else:
            self.ui.labelHumidifierStatusValue.setText("OFF")
        
        if(sensorStat["Dhum"]):
            self.ui.labelDehumidifierStatusValue.setText("ON")
        else:
            self.ui.labelDehumidifierStatusValue.setText("OFF")
                    
        if(sensorStat["Htr"]):
            self.ui.labelHeaterSatusValue.setText("ON")
        else:
            self.ui.labelHeaterSatusValue.setText("OFF")
        
        if(sensorStat["IFan"]):
            self.ui.labelInternalFanStatusValue.setText("ON")
        else:
            self.ui.labelInternalFanStatusValue.setText("OFF")
        
        if(sensorStat["FFan"]):
            self.ui.labelFreshAirFanStatusValue.setText("ON")
        else:
            self.ui.labelFreshAirFanStatusValue.setText("OFF")

        if(sensorStat["Dev7"]):
            self.ui.labelDevice7StatusValue.setText("ON")
        else:
            self.ui.labelDevice7StatusValue.setText("OFF")
        
        if(sensorStat["Dev8"]):
            self.ui.labelDevice8StatusValue.setText("ON")
        else:
            self.ui.labelDevice8StatusValue.setText("OFF")

    @QtCore.pyqtSlot()
    def on_connection(self):
        print("Connected to the broker!")
        self.client.subscribe("mcuring/status")
        pass
'''
class WorkerObject(QtCore.QObject):
    @QtCore.pyqtSlot()
    def background_job(self):

        time_stamp = {
            "Year":None,
            "Month":None,
            "Day":None,
            "Hour":None,
            "Minute":None,
            "Second":None            
        }
        
        # another_client = MqttClient(self)
        # another_client.hostname = "192.168.43.1"
        # another_client.hostname = "192.168.100.233"
        # another_client.hostname = "192.168.1.15"
        # another_client.hostname = a
        # another_client.connectToHost()

        while True:
            date_and_time = datetime.datetime.now()
            time_stamp["Year"] = date_and_time.year
            time_stamp["Month"] = date_and_time.month
            time_stamp["Day"] = date_and_time.day
            time_stamp["Hour"] = date_and_time.hour
            time_stamp["Minute"] = date_and_time.minute
            time_stamp["Second"] = date_and_time.second
            
            # print(time_stamp)

            json_timeStamp = json.dumps(time_stamp)
            Main().client.publish("mcuring/time", json_timeStamp)
            print(a)
            # TODO access client object from Main class and publish message
            time.sleep(1)
'''

class About(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.dialog_about = Ui_About()
        self.dialog_about.setupUi(self)
        self.setFixedSize(252, 166)

class DataLogger(QtWidgets.QDialog): #, QtWidgets.QFileDialog
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.dtlUI = Ui_DataLoggerSetting()
        self.dtlUI.setupUi(self)

        self.dtlUI.pushButtonBrowse.clicked.connect(self.file_dilg)
        self.dtlUI.pushButtonApply.clicked.connect(self.apply_dilg)
        self.dtlUI.pushButtonExit.clicked.connect(self.exit_window)

        self.data_file_name = 'dat.json'
        self.log_file = None
        self.log_filename = None

        # initialize Dialogue with last saved data
        try:
            with open(self.data_file_name, 'rb') as config_path:
                self.config_val = json.load(config_path)
                config_path.close()            
                # print("Data Saved on File : " + self.config_val)
                self.dtlUI.lineEditBrowsePath.setText(self.config_val["log_path"])
        except:
            print("Could not find the file !")
            pass
    
    def file_dilg(self):
        self.log_filename = QtWidgets.QFileDialog.getSaveFileName(self, "Select log file ","", '*.csv')
        self.config_val["log_path"] = str(self.log_filename[0])
        self.dtlUI.lineEditBrowsePath.setText(self.config_val["log_path"])

    def apply_dilg(self):

        self.config_val["log_path"] = self.dtlUI.lineEditBrowsePath.text()
        #creat the file
        with open(self.config_val["log_path"], 'w+') as logFile:
            writer = csv.DictWriter(logFile, fieldnames=fieldNames)
            writer.writeheader()
            logFile.close()

        print(self.config_val)
        with open(self.data_file_name, 'wb') as configFile:
            config_file_updated = json.dumps(self.config_val)
            configFile.write(config_file_updated.encode())
            configFile.close()                
        pass        

    def exit_window(self):
        self.close()
        pass        

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()