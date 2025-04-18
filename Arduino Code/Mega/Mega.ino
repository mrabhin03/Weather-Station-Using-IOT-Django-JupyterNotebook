// DSM501A PM2.5 Dust Sensor Module for Arduino
#define DUST_SENSOR_PIN A6 // Connect the sensor's analog output to analog pin A0

//SOUND,CO/CO2
#include "DFRobot_BMP280.h"
#include "Wire.h"

typedef DFRobot_BMP280_IIC    BMP;   

BMP   bmp(&Wire, BMP::eSdoLow);

#define SEA_LEVEL_PRESSURE    1015.0f   

//PIN deceleration 
const int anemometerPin = A7;  // Connect anemometer signal pin to analog pin A7
//CO,SOUND 
int souPin=A5;
int coPin=A4;
int dhtPin=2;
//NH3,NO2
int NH3Pin = A0;
int NO2Pin = A1;
//LDR , moisture 
int moPin=A2;
int ldrPin=A3;

//values deceleration 
int NH3Value = 0;
int NO2Value = 0;
int ldrPercentage=0;
int ldrvalue=0;
int dustLevel=0;

const float voltageSupply = 5.0;  // Supply voltage to the sensor
const float analogResolution = 1023.0;  // Analog resolution (10-bit ADC)


void printLastOperateStatus(BMP::eStatus_t eStatus)
{
  switch(eStatus) {
  case BMP::eStatusOK:    Serial.println("everything ok"); break;
  case BMP::eStatusErr:   Serial.println("unknow error"); break;
  case BMP::eStatusErrDeviceNotDetected:    Serial.println("device not detected"); break;
  case BMP::eStatusErrParameter:    Serial.println("parameter error"); break;
  default: Serial.println("unknow status"); break;
  }
}


//UV
#include "DFRobot_LTR390UV.h"
DFRobot_LTR390UV ltr390(/*addr = */LTR390UV_DEVICE_ADDR, /*pWire = */&Wire);

//DHT
#include<DHT.h>
DHT dht(dhtPin,DHT11);

void setup()
{ 
  Serial.begin(9600);
  //DHT
  
  dht.begin();

  //UV
  while(ltr390.begin() != 0){
    Serial.println(" Sensor initialize failed!!");
    delay(1000);
  }
  //Serial.println(" Sensor  initialize success!!");
  ltr390.setALSOrUVSMeasRate(ltr390.e18bit,ltr390.e100ms);//18-bit data, sampling time of 100ms 
  ltr390.setALSOrUVSGain(ltr390.eGain3);//Gain of 3
  ltr390.setMode(ltr390.eUVSMode);//Set UV mode 
  
  //CO,SOUND

  bmp.reset();
  //Serial.println("bmp read data test");
  while(bmp.begin() != BMP::eStatusOK) {
    Serial.println("bmp begin faild");
    printLastOperateStatus(bmp.lastOperateStatus);
    delay(2000);
  }
  //Serial.println("bmp begin success");
  delay(100);
}

void loop()
{ Serial.print("*");
  //NH3,NO2
  NH3Value = analogRead(NH3Pin);
  //Serial.print("NH3 :");
  Serial.print(NH3Value);
  Serial.print(",");
  NO2Value = analogRead(NO2Pin);
  //Serial.print("NO2 :");
  Serial.print(NO2Value);
  Serial.print(",");

  //UV
  uint32_t data = 0;
  data = ltr390.readOriginalData();//Get UV raw data
  //Serial.print("UV:");
  Serial.print(data);
  Serial.print(",");

  //DHT
  ldrvalue=analogRead(ldrPin);
  ldrPercentage = map(ldrvalue, 0 ,1023, 100, 0);
  //Serial.print("HUMIDITY :");
  Serial.print(dht.readHumidity());
  Serial.print(",");
  //Serial.print("TEMPERATURE :");
  Serial.print(dht.readTemperature());
  Serial.print(",");
  //Serial.print("LDR :");
  Serial.print(ldrPercentage);
  Serial.print(",");
  //Serial.print("MOISTURE :");
  Serial.print(analogRead(moPin));
  Serial.print(",");
  
  //SOUND,CO
  // float   temp = bmp.getTemperature();
  uint32_t    press = bmp.getPressure();
  float   alti = bmp.calAltitude(SEA_LEVEL_PRESSURE, press);
  int soValue=analogRead(souPin);
  int souPercentage=map(soValue,0,1024,0,100);

  int coValue=analogRead(coPin);
  long coPercentage=(coValue*100L/1024);

  //Serial.print("Sound :");
  Serial.print(souPercentage);
  Serial.print(",");

  //Serial.print("Air Quality :");
  Serial.print(coPercentage);
  Serial.print(",");
  
  // Serial.print("Temperature : "); 
  // Serial.println(temp);

  //Serial.print("Pressure "); 
  Serial.print(press/100);
  Serial.print(",");
  //Serial.print("altitude (unit meter): ");
  Serial.print(alti);
  Serial.print(",");
  dustLevel = readDustSensor();
  //Serial.print("PM2.5 Dust Level: ");
  Serial.print(dustLevel);
  Serial.print(",");
  float voltage = readAnemometerVoltage();  // Read voltage from anemometer
  // float windSpeed = calculateWindSpeed(voltage);  // Convert voltage to wind speed in m/s
  //Serial.print("Wind Speed (m/s): ");
  float windSpeed=5;
  Serial.print(windSpeed);
  Serial.println("#");

  delay(200000);

}

float readAnemometerVoltage() {
  int sensorValue = analogRead(anemometerPin);
  float voltage = (sensorValue / analogResolution) * voltageSupply;
  return voltage;
}

float calculateWindSpeed(float voltage) {
  // You need to calibrate this conversion based on your anemometer's specifications
  // This is just a basic example
  // You may need to adjust these values based on your sensor's characteristics
  float windSpeed = voltage * 2.5;  // For example, assuming linear relationship
  return windSpeed;
}


int readDustSensor() {
  int sensorValue = analogRead(DUST_SENSOR_PIN);
  
  // Map the sensor value to dust level (adjust as per your sensor's specifications)
  // This is a basic example and might need calibration
  int dustLevel = map(sensorValue, 0, 1023, 0, 500); // Assuming a range of 0-500 µg/m³
  
  return dustLevel;
}