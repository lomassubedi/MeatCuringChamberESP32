
from PyQt5 import QtCore
from PyQt5 import QtWidgets, QtGui

import paho.mqtt.client as mqtt

import json
from meat_curing_mw import Ui_MeatCuringChamberMW
import sys
import datetime

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

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.ui = Ui_MeatCuringChamberMW()
        self.setFixedSize(733, 386)
        self.ui.setupUi(self)

        self.ui.lcdNumberCurTmp.setStyleSheet("color: red")
        self.ui.lcdNumberCurHum.setStyleSheet("color: red")

        self.ui.lcdNumberSetTmpVal.setStyleSheet("color: green")
        self.ui.lcdNumberSetHumVal.setStyleSheet("color: green")

        # Class wise global variabels
        self.broker_ip = None
        self.broker_port = None

        # self.client = mqtt.Client("UI")
        # self.client.on_message = self.on_message

        self.storage_file_name = 'dat.json'

        self.flag_connected = False

        self.client = MqttClient(self)
        # self.client.stateChanged.connect(self.on_stateChanged)
        self.client.messageSignal.connect(self.on_messageSignal)

        self.redColor = QtGui.QColor(255, 0, 0)
        self.blackColor = QtGui.QColor(0, 0, 0)
        self.greenColor = QtGui.QColor(0, 128, 0)

        # initialize with last data
        try:
            with open(self.storage_file_name, 'rb') as config_data:
                self.config_val = json.load(config_data)
                config_data.close()
            
            self.ui.lineEditBrokerIP.setText(self.config_val["broker_ip"])
            self.ui.lineEditBrokerPort.setText(str(self.config_val["broker_port"]))
            self.ui.lcdNumberSetTmpVal.setProperty("value", self.config_val["lastTmpSetPoint"])
            self.ui.lcdNumberSetHumVal.setProperty("value", self.config_val["lastHumSetPoint"])
        except:
            print("Could not find the file !")
            pass

        ''' Signals '''
        self.ui.actionQuit.triggered.connect(self.exitApp)
        self.ui.pushButtonConnectBroker.clicked.connect(self.connectBroker)
        self.ui.pushButtonSetSetpointApply.clicked.connect(self.applySettings)
        self.ui.pushButtonExit.clicked.connect(self.exitApp)

    def connectBroker(self):

        if self.flag_connected == False:
            self.broker_ip = self.ui.lineEditBrokerIP.text()
            self.broker_port = self.ui.lineEditBrokerPort.text()

            print("IP of the broker to be connected : " + str(self.broker_ip))
            print("PORT of the broker to be connected : " + self.broker_port)

            try:
                self.client.hostname = self.broker_ip
                self.client.connectToHost()

                self.client.subscribe("mcuring/test")
                # self.client.subscribe("mcuring/espReply/#", 0)
                print("Connected to the broker!")
                self.event_log(self.greenColor, "Connected to MQTT Broker")
                self.ui.pushButtonConnectBroker.setText("Disconnect")
                self.ui.lineEditBrokerIP.setDisabled(True)
                self.ui.lineEditBrokerPort.setDisabled(True)
                self.flag_connected = True
                pass
            except TimeoutError:
                print("Timeout Error: Could not connect to the broker! Please check IP and Port and connect again!")
                pass
        else:
            try:
                # self.client.disconnect()
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
        self.ui.lcdNumberSetTmpVal.setProperty("value", self.valTempSetPoint)
        self.ui.lcdNumberSetHumVal.setProperty("value", self.valHumSetPoint)
        self.event_log(self.blackColor, str("New Setpoint, T: " + str(self.valTempSetPoint) + " H: " + str(self.valHumSetPoint)))

        self.dict_setpoint = {
            "tmpSetPoint": self.valTempSetPoint,
            "humSetPoint":self.valHumSetPoint
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

        if(self.broker_ip):
            self.client.publish("ui/setpoint", json_set_point)
        else:
            print("Error connecting to the broker !")

    def exitApp(self):
        dict_data = {
            "broker_ip":self.ui.lineEditBrokerIP.text(),
            "broker_port":int(self.ui.lineEditBrokerPort.text()),
            "lastTmpSetPoint":self.ui.lcdNumberSetTmpVal.intValue(),
            "lastHumSetPoint":self.ui.lcdNumberSetHumVal.intValue()
        }
        dict_data_json_dump = json.dumps(dict_data)
        with open(self.storage_file_name, 'wb') as last_val:
            last_val.write(dict_data_json_dump.encode())
            last_val.close()
        sys.exit()

    def event_log(self, color, log_string):
        self.ui.textBrowserDeviceStatus.setTextColor(color)
        self.ui.textBrowserDeviceStatus.append("[" + str(datetime.datetime.now().strftime('%H:%M:%S')) + "]" + log_string)
        pass

    # @QtCore.pyqtSlot(int)
    # def on_stateChanged(self, state):
    #     if state == MqttClient.Connected:            
    #         # self.client.subscribe("mcurint/test")

    @QtCore.pyqtSlot(str)
    def on_messageSignal(self, msg):
        print("Mqtt message : " + msg)
        
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()