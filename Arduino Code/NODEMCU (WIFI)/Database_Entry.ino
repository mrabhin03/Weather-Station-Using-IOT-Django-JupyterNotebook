#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

#define HOST "localhost"
#define WIFI_SSID "Only For You"
#define WIFI_PASSWORD "**********"
String IPV4="***.***.**.***";
char data;
int sensors[12],array_length=0;
String myString = "";
String Lost_data[50],insert_query;
int flag = 0;

String IP_value;
int checkWiFiConnection() 
{
  if (WiFi.status() != WL_CONNECTED)
  {
    Serial.println("Connection Not Found..");
    return false;
  }

  Serial.println("Connected to Wi-Fi");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
  IP_value = WiFi.localIP().toString();
  return true;
}

void setup() 
{
  Serial.begin(9600);
  Serial.println("Communication Started\n");
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  checkWiFiConnection();
}

void loop()
{
  if (Serial.available() > 0) {
    while (Serial.available() > 0) {
      data = Serial.read();
      if (data == '*') {
        flag = 1;
      } else if (data == '#') {
        flag = 0;
        int startIndex = 0;
        int commaIndex;
        for (int i = 0; i < 13; i++) {
          commaIndex = myString.indexOf(',', startIndex);
          if (commaIndex != -1) {
            sensors[i] = myString.substring(startIndex, commaIndex).toDouble();
            startIndex = commaIndex + 1;
          } else {
            sensors[i] = myString.substring(startIndex).toDouble();
            break;
          }
        }
        for (int i = 0; i < 13; i++) {
          Serial.print("Sensor");
          Serial.print(i + 1);
          Serial.print(": ");
          Serial.print(sensors[i]);
          if (i < 11) {
            Serial.print(", ");
          }
        }
        Serial.println();

        myString = "";
      } else {
        myString += data;
      }
    }
    String nh3 = String(sensors[0]);
    String no2 = String(sensors[1]);
    String uv = String(sensors[2]);
    String hum = String(sensors[3]);
    String temp = String(sensors[4]);
    String ldp = String(sensors[5]);
    String moi = String(sensors[6]);
    String sou = String(sensors[7]);
    String carbon = String(sensors[8]);
    String press = String(sensors[9]);
    String atti = String(sensors[10]);
    String pm25 = String(sensors[11]);
    String windspeed = String(sensors[12]);
    insert_query="nh3=" + nh3 + "&no2="+no2 + "&uv="+uv+ "&hum="+hum+ "&temp="+temp+ "&ldp="+ldp+ "&moi="+moi+ "&sou="+sou+ "&carbon="+carbon+ "&press="+press+ "&atti="+atti+ "&pm25="+pm25+ "&windspeed="+windspeed;
    Lost_data[array_length]=insert_query;
    array_length++;
    if(checkWiFiConnection()){
      for(int i=0;i<array_length;i++){
        WiFiClient client;
        HTTPClient http;
        String url = "http://192.168.43.230:8000/datainsert/?"+Lost_data[i];
        Serial.print("Sending data: ");
        Serial.println(url);

        http.begin(client, url);

        int httpCode = http.GET();

        if (httpCode == HTTP_CODE_OK) 
        {
          String response = http.getString();
          Serial.println("Server response: " + response);
        } 
        else
        {
          Serial.print("HTTP GET request failed with error code: ");
          Serial.println(httpCode);
          if (httpCode == HTTPC_ERROR_CONNECTION_REFUSED)
          {
            Serial.println("Connection refused by the server.");
          }
          else if (httpCode == HTTP_CODE_NOT_FOUND) 
          {
            Serial.println("Server resource not found.");
          }
          else {
            Serial.println("Unknown error occurred.");
          }
        }
        http.end();
      }
      array_length=0;
    }
    else{
      //Array Store
    }
  }
}