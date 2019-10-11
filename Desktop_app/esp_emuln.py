import json
import paho.mqtt.client as mqtt

client = mqtt.Client("ESP Emuln")

host = "192.168.1.102"

client.connect(host, port=1883)

dict_reply = {
  "freezer": False,
  "hunidifier": False,
  "dehumidifier": False,
  "heater": False,
  "internalfan": False,
  "freshairfan": False,
  "device7": False,
  "device8": False,
  "curTemp": 45.32,
  "curHum": 68.02
}

json_set_point = json.dumps(dict_reply)

client.publish("mcuring/espReply", json_set_point)
