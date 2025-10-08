#include <Wire.h>
#include <SPI.h>
#include <SoftwareSerial.h>
#include <BleMouse.h>
#include <HardwareSerial.h>
#include <Arduino.h>
#include <string.h>

#define uS_TO_S_FACTOR 1000000 /* Conversion factor for micro seconds to seconds */ 
#define TIME_TO_SLEEP 3


const int touchPin = 32;
const int t_2 = 33;
const int t_3 = 27;
const int t_4 = 14;
const int micPin = 36; 
const int v_threshold = 500; 

const int threshold = 80; // สำหรับเช็คการสัมผัส
const int threshold2 = 55; //สำหรับเช็คสัมผัสtouch pin ที่ใช้ปลุกจากการ sleep

int touchValue;
int touchV2;
int touchV3;
int touchV4;

bool clapDetected = false;
unsigned long lastClapTime = 0;
unsigned long debounceDelay = 1000; // Debounce time in milliseconds
 
//odroid haedware serial with rxtx2
HardwareSerial mySerial(2);
int txpin = 17;
int rxpin = 16;

uint8_t data[6];
int16_t gyroX, gyroZ;

int Sensitivity = 600;
int delayi = 20;

BleMouse bleMouse;

uint32_t timer;
uint8_t i2cData[14];

const uint8_t IMUAddress = 0x68;
const uint16_t I2C_TIMEOUT = 1000;

// ฟังก์ชันสำหรับการเขียนข้อมูลไปยังอุปกรณ์ที่เชื่อมต่อผ่าน I2C
uint8_t i2cWrite(uint8_t registerAddress, uint8_t* data, uint8_t length, bool sendStop) {
  Wire.beginTransmission(IMUAddress);
  Wire.write(registerAddress);
  Wire.write(data, length);
  return Wire.endTransmission(sendStop); // คืนค่า 0 เมื่อสำเร็จ
}

// ฟังก์ชันสำหรับการเขียนข้อมูลเดี่ยวไปยังอุปกรณ์ที่เชื่อมต่อผ่าน I2C
uint8_t i2cWrite2(uint8_t registerAddress, uint8_t data, bool sendStop) {
  return i2cWrite(registerAddress, &data, 1, sendStop); // คืนค่า 0 เมื่อสำเร็จ
}

// ฟังก์ชันสำหรับการอ่านข้อมูลจากอุปกรณ์ที่เชื่อมต่อผ่าน I2C
uint8_t i2cRead(uint8_t registerAddress, uint8_t* data, uint8_t nbytes) {
  uint32_t timeOutTimer;
  Wire.beginTransmission(IMUAddress);
  Wire.write(registerAddress);
  if(Wire.endTransmission(false))
    return 1;
  Wire.requestFrom(IMUAddress, nbytes,(uint8_t)true);
  for(uint8_t i = 0; i < nbytes; i++) {
    if(Wire.available())
      data[i] = Wire.read();
    else {
      timeOutTimer = micros();
      while(((micros() - timeOutTimer) < I2C_TIMEOUT) && !Wire.available());
      if(Wire.available())
        data[i] = Wire.read();
      else
        return 2;
    }
  }
  return 0;
}
//ฟังก์ชั่นcallbackทำงานเมื่อถูกปลุกโดย touch pin
void callback(){
  ESP.restart(); 
}


void setup() {
  touchSleepWakeUpEnable(T3,threshold2); //เปิดใช้งานการปลุกด้วยการสัมผัสtouchpin  
  pinMode(micPin, INPUT);
  mySerial.begin(115200, SERIAL_8N1, rxpin, txpin);
  Wire.begin();

  // กำหนดค่าเริ่มต้นสำหรับ IMU (Inertial Measurement Unit)
  i2cData[0] = 7;
  i2cData[1] = 0x00;
  i2cData[3] = 0x00;

  while(i2cWrite(0x19, i2cData, 4, false));
  while(i2cWrite2(0x6B, 0x01, true));
  while(i2cRead(0x75, i2cData, 1));
  delay(100);
  while(i2cRead(0x3B,i2cData,6));

  timer = micros();
  Serial.begin(115200);
  bleMouse.begin();
  delay(100);
}


void loop() {
  //รับคอมมานด์จาก odroid ผ่าน uart
  int recieveValue;
  if(mySerial.available()){
    char data[20];
    int i;
    while(mySerial.available()){
      char r = mySerial.read();
      data[i] = r;
      i++;
    }
    sscanf(data, "%d", &recieveValue);
    Serial.println(recieveValue);
}
  while(i2cRead(0x3B,i2cData,14));

  gyroX = ((i2cData[8] << 8) | i2cData[9]);
  gyroZ = ((i2cData[12] << 8) | i2cData[13]);

  gyroX = gyroX / Sensitivity / 1.1  * -1;
  gyroZ = gyroZ / Sensitivity  * -1;

  //อ่านค่าจากความจุไฟฟ้าจากทุก touch pin
  touchValue = touchRead(touchPin);
  touchV2 = touchRead(t_2);
  touchV3 = touchRead(t_3);
  touchV4 = touchRead(t_4);
  //Serial.println(touchValue);
  
  // ส่งข้อมูลการเคลื่อนไหวไปยังอุปกรณ์ที่เชื่อมต่อผ่าน Bluetooth
  if(bleMouse.isConnected()){
    bleMouse.move(gyroZ, -gyroX);
    if(touchValue < threshold){
       bleMouse.click(MOUSE_LEFT);
       delay(250);
    }   
    if (touchV2 < threshold){
       bleMouse.click(MOUSE_RIGHT);
       delay(250);
    }
    if (touchV3 < threshold){
       bleMouse.move(0,0,-1);
       delay(250); 
    }
    if (touchV4 < threshold){
       bleMouse.move(0,0,1);
       delay(250); 
    }
    delay(delayi);
    }

  //อ่านค่าจากเซนเซอร์เสียงหากมีการตรวจจับจะเข้าสู่สภาวะdeep_sleep   
  int micValue = analogRead(micPin);
  if (micValue > v_threshold) {
    if (!clapDetected) {
      if (millis() - lastClapTime > debounceDelay) {
        clapDetected = true;
        lastClapTime = millis();
        Serial.println("Sleep");
        esp_deep_sleep_start();
      }
    }
  } else {
    clapDetected = false;
  }  
}
