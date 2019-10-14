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
#include <PubSubClient.h>
#include <SPI.h>
#include <Wire.h>

#include "ArduinoJson.h"

#include "Adafruit_BME280.h"

#include "ESP32_Servo.h"

#include<string.h>

#define     LCD_EN
#define     WEB_CTRL_EN
// #define     SD_EN



#ifdef SD_EN
#include "SD.h"
#include "FS.h"
#endif


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

//const char* ssid = "CAPsMAN";
//const char* password = "tarangaK0W";

//const char* ssid = "HONGSHI";
//const char* password = "digicom123";

//const char* ssid = "yangobahal";
//const char* password = "8614481234";

const char* ssid = "LSD";
const char* password = "N3pal@12345";

//MQTT Broker address
const char* mqtt_server = "192.168.1.15";

// Global Variables
// MQTT Topic constants
const char * topicSetPoint = "mcuring/setPoint";
const char * topicStatus = "mcuring/status";
const char * topicTime = "mcuring/time";

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

typedef struct date_time {
  unsigned int year;
  unsigned char month;
  unsigned char day;
  unsigned char hour;
  unsigned char min;
  unsigned char sec;
} dt_t;

dt_t dateTimeStamp;

// Global object creation

// Wifi and MQTT Publish Subscribe Object
WiFiClient espClient;
PubSubClient client(espClient);

// BME280 Object
Adafruit_BME280 bme(SDA, SCL);

//// HTTP Client for extracting time from TimeZoneDB API
//HTTPClient http;

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

void refrestDisp(IPAddress servIP, float tmp, float hum) {

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
  tmpHum += String(tmp, 2);
  tmpHum += String(" | H:");
  tmpHum += String(hum, 2);

  display.setFont(ArialMT_Plain_16);
  display.drawString(4, 40, tmpHum);
  display.display();  
}
#endif

// MQTT Call back routine
void callback(char* topic, byte* payload, unsigned int length) {
  /* MQTT message print */
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i=0;i<length;i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  if(!strcmp(topic, topicSetPoint)) {

  StaticJsonDocument<256> doc;
  DeserializationError error = deserializeJson(doc, payload, length); 
    // Test if parsing succeeds.
  if (error) {
    Serial.print(F("deserializeJson() failed: "));
    Serial.println(error.c_str());
    return;
  }

  setTmp = doc["tmpSetPoint"];
  setHum = doc["humSetPoint"];

  // Print values.
  Serial.print("Temperature Setpoint ");  
  Serial.println(setTmp, 3);
  Serial.print("Humidity Setpoint ");
  Serial.println(setHum, 3);
  }

  if(!strcmp(topic, topicTime)) {
    StaticJsonDocument<256> doc;
    DeserializationError error = deserializeJson(doc, payload, length); 
      // Test if parsing succeeds.
    if (error) {
      Serial.print(F("deserializeJson() failed: "));
      Serial.println(error.c_str());
      return;
    }

    dateTimeStamp.year = doc["Year"];
    dateTimeStamp.month = doc["Month"];
    dateTimeStamp.day = doc["Day"];
    dateTimeStamp.hour = doc["Hour"];
    dateTimeStamp.min = doc["Minute"];
    dateTimeStamp.sec = doc["Second"];

//    sprintf(printBuffer, "Date and Time : %d/%d/%d %d:%d:%d", \
//    dateTimeStamp.year, dateTimeStamp.month, dateTimeStamp.day, dateTimeStamp.hour, dateTimeStamp.min, dateTimeStamp.sec);
//    Serial.println(printBuffer);
  }  
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP32Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected to broker");
      // Once connected, publish an announcement...
//      client.publish("outTopic", "hello world");
//      // ... and resubscribe
      client.subscribe("mcuring/setPoint");
      client.subscribe("mcuring/time");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
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

#ifdef SD_EN
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
#endif

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


  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
    
  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

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

  // start MQTT operation 
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

}

void loop() {

  if (!client.connected()) {
    reconnect();
  }  
  
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

      StaticJsonDocument<256> doc;
      char statusValue[256];

      doc["curTemp"] = t;
      doc["curHum"] = h;
      doc["Frez"] = freezerRelayStatus;
      doc["Hum"] = humidifierRelayStatus;
      doc["Dhum"] = deHumidifierRelayStatus;
      doc["Htr"] = heaterRelayStatus;
      doc["IFan"] = internalFanRelayStatus;
      doc["FFan"] = freshAirFanRelayStatus;
      doc["Dev7"] = device7RelayStatus;
      doc["Dev8"] = device8RelayStatus;

      size_t n = serializeJson(doc, statusValue);
      Serial.println(statusValue);
      client.publish(topicStatus, statusValue);

      #ifdef LCD_EN
        refrestDisp(WiFi.localIP(), t, h);
      #endif
    }    
  }

  #ifdef SD_EN
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

  #endif
  
  #if 0 // Skip data logging for a while
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
 }
 #endif
  
  ESP.getFreeHeap();

  #if 1
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
  #endif

  client.loop();
}
