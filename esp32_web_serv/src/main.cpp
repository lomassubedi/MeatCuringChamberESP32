/* 
 * Project : Meat Curing Chamber Controller  
 * Author : Lomas Subedi 
 * Controller : ESP WROOM - 32
 */

#include <WiFiClient.h>
#include <ESP32WebServer.h>
#include <WiFi.h>
#include <ESPmDNS.h>

#include "FS.h"
#include "SD.h"
#include "SPI.h"


const char* ssid = "internets";
const char* password = "CLFA4ABD38";

ESP32WebServer server ( 80 );

const int led = 13;

/* this array contains the web will be responded to client
it uses jquery for making GET request and processing slider UI control */
char res[2048]=
"<!DOCTYPE html>\
<html>\
<head>\
<title>Chamber Control</title>\
</head>\
<style> \
  header, footer {\
    padding: 1em;\
    color: white;\
    background-color: green;\
    clear: left;\
    text-align: center;\
  }\
  nav {   \
    float: left;\
    border-right: thik soli #ff0000;\
    max-width: 160px;\
    margin: 20px;\
    padding: 1em;\
  }\
  .controlTmpHum, .readTempHum {\
    float: center\
      padding: 1em;\
      overflow: hidden;   \
  }   \
</style>\
<body>\
  <header><h1> Meat Curing Chamber Dashboard </h1></header>\
  <div class='enableDisableDevice'>\
    <nav>\
      <form id='checkDev'>Device Control<br>\
        <input type='checkbox' name='freezer' value='0'>Freezer<br>\
        <input type='checkbox' name='humidifier' value='0'>Humidifier<br>\
        <input type='checkbox' name='deHumidifier' value='0'>Dehumidifier<br>\
        <input type='checkbox' name='heater' value='0'>Heater<br>\
        <input type='checkbox' name='internalFan' value='0'>Internal Fan<br>\
        <input type='checkbox' name='freshAirFan' value='0'>Fresh air fan<br>\
        <input type='checkbox' name='dev7' value='0'>Device 7<br>\
        <input type='checkbox' name='dev8' value='0'>Device 8<br>\
      </form>\
    </nav>\
  </div>\
  <div class='controlTmpHum'>\
    <br>\
    <form'>\
      Set Humidity: <input type='text' name='setHumidity'>\
      <br>\
      <br>\
      Set Temperature: <input type='text' name='setTemperature'>\
      <br>\
      <br>\
      <input type='submit' value='Save'>\
    </form>\
  </div>\
  <div class='readHum'>\
    <br>\
      Current Humidity: \
      <script type='text/javascript'>\
      document.write('100')\
      </script> % </p> \
  </div>\
  <div class='readTemp'>\
    <p>Current Temperature: \
    <script type='text/javascript'>\
      document.write('23')\
      </script> &degF</p> \
  </div>\
  <footer>\
    <p>\
      Copyright &copy <i>Keyl Schaub, 2018</i>\
    </p>\
  </footer>\
</body>\
</html>";

void handleRoot() {
  server.send(200, "text/html", res);
}

void handleNotFound(){
  String message = "File Not Found\n\n";
  server.send(404, "text/plain", message);
}

void listDir(fs::FS &fs, const char * dirname, uint8_t levels){
    Serial.printf("Listing directory: %s\n", dirname);

    File root = fs.open(dirname);
    if(!root){
        Serial.println("Failed to open directory");
        return;
    }
    if(!root.isDirectory()){
        Serial.println("Not a directory");
        return;
    }

    File file = root.openNextFile();
    while(file){
        if(file.isDirectory()){
            Serial.print("  DIR : ");
            Serial.println(file.name());
            if(levels){
                listDir(fs, file.name(), levels -1);
            }
        } else {
            Serial.print("  FILE: ");
            Serial.print(file.name());
            Serial.print("  SIZE: ");
            Serial.println(file.size());
        }
        file = root.openNextFile();
    }
}

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.println("");
  
  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  // Setup SD card

  if(!SD.begin()){
      Serial.println("Card Mount Failed");
      return;
  }

  uint8_t cardType = SD.cardType();

  if(cardType == CARD_NONE){
      Serial.println("No SD card attached");
      return;
  }

  listDir(SD, "/", 0);

  if (MDNS.begin("esp32")) {
  Serial.println("MDNS responder started");
  }
  
  server.on("/", handleRoot);
  
  server.onNotFound(handleNotFound);
  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
}
