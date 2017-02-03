
#include <ESP8266WiFi.h>
#include <WiFiClient.h> 
#include <WiFiUdp.h>


IPAddress myipa( 10,0,0,1 );

//Wifi Settings
static char *ssid = "STONEFIELD";
static char *pass = "miyasaka";

//UDPSettings
static WiFiUDP UDP;
static const char *ripa = "10.0.0.100";
static const int port = 4000;
char buff[256];

void conwifi(){
  int x = 0;
  //Connect to Wifi
  WiFi.begin( ssid, pass );
  WiFi.config( IPAddress(10,0,0,1), IPAddress(10,0,0,100), IPAddress(255,255,255,0) );
  while( WiFi.status() != WL_CONNECTED ){
    digitalWrite( 2, x );
    x=(x==0?1:0);
    delay( 1000 );
  }
  digitalWrite( 2, 1 );
} 

void setup() {
  
  pinMode( 15, OUTPUT );
  pinMode( 2, OUTPUT );
  digitalWrite( 15, 1 );
  digitalWrite( 2, 1 );

  pinMode( 5, INPUT );
  
  conwifi();

  //for debug
//  Serial.begin(115200);
//  delay(100);
  UDP.begin( 4000 );

}

void status(){
      digitalWrite(5,0);
      delay(100);
      digitalWrite(5,1);
}

void loop() {
  if( WiFi.status() == WL_CONNECTED ){
    UDP.beginPacket( ripa, 4000 );
    UDP.write( "{\"MAC\":\"5c:cf:7f:89:f3:b0\",\"Value\":\"" );
    UDP.write( digitalRead(5)?"True":"False" );
    UDP.write( "\"}" );
    UDP.endPacket();
    delay( 1000 );
  }else{
    WiFi.disconnect();
    conwifi();
  }
}
