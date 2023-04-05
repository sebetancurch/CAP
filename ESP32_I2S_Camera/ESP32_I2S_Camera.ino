#include "OV7670.h"

#include <Adafruit_GFX.h>    // Core graphics library

#include <WiFi.h>
#include <WiFiMulti.h>
#include <WiFiClient.h>
#include "BMP.h"

const int SIOD = 21; //SDA
const int SIOC = 22; //SCL

const int VSYNC = 34;
const int HREF = 35;

const int XCLK = 33;
const int PCLK = 32;

const int D00 = 27;
const int D01 = 17;
const int D02 = 16;
const int D03 = 15;
const int D04 = 14;
const int D05 = 13;
const int D06 = 12;
const int D07 = 4;


const int TFT_DC = 2;
const int TFT_CS = 5;
//DIN <- MOSI 23
//CLK <- SCK 18

#define ssid1        "VILLANUEVA_CORTES_ETB"
#define ssid2        "Familia Ruiz"
#define password1    "Cr1st1an.dav1d"
#define password2    "pipe1127"
//#define ssid2        ""
//#define password2    ""


OV7670 *camera;

WiFiMulti wifiMulti;
WiFiServer server(80);

unsigned char bmpHeader[BMP::headerSize];

void serve()
{
  WiFiClient client = server.available();
  if (client) 
  {
    //Serial.println("New Client.");
    String currentLine = "";
    while (client.connected()) 
    {
      if (client.available()) 
      {
        char c = client.read();
        //Serial.write(c);
        if (c == '\n') 
        {
          if (currentLine.length() == 0) 
          {
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println();
            client.print(
              "<style>body{margin: 0}\nimg{height: 100%; width: auto}</style>"
              "<img id='a' src='/camera' onload='this.style.display=\"initial\"; var b = document.getElementById(\"b\"); b.style.display=\"none\"; b.src=\"camera?\"+Date.now(); '>"
              "<img id='b' style='display: none' src='/camera' onload='this.style.display=\"initial\"; var a = document.getElementById(\"a\"); a.style.display=\"none\"; a.src=\"camera?\"+Date.now(); '>");
            client.println();
            break;
          } 
          else 
          {
            currentLine = "";
          }
        } 
        else if (c != '\r') 
        {
          currentLine += c;
        }
        
        if(currentLine.endsWith("GET /camera"))
        {
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:image/bmp");
            client.println();
            
            client.write(bmpHeader, BMP::headerSize);
            client.write(camera->frame, camera->xres * camera->yres * 2);
        }
      }
    }
    // close the connection:
    client.stop();
    //Serial.println("Client Disconnected.");
  }  
}

void setup() 
{
  pinMode(5, INPUT);
  pinMode(26, OUTPUT);


  
  Serial.begin(115200);

  //wifiMulti.addAP(ssid1, password1);
  wifiMulti.addAP(ssid2, password2);
  Serial.println("Connecting Wifi...");
  if(wifiMulti.run() == WL_CONNECTED) {
      Serial.println("");
      Serial.println("WiFi connected");
      Serial.println("IP address: ");
      Serial.println(WiFi.localIP());
  }
  
  camera = new OV7670(OV7670::Mode::QQQVGA_RGB565, SIOD, SIOC, VSYNC, HREF, XCLK, PCLK, D00, D01, D02, D03, D04, D05, D06, D07);
  
  BMP::construct16BitHeader(bmpHeader, camera->xres, camera->yres);

  server.begin();
  Serial.println("BEGINNED");
  
}

void loop()
{
  
  //Serial.println("uno");
  if(digitalRead(5)==true)
  {
    camera->oneFrame();
  }
  serve();
  //camera->oneFrame();
  //Serial.println("dos");
  //serve();
  //Serial.println("TRES");

}
