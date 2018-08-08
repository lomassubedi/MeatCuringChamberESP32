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
 * OLED Display Connectiion
 * ------------------------
 * SDA    -> 21
 * SCL    -> 22
 * ------------------------
 * BME 280 Connection
 * ------------------------
 * SDA    -> 2
 * SCL    -> 4
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
 * Device 7       -> 12
 * Device 8       -> 13
 * ------------------------
 */

#include <WiFi.h>
#include <WiFiClient.h>

#include <SPI.h>
#include <Wire.h>

#include "Adafruit_BME280.h"

#include "SD.h"

#define     LCD_EN

#ifdef  LCD_EN
  #include "SSD1306Wire.h"
#endif

#define     BUF_SZ          512
//#define     OLED_RESET      4
#define     ADDRESS         0x3C

#define     SDA             21
#define     SDC             22

// BME280 Configuration
//#define I2C_SDA             21
//#define I2C_SCL             22
#define SEALEVELPRESSURE_HPA (1013.25)
#define BME280_ADD 0x76

#define     REF_RATE        2000    // LCD refresh each 2 sec

char printBuffer[BUF_SZ];
char lcdBuffr[50];

uint64_t millisTick = 0;

//const char* ssid = "internets";
//const char* password = "CLFA4ABD38";

//const char* ssid = "yangobahal";
//const char* password = "43A74C699A";

const char* ssid = "Bee";
const char* password = "p@ssw0rd";

/*
const char* ssid = "Nanook";
const char* password = "nanook and punter";
*/

// GPIO Pin defination
const char freezer = 14;
const char humidifier = 27;
const char deHumidifier = 26;
const char heater = 25;
const char internalFan = 33;
const char freshAirFan = 32;
const char device7 = 12;
const char device8 = 13;

// Pin Status flags
bool freezerStatus = false;
bool humidifierStatus = false;
bool deHumidifierStatus = false;
bool heaterStatus = false;
bool internalFanStatus = false;
bool freshAirFanStatus = false;
bool device7Status = false;
bool device8Status = false;

// Temperature and humidity variables
float h = 0.0;
float t = 0.0;
float f = 0.0;

// Set web server port number to 80
WiFiServer server(80);

// Web page file stored on the SD card
File webFile; 

// Variable to store the HTTP request
String httpReq;       // buffered HTTP request stored as null terminated string
char reqIndex = 0;              // index into HTTP_req buffer

// BME280 Object
Adafruit_BME280 bme(SDA, SCL);

// Oled Object
#ifdef     LCD_EN
  SSD1306Wire display(ADDRESS, SDA, SDC);
#endif

void setNewControls() {

  if (httpReq.indexOf("freezer=1") >= 0) {
    freezerStatus = true;
    digitalWrite(freezer, LOW);
  } else if(httpReq.indexOf("freezer=0") >= 0) {
    freezerStatus = false;
    digitalWrite(freezer, HIGH);
  }

  if (httpReq.indexOf("humidifier=1") >= 0) {
    humidifierStatus = true;
    digitalWrite(humidifier, LOW);
  } else if(httpReq.indexOf("humidifier=0") >= 0) {
    humidifierStatus = false;
    digitalWrite(humidifier, HIGH);
  }  

  if (httpReq.indexOf("deHumidifier=1") >= 0) {
    deHumidifierStatus = true;
    digitalWrite(deHumidifier, LOW);
  } else if(httpReq.indexOf("deHumidifier=0") >= 0) {
    deHumidifierStatus = false;
    digitalWrite(deHumidifier, HIGH);
  }    

  if (httpReq.indexOf("heater=1") >= 0) {
    heaterStatus = true;
    digitalWrite(heater, LOW);
  } else if(httpReq.indexOf("heater=0") >= 0) {
    heaterStatus = false;
    digitalWrite(heater, HIGH);
  }    

  if (httpReq.indexOf("internalFan=1") >= 0) {
    internalFanStatus = true;
    digitalWrite(internalFan, LOW);
  } else if(httpReq.indexOf("internalFan=0") >= 0) {
    internalFanStatus = false;
    digitalWrite(internalFan, HIGH);
  }     

  if (httpReq.indexOf("freshAirFan=1") >= 0) {
    freshAirFanStatus = true;
    digitalWrite(freshAirFan, LOW);
  } else if(httpReq.indexOf("freshAirFan=0") >= 0) {
    freshAirFanStatus = false;
    digitalWrite(freshAirFan, HIGH);
  }     

  if (httpReq.indexOf("dev7=1") >= 0) {
    device7Status = true;
    digitalWrite(device7, LOW);
  } else if(httpReq.indexOf("dev7=0") >= 0) {
    device7Status = false;
    digitalWrite(device7, HIGH);
  } 

  if (httpReq.indexOf("dev8=1") >= 0) {
    device8Status = true;
    digitalWrite(device8, LOW);
  } else if(httpReq.indexOf("dev8=0") >= 0) {
    device8Status = false;
    digitalWrite(device8, HIGH);
  }   

  //   if (httpReq.indexOf("setHumidity") >= 0) {
  //   device8Status = true;
  //   digitalWrite(device8, HIGH);
  // } else if(httpReq.indexOf("dev8=0") >= 0) {
  //   device8Status = false;
  //   digitalWrite(device8, LOW);
  // }   

}
// Send XML file with sensor readings
void sendXMLFile(WiFiClient cl, float tempC, float tempF, float hum) {

  cl.print("<?xml version = \"1.0\" ?>");
  cl.print("<inout>");    

  // Updat temperature Celcius 
  cl.print("<tempC>");
  cl.print(tempC);  
  cl.print("</tempC>");

  // Update temperature deg F 
  cl.print("<tempF>");
  cl.print(tempF);
  cl.print("</tempF>");

  // update RH
  cl.print("<hum>");
  cl.print(hum);
  cl.print("</hum>");

  sprintf(printBuffer, "Humidity -> %f\tTemperature ->%f*C\t%f*f\r\n", hum, tempC, tempF);
  Serial.print(printBuffer);

  // Check Box Device status
  // For freezer
  cl.print("<freezer>");
  if (freezerStatus) {
    cl.print("checked");
  } else {
    cl.print("unchecked");
  }
  cl.println("</freezer>");

  // Humidifier
  cl.print("<humidifier>");
  if (humidifierStatus) {
    cl.print("checked");
  } else {
    cl.print("unchecked");
  }
  cl.println("</humidifier>");

  // De Humidifier
  cl.print("<deHumidifier>");
  if (deHumidifierStatus) {
    cl.print("checked");
  } else {
    cl.print("unchecked");
  }
  cl.println("</deHumidifier>");

  // Heater
  cl.print("<heater>");
  if (heaterStatus) {
    cl.print("checked");
  } else {
    cl.print("unchecked");
  }
  cl.println("</heater>");  

  // Internal Fan
  cl.print("<internalFan>");
  if (internalFanStatus) {
    cl.print("checked");
  } else {
    cl.print("unchecked");
  }
  cl.println("</internalFan>");    

  // Fresh Air Fan
  cl.print("<freshAirFan>");
  if (freshAirFanStatus) {
    cl.print("checked");
  } else {
    cl.print("unchecked");
  }
  cl.println("</freshAirFan>");     

  // Device 7
  cl.print("<dev7>");
  if (device7Status) {
    cl.print("checked");
  } else {
    cl.print("unchecked");
  }
  cl.println("</dev7>");   

  // Device 8
  cl.print("<dev8>");
  if (device8Status) {
    cl.print("checked");
  } else {
    cl.print("unchecked");
  }
  cl.println("</dev8>");   

  cl.print("</inout>");

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
  // Setup SD card
  if(!SD.begin()){
    Serial.println("Card Mount Failed");
    #ifdef LCD_EN
    oledPrintScreen("Card Mount Failed");
    #endif
//    return;
  } else {
    Serial.println("SD card successfully mounted !!!");
    #ifdef LCD_EN
    oledPrintScreen("SD mounted !!!");   
    #endif 
    delay(1000);
  }

  uint8_t cardType = SD.cardType();

  if(cardType == CARD_NONE){
      Serial.println("No SD card attached!");
      #ifdef LCD_EN
      oledPrintScreen("No SD card attached!");   
      #endif
//      return;
  }
//  WiFi.disconnect(true);
//  delay(4000);
  // WiFi.
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
  digitalWrite(freezer, LOW);

  pinMode(humidifier, OUTPUT);
  digitalWrite(humidifier, LOW);

  pinMode(deHumidifier, OUTPUT);
  digitalWrite(deHumidifier, LOW);

  pinMode(heater, OUTPUT);
  digitalWrite(heater, LOW);

  pinMode(internalFan, OUTPUT);
  digitalWrite(internalFan, LOW);

  pinMode(freshAirFan, OUTPUT);
  digitalWrite(freshAirFan, LOW);

  pinMode(device7, OUTPUT);
  digitalWrite(device7, LOW);

  pinMode(device8, OUTPUT);
  digitalWrite(device8, LOW);

}

void loop() {

   WiFiClient client = server.available();   // Listen for incoming clients

    if(!(millis() % REF_RATE)) {

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
      Serial.print(F("Temperature : "));
      Serial.print(t);
      Serial.print("C ");
      Serial.print(f);
      Serial.print("F. ");
      Serial.print(F("Humidity : "));
      Serial.print(h);
      Serial.println("%.");
      #ifdef LCD_EN
      refrestDisp(WiFi.localIP(), f, h);
      #endif
    }    
  }

  if (client) {  // if new client connects
    boolean currentLineIsBlank = true;
    reqIndex = 0;
    while (client.connected()) {      
      if (client.available()) {   // client data available to read
        char c = client.read(); // read 1 byte (character) from client
        httpReq += c;

        // if the current line is blank, you got two newline characters in a row.
        // that's the end of the client HTTP request, so send a response:
        if (c == '\n' && currentLineIsBlank) {

          // send a standard http response header
          client.println("HTTP/1.1 200 OK");

          Serial.println(httpReq);

          // Send XML file or Web page
          // If client already on the web page, browser requests with AJAX the latest
          // sensor readings (ESP32 sends the XML file)
          if (httpReq.indexOf("updateData") >= 0) {
            // send rest of HTTP header
            client.println("Content-Type: text/xml");
            client.println("Connection: keep-alive");
            client.println();

            int indxStart = httpReq.indexOf("/updateData&");
            int indxEnd = httpReq.indexOf(" HTTP");

            String updateString = httpReq.substring(indxStart + 1, indxEnd);
            
            if (updateString.indexOf("setHum=") >= 0) {

              int indxHumStart = updateString.indexOf("setHum=");
              indxHumStart += sizeof("setHum=");

              String humStr = updateString.substring(indxHumStart, indxHumStart + 3);
              Serial.print("Index value : ");
              Serial.println(indxHumStart);
              Serial.print("This is the received string: ");
              Serial.println(humStr);              
              int indxHumEnd = humStr.toInt();

              // String _humStr = humStr.substring(indxHumEnd);

              Serial.print("Humidity Value : ");
              Serial.println(indxHumEnd);
            }
                                    
            Serial.println(updateString);            
            
            setNewControls();
            // Send XML file with sensor readings
            sendXMLFile(client, t, f, h);
          }

          // When the client connects for the first time, send it the index.html file
          // stored in the microSD card
          else {  
            // send rest of HTTP header
            client.println("Content-Type: text/html");
            client.println("Connection: keep-alive");
            client.println();

            // send web page stored in microSD card
            webFile = SD.open("/dashboard.html");
            if (webFile) {
              while(webFile.available()) {
                // send web page to client
                client.write(webFile.read()); 
              }
              webFile.close();
            }
          }
          break;
        }
        // every line of text received from the client ends with \r\n
        if (c == '\n') {
          // last character on line of received text
          // starting new line with next character read
          currentLineIsBlank = true;
        } 
        else if (c != '\r') {
          // a text character was received from client
          currentLineIsBlank = false;
        }
      } // end if (client.available())
      // Serial.println(header);
    } // end while (client.connected())
    // Clear the header variable
    httpReq = "";
    // Close the connection
    client.stop();
    Serial.println("Client disconnected.");    
  } // end if (client)  
}   
