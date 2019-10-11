/* 
 * Project : Meat Curing Chamber Controller  
 * Author : Lomas Subedi 
 * Controller : ESP WROOM - 32
 */

/*
 * ------------------------
 * Pin Configuration
 * ------------------------
 * ------------------------
 * OLED and BME280 Connection
 * ------------------------
 * SDA    -> 21
 * SCL    -> 22
 * ------------------------
 * SD Card Connection
 * ------------------------
 * CS     -> 5
 * SCK    -> 18
 * MOSI   -> 23
 * MISO   -> 19
 * ------------------------
 * IO Control
 * ------------------------
 * Freezer        -> 14
 * Humidifier     -> 27
 * Dehumidifier   -> 26
 * Heater         -> 25
 * Internal fan   -> 33
 * Fresh air fan  -> 32
 * Device 7       -> 34
 * Device 8       -> 35
 * Servo 1        -> 12
 * Servo 2        -> 13
 * ------------------------
 */

#include <WiFi.h>
#include <WiFiClient.h>

#include <SPI.h>
#include <Wire.h>
#include <HTTPClient.h>
#include "ArduinoJson.h"

#include "Adafruit_BME280.h"

#include "SD.h"
#include "FS.h"

#include "ESP32_Servo.h"

#define     LCD_EN
#define     WEB_CTRL_EN

#ifdef  LCD_EN
  #include "SSD1306Wire.h"
#endif

#define     BUF_SZ          200
//#define     OLED_RESET      4
#define     ADDRESS         0x3C


// I2C Lines for BME280 and OLED Display
#define     SDA             21
#define     SDC             22

// BME280 Configuration
#define SEALEVELPRESSURE_HPA (1013.25)
//#define BME280_ADD 0x77  /* 0x77 address of the sensor with Kyle*/
#define BME280_ADD 0x76  /* 0x76 address of the sensor with Lomas */

// Time intervals definations
#define     REF_RATE                    2000       // LCD refresh each 2 sec
#define     INTERVAL_LOG                5000       // data logging each 5 sec
#define     INTERVAL_SD_ERROR           5000       // SD card error disp interval

// #define     INTERVAL_FREEZER_LAST_ON    900000UL   // Freezer 15 minutes interval 15 minutes
#define     INTERVAL_FREEZER_LAST_ON    300000UL

// #define     INTERVAL_FRESH_AIR_FAN_ON   900000UL   // Fresh Air Fan ON time interval 15 minutes
#define     INTERVAL_FRESH_AIR_FAN_ON   420000UL

// #define     INTERVAL_FRESH_AIR_FAN_OFF  21600000UL   // Fresh Air Fan OFF time interval 6Hrs
#define     INTERVAL_FRESH_AIR_FAN_OFF  900000UL   // Fresh Air Fan Off time interval 15 minutes


#define     DELAY_SERVO_OFF             10000        // Servo turn off delay after fan turned OFF
#define     OFFSET_TMP                  1.5F
#define     OFFSET_HUM                  2.5F
#define     OFFSET_HUM_2_5              2.50F
#define     OFFSET_HUM_5_0              5.0F


char printBuffer[BUF_SZ];
char timeValBuff[50];
char fileNameBuffer[50];
char fileInputTextBuffer[100];


// WiFi SSID and Passwords definations

//const char* ssid = "Nanook";
//const char* password = "nanook and punter";

//const char* ssid = "yangobahal";
//const char* password = "43A74C699A";

//const char* ssid = "yangobahal";
//const char* password = "8614481234";

const char* ssid = "CAPsMAN";
const char* password = "tarangaK0W";

// Name address for Open TimeZone db API
const char* TimeZoneDBServer = "http://api.timezonedb.com"\
                                "/v2/get-time-zone?key=0979M2P2XE7T&"\
                                "format=json&by=zone&zone=Asia/Kathmandu";

// Global Variables


// Time keeping variables
unsigned long time_last_ref = 0;
unsigned long time_cur_ref = 0;

unsigned  long time_last_log_intrval = 0;
unsigned  long time_cur_log_intrval = 0;

// GPIO Pin defination
const char SD_CS = 5;

const char freezer = 14;
const char humidifier = 27;
const char deHumidifier = 26;
const char heater = 25;
const char internalFan = 33;
const char freshAirFan = 32;
const char device7 = 34;
const char device8 = 35;
bool flagSDProblem = false;

const char servo1Pin = 12;
const char servo2Pin = 13;

// Relay Status flags 
bool freezerRelayStatus = false;
bool humidifierRelayStatus = false;
bool deHumidifierRelayStatus = false;
bool heaterRelayStatus = false;
bool internalFanRelayStatus = false;
bool freshAirFanRelayStatus = false;
bool device7RelayStatus = false;
bool device8RelayStatus = false;

// Flag flow chart
bool flagCoolingMode = true;
bool flagHeatingMode = false;
bool flagFreshAirFanOnInstance = false;

// Loop control misc flags
bool flagColModeLopEntry = false;
bool flagFresAirFanEntry = false;
bool flagFresAirFanOffEntry = false;

// Time records 
uint64_t freezerLastOnTime = 0;
uint64_t freshAirFanOnTime = 0;
uint64_t freshAirFanOffTime = 0;

// vars and flags for servo 
bool flagServCnt = false;
uint16_t servAngle = 0;
uint64_t timeNowServOp = 0;
uint64_t timePrevServOp = 0;

// Temperature and humidity variables
float h = 0.0;
float t = 0.0;
float f = 0.0;
volatile float setHum = 0.0;
volatile float setTmp = 0.0;

// Variable to store the HTTP request
String httpReq;       // buffered HTTP request stored as null terminated string
char reqIndex = 0;    // index into HTTP_req buffer

// Global object creation
// Set web server port number to 80
WiFiServer server(80);

// Web page file stored on the SD card
File webFile; 

// BME280 Object
Adafruit_BME280 bme(SDA, SCL);

// HTTP Client for extracting time from TimeZoneDB API
HTTPClient http;

// Servo object instantiation
Servo servo1;
Servo servo2;

// Oled Object
#ifdef     LCD_EN
  SSD1306Wire display(ADDRESS, SDA, SDC);
#endif

// Freezer Control
void freezerTurnOn(void) {
   digitalWrite(freezer, LOW);
   freezerRelayStatus = true;
}

void freezerTurnOff(void) {
  digitalWrite(freezer, HIGH);
  freezerRelayStatus = false;
  freezerLastOnTime = millis();
}

// Humidifier control
void humidifierTurnOn(void) {
   digitalWrite(humidifier, LOW);
   humidifierRelayStatus = true;
}

void humidifierTurnOff(void) {
   digitalWrite(humidifier, HIGH);
   humidifierRelayStatus = false;
}

// De Humidifier control
void deHumidifierTurnOn(void) {
   digitalWrite(deHumidifier, LOW);
   deHumidifierRelayStatus = true;
}

void deHumidifierTurnOff(void) {
   digitalWrite(deHumidifier, HIGH);
   deHumidifierRelayStatus = false;
}

// Heater control
void heaterTurnOn(void) {
   digitalWrite(heater, LOW);
   heaterRelayStatus = true;
}

void heaterTurnOff(void) {
   digitalWrite(heater, HIGH);
   heaterRelayStatus = false;
}

// Internal Fan control
void internalFanTurnOn(void) {
   digitalWrite(internalFan, LOW);
   internalFanRelayStatus = true;
}

void internalFanTurnOff(void) {
   digitalWrite(internalFan, HIGH);
   internalFanRelayStatus = false;
}

// Fresh air Fan control
void freshAirFanTurnOn(void) {
   digitalWrite(freshAirFan, LOW);
   freshAirFanRelayStatus = true;
   freshAirFanOnTime = millis();
}

void freshAirFanTurnOff(void) {
   digitalWrite(freshAirFan, HIGH);
   freshAirFanRelayStatus = false;
   freshAirFanOffTime = millis();
}

// Device 7 control
void device7TurnOn(void) {
   digitalWrite(device7, LOW);
   device7RelayStatus = true;
}

void device7TurnOff(void) {
   digitalWrite(device7, HIGH);
   device7RelayStatus = false;
}

// Device 8 control

void device8TurnOn(void) {
   digitalWrite(device8, LOW);
   device8RelayStatus = true;
}

void device8TurnOff(void) {
   digitalWrite(device8, HIGH);
   device8RelayStatus = false;
}

void servoInit(void) {
  servo1.attach(servo1Pin);
  servo2.attach(servo2Pin);  
}

void openServos(void) {
  servo1.write(30);
  servo2.write(30);
}

void closeServos(void) {
  servo1.write(0);
  servo2.write(0);
}

#ifdef LCD_EN
void oledInit(void) {
  
  display.init();  
  display.displayOn();
  display.clear();
  display.invertDisplay();
  display.flipScreenVertically();
  display.setContrast(90, 100, 64);
  
}

void oledPrintScreen(const char * str) {
  display.clear();
  display.setFont(ArialMT_Plain_16);
  display.drawString(2, 30, str);
  display.display();

}

void refrestDisp(IPAddress servIP, float tempF, float hum) {

  display.clear();
  
  display.setFont(ArialMT_Plain_10);
  display.drawString(0, 0, "  !!! Meat Locker V 2.0 !!!");
  display.display();

  display.drawHorizontalLine(0, 15, 128);
  display.display();

  // Display the IP on the LCD
  display.setFont(ArialMT_Plain_16);
  display.drawString(2, 19, servIP.toString());
  display.display();

  display.drawHorizontalLine(0, 38, 128);
  display.display();

  // Display temperature humidyty data
  String tmpHum = String("T:");
  tmpHum += String(tempF, 2);
  tmpHum += String(" | H:");
  tmpHum += String(hum, 2);

  display.setFont(ArialMT_Plain_16);
  display.drawString(4, 40, tmpHum);
  display.display();  
}

#endif

void logToFile(fs::FS &fs, const char * path, const char * message){
  Serial.printf("Writing file: %s\n", path);

  if(fs.exists(path)) {
    File file = fs.open(path, FILE_APPEND);

    if(!file){
      Serial.println("Failed to open file for appending the data ");
      return;
    }

    if(file.println(message)){
      Serial.println("Successfully appended the new data !!!");
    } else {
      Serial.println("failed appending the data !!!");
    }
    
  } else {    // If file not exists, create it
    File file = fs.open(path, FILE_WRITE);
    
    if(!file){
      Serial.println("Failed to open file for writing");
      return;
    }
    
    if(file.println("Date, Time, Temperature (C), Humidity(%)")){
      Serial.println("Written the header !!");
    } else {
      Serial.println("Write failed");
    }
  }
}

void setup() {

  Serial.begin(115200);

  #ifdef LCD_EN
  oledInit();
    
  // ----------------------------------------------------
  // Display welcome message
  // ----------------------------------------------------

  display.clear();
  display.setFont(ArialMT_Plain_16);
  display.drawString(5, 10, "*** WELCOME ***");
  display.display();
  delay(1000);

  display.drawString(0, 40, "Meat Locker V 2.0");
  
  display.display();
  delay(5000);

  // ----------------------------------------------------
  #endif

  pinMode(SD_CS, OUTPUT);
  
  // Setup SD card
  if(!SD.begin(SD_CS)){

    Serial.println("Card Mount Failed");
    #ifdef LCD_EN
    oledPrintScreen("Card Mount Failed");
    #endif    

    flagSDProblem = true;

  } else {

    Serial.println("SD card successfully mounted !!!");
    #ifdef LCD_EN
    oledPrintScreen("SD mounted !!!");   
    #endif 

    flagSDProblem = false;
    delay(1000);
  }

  uint8_t cardType = SD.cardType();

  if(cardType == CARD_NONE) {

    flagSDProblem = true;
    
    Serial.println("No SD card attached!");
    #ifdef LCD_EN
    oledPrintScreen("No SD card attached!");   
    #endif

  } else {
    flagSDProblem = false;
  }

  Serial.print("Connecting to : ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  Serial.println("");

  // ----------------------------------------------------
  // Wait for connection
  // ----------------------------------------------------
  #ifdef LCD_EN
  display.clear();
  display.setFont(ArialMT_Plain_16);
  display.drawString(0, 10, "Connecting to:");
  display.display();
  display.drawString(0, 40, ssid);
  display.display();
  delay(1000);
  #endif
  // ----------------------------------------------------
  
  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  server.begin();

  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");  
  Serial.println(WiFi.localIP());

  // ----------------------------------------------------
  // Display SSID connection information
  #ifdef LCD_EN
  display.clear();
  display.setFont(ArialMT_Plain_16);
  display.drawString(0, 10, "Connected to :");
  display.drawString(0, 40, ssid);
  display.display();
  delay(5000);
  #endif
  // ----------------------------------------------------

  // ----------------------------------------------------
  // Initialize the sensor 
  bool status;
  status = bme.begin(BME280_ADD);
  
  if (!status) {
    Serial.println("Could not find a valid BME280 sensor, check wiring!");
    display.clear();
    display.setFont(ArialMT_Plain_16);
    display.drawString(0, 10, "No Sensor");
    display.drawString(0, 40, "Check Wiring");
    display.display();
    delay(5000);
  }
  
  // Initialize GPIOS
  pinMode(freezer, OUTPUT);
  digitalWrite(freezer, HIGH);

  pinMode(humidifier, OUTPUT);
  digitalWrite(humidifier, HIGH);

  pinMode(deHumidifier, OUTPUT);
  digitalWrite(deHumidifier, HIGH);

  pinMode(heater, OUTPUT);
  digitalWrite(heater, HIGH);

  pinMode(internalFan, OUTPUT);
  digitalWrite(internalFan, HIGH);

  pinMode(freshAirFan, OUTPUT);
  digitalWrite(freshAirFan, HIGH);

  pinMode(device7, OUTPUT);
  digitalWrite(device7, HIGH);

  pinMode(device8, OUTPUT);
  digitalWrite(device8, HIGH);

  servoInit();

  // Fresh air fan turning ON initially
  openServos();
  freshAirFanTurnOn(); 

}

WiFiClient client;
void loop() {

   client = server.available();   // Listen for incoming clients

    time_cur_ref = millis();
    
    if( (time_cur_ref - time_last_ref) >= REF_RATE) {
    time_last_ref = time_cur_ref;

    // Reading temperature or humidity takes about 250 milliseconds!
    // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
    h = bme.readHumidity();
    // Read temperature as Celsius (the default)
    t = bme.readTemperature();
    // Read temperature as Fahrenheit (isFahrenheit = true)
    f = (1.8) * t + 32;

    // Check if any reads failed and exit early (to try again).
    if (isnan(h) || isnan(t) || isnan(f)) {
      Serial.println("Failed to read from BME 280 sensor!");
      // Display SSID connection information
      #ifdef LCD_EN
        display.clear();
        display.setFont(ArialMT_Plain_24);
        display.drawString(10, 5, "*** No ***");
        display.display();
        display.drawString(0, 30, "!! Sensor !!");
        display.display();
        delay(1000);
      #endif
      // ----------------------------------------------------
    } else {

      sprintf(printBuffer, "Humidity -> %f%\tTemperature ->%f*C\t%f*f\r\n", h, t, f);
      Serial.print(printBuffer);

      #ifdef LCD_EN
        refrestDisp(WiFi.localIP(), f, h);
      #endif
    }    
  }

  // In case SD is not correctly connected
  if(flagSDProblem) {
    /* TODO:
     * Send SD ERROR Message to UI     
    */

    if((millis() % INTERVAL_SD_ERROR) == 0) {
      Serial.println("Error, No SD card detected. Please check the wiring and restart the system !!!");

      /* TODO:
       * Send SD ERROR Message to UI     
      */
    }    
  }
  
  time_cur_log_intrval = millis();
  if((time_cur_log_intrval -  time_last_log_intrval) >= INTERVAL_LOG) {
    time_last_log_intrval = time_cur_log_intrval;
    // configure traged server and url
    http.begin(TimeZoneDBServer);

    Serial.println("Connecting to timezonedb [time server]...");
    // start connection and send HTTP header
    int httpCode = http.GET();

    // httpCode will be negative on error
    if(httpCode > 0) {
        // file found at server
        if(httpCode == HTTP_CODE_OK) {
            
            // Collect Payload
            String payload = http.getString();
            
            // Payload is JSON, thus parse the JSON
            int bufferSize = payload.length() + 1;                         
            DynamicJsonBuffer jsonBuffer(bufferSize);
            JsonObject& root = jsonBuffer.parseObject(payload);

            if (!root.success()) {
              Serial.println("JSON parsing failed!");
              return;
            }

            strcpy(timeValBuff, root["formatted"]);    

            Serial.print("Date and Time : ");
            Serial.println(timeValBuff);         
        }
    } else {
        Serial.printf("Could not connect to api.timezonedb.com. Please check the connection,"\
                        "error: %s\n", http.errorToString(httpCode).c_str());
    }
    http.end();

    // End HTTP connection
    // Now log the collected data

  String dateTimeStr = String(timeValBuff);
  String dateStr = dateTimeStr.substring(0, 10);
  Serial.print("Date String : ");
  Serial.println(dateStr);
  
  String timeStr = dateTimeStr.substring(10);
  Serial.print("Time String : ");
  Serial.println(timeStr);
  
  String logFilePath = "/" + dateStr + ".csv";
  
  logFilePath.toCharArray(fileNameBuffer, (logFilePath.length() + 1));
  
  String dataString = dateStr + "," +  timeStr + "," + String(t) + "," + String(h);  

  dataString.toCharArray(fileInputTextBuffer, (dataString.length() + 1));

  // These will be the headers for your excel file, CHANGE "" 
  // to whatevr headers you would like to use
  logToFile(SD, (const char *)fileNameBuffer, (const char *)fileInputTextBuffer);

//  sprintf("Humidity Set Point: %f, Temperature Set Point : %f", setHum, setTmp);
//  Serial.println(printBuffer);

 }
  
  // if (client) {  // if new client connects
  //   boolean currentLineIsBlank = true;
  //   reqIndex = 0;
  //   while (client.connected()) {      
  //     if (client.available()) {   // client data available to read
  //       char c = client.read(); // read 1 byte (character) from client
  //       httpReq += c;

  //       // if the current line is blank, you got two newline characters in a row.
  //       // that's the end of the client HTTP request, so send a response:
  //       if (c == '\n' && currentLineIsBlank) {

  //         // send a standard http response header
  //         client.println("HTTP/1.1 200 OK");          

  //         // Send XML file or Web page
  //         // If client already on the web page, browser requests with AJAX the latest
  //         // sensor readings (ESP32 sends the XML file)
  //         if (httpReq.indexOf("updateData") >= 0) {
  //           // send rest of HTTP header
  //           client.println("Content-Type: text/xml");
  //           client.println("Connection: keep-alive");
  //           client.println();

  //           int indxStart = httpReq.indexOf("/updateData&");
  //           int indxEnd = httpReq.indexOf(" HTTP");

  //           String updateString = httpReq.substring(indxStart + 1, indxEnd);
            
  //           if (updateString.indexOf("setHum=") >= 0) {

  //             int indxHumStart = updateString.indexOf("setHum=");
  //             indxHumStart += sizeof("setHum=");

  //             String humStr = updateString.substring(indxHumStart, indxHumStart + 5);           
  //             setHum = humStr.toFloat();

  //             Serial.print("Humidity Set Value : ");
  //             Serial.println(setHum);
  //           }

  //           if (updateString.indexOf("setTmp=") >= 0) {

  //             int indxTmpStart = updateString.indexOf("setTmp=");
  //             indxTmpStart += sizeof("setTmp=");
  //             String tmpStr = updateString.substring(indxTmpStart, indxTmpStart + 5);            
  //             setTmp = tmpStr.toFloat();

  //             Serial.print("Temperature  Set Value : ");
  //             Serial.println(setTmp);
  //           }            
                                    
  //           Serial.println(updateString);                        
  //           // Send XML file with sensor readings
  //           sendXMLFile(client, t, f, h);
  //         }

  //         // When the client connects for the first time, send it the index.html file
  //         // stored in the microSD card
  //         else {  
  //           // send rest of HTTP header
  //           client.println("Content-Type: text/html");
  //           client.println("Connection: keep-alive");
  //           client.println();

  //           // send web page stored in microSD card
  //           webFile = SD.open("/dashboard.html");
  //           if (webFile) {
  //             while(webFile.available()) {
  //               // send web page to client
  //               client.write(webFile.read()); 
  //             }
  //             webFile.close();
  //           }
  //         }
  //         break;
  //       }
  //       // every line of text received from the client ends with \r\n
  //       if (c == '\n') {
  //         // last character on line of received text
  //         // starting new line with next character read
  //         currentLineIsBlank = true;
  //       } 
  //       else if (c != '\r') {
  //         // a text character was received from client
  //         currentLineIsBlank = false;
  //       }
  //     } // end if (client.available())
  //   } // end while (client.connected())
  //   // Clear the header variable
  //   httpReq = "";
  //   // Close the connection
  //   client.stop();
  //   Serial.println("Client disconnected.");    
  // } // end if (client)  
  
  ESP.getFreeHeap();

  // ---------------- Main Control loop  ----------------
  // -------- Cooling/Heating Loop ----------------------
  
  if(flagCoolingMode) {   // Cooling mode    
    // is Tmp  > 1.5DC + STP
    if( t > (setTmp + OFFSET_TMP)) { 
      // Check if the freezer was on before 15 minutes
      if(((millis() - freezerLastOnTime) > INTERVAL_FREEZER_LAST_ON) || (!flagColModeLopEntry)) {
        flagColModeLopEntry = true;
        freezerTurnOn(); 
      }
    } else if(t <= (setTmp - OFFSET_TMP)) {
      freezerTurnOff();
    } else {
      // Do nothing
    }
  } else {     // Heating Mode
    // is Tmp  > 1.5DC + STP
    if( t > (setTmp + OFFSET_TMP)) {
      heaterTurnOff();
    } else if(t <= (setTmp - OFFSET_TMP)) {    
      heaterTurnOn();
    } else {
      // Do nothing
    }
  }
  // -------- End of Cooling/Heating Loop --------------------

  
  // -------- Humidity Loop ----------------------
  // is Hum  > 2.5% + HSP
  if(h > (setHum + OFFSET_HUM_2_5)) {

    // is Hum  > 5.0% + HSP
    if(h > (setHum + OFFSET_HUM_5_0)) {

      humidifierTurnOff();
      deHumidifierTurnOn();
    }

    // is Hum  < HSP - 2.5%
  } else if(h <= (setHum - OFFSET_HUM_2_5)) {

    // is Hum  < HSP - 5.0%
    if(h <= (setHum - OFFSET_HUM_5_0)) {

      humidifierTurnOn();
      deHumidifierTurnOff();
    }   
        
  } else {
    deHumidifierTurnOff();
    humidifierTurnOff();
  }
  
  // -------- End of Humidity Loop ----------------------


  // -------- Fresh Air Fan Loop ----------------------
    // Is Fresh air fan ON for more than 15mins ?
    if(((millis() - freshAirFanOnTime) > INTERVAL_FRESH_AIR_FAN_ON)) {
      flagFresAirFanEntry = true;

      freshAirFanTurnOff();
      delay(DELAY_SERVO_OFF);
      closeServos();        
    }

    // Is Fresh air fan OFF for more than 6Hrs ?
  //  if(((millis() - freshAirFanOffTime) > INTERVAL_FRESH_AIR_FAN_OFF)) {
    //  flagFresAirFanOffEntry = true;
     // openServos();
     // freshAirFanTurnOn();        
 //   }
  // -------- End of Fresh Air Fan Loop ----------------------

  // -------- Internal Fan control Loop ----------------------
  if(freezerRelayStatus || humidifierRelayStatus ||
      deHumidifierRelayStatus || heaterRelayStatus ||
      freshAirFanRelayStatus || device7RelayStatus || device8RelayStatus
      ) {
    internalFanTurnOn();
  } else {
    internalFanTurnOff();
  }
  // -------- End of Internal Fan control Loop ---------------------- 
}
