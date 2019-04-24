/*
  UrineAnalyser.ino - Application which sensor urine color using Xkit for Arduino board
  Version 1.0
  Created by Soham Dinesh Patel
  April 18, 2019.

  Last update on April 18, 2019

  Note: DemoCode for Xkit Shield has been used as a base for this implementation.
*/

#include <WISOL.h>
#include <Tsensors.h>
#include <Wire.h>
#include <math.h>
#include <SimpleTimer.h>
#include <avr/wdt.h>

#define S0 22
#define S1 24
#define S2 26
#define S3 28
#define sensorOut 30

#define SAMPLING_RATE 40 // Times of collection

int redValues[SAMPLING_RATE];
int greenValues[SAMPLING_RATE];
int blueValues[SAMPLING_RATE];

Isigfox *Isigfox = new WISOL();
Tsensors *tSensors = new Tsensors();
SimpleTimer timer;
int watchdogCounter;
uint8_t buttonCounter;
uint8_t PublicModeSF;
uint8_t stateLED;
uint8_t ledCounter;
const uint8_t buttonPin = A1;
const int redLED = 6;
int redFrequency = 0;
int greenFrequency = 0;
int blueFrequency = 0;
int reqCounter = 0;

typedef union{
    float number;
    uint8_t bytes[4];
} FLOATUNION_t;

typedef union{
    uint16_t number;
    uint8_t bytes[2];
} UINT16_t;

typedef union{
    int16_t number;
    uint8_t bytes[2];
} INT16_t;

void setup() {
  int flagInit;
  
  Wire.begin();
  Wire.setClock(100000);

  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);
  pinMode(sensorOut, INPUT);
  
  // Setting frequency-scaling to 20%
  digitalWrite(S0,HIGH);
  digitalWrite(S1,HIGH);

  Serial.begin(9600);

  // Init watchdog timer
  watchdogSetup();
  watchdogCounter = 0;
  
  // WISOL test
  flagInit = -1;
  while (flagInit == -1) {
    Serial.println(""); // Make a clean restart
    delay(1000);
    PublicModeSF = 0;
    flagInit = Isigfox->initSigfox();
    Isigfox->testComms();
    GetDeviceID();
    //Isigfox->setPublicKey(); // set public key for usage with SNEK
  }
  
  // Init sensors on Thinxtra Module
  tSensors->initSensors();
  tSensors->setReed(reedIR);
  buttonCounter = 0;
  tSensors->setButton(buttonIR);

  // Init LED
  stateLED = 0;
  ledCounter = 0;
//  pinMode(redLED, INPUT);

  // Init timer to send a Sigfox message every 1 minutes
  unsigned long sendInterval = 60000;
  timer.setInterval(sendInterval, timeIR);

  Serial.println(""); // Make a clean start
  delay(1000);
}

void loop() {
  timer.run();
  wdt_reset();
  watchdogCounter = 0;
//  getRed();
//  getGreen();
//  getBlue();
}

void Send_Sensors(){
  UINT16_t tempt, photo, pressure, red, green, blue;
  INT16_t x_g, y_g, z_g;
  acceleration_xyz *xyz_g;
  FLOATUNION_t a_g;

  // Sending a float requires at least 4 bytes
  // Thus they can be stored in 2 bytes
  
  if (reqCounter == 0) {
    // No Alert Patient Data
    ph.number = (uint16_t) (660); // ph = 6.6
    Serial.print("pH: "); Serial.println((float)ph.number/100);
    glucose.number = (uint16_t) (50); // glucose = 0.5
    Serial.print("Glucose: "); Serial.println((float)glucose.number/100);
        
    red.number = (uint16_t) 255;
    green.number = (uint16_t) 250;
    blue.number = (uint16_t) 229;
    
  } else if (reqCounter == 1) {
    // Alert Nurse Patient Data
    ph.number = (uint16_t) (560); // ph = 5.6
    Serial.print("pH: "); Serial.println((float)ph.number/100);
    glucose.number = (uint16_t) (50); // glucose = 0.5
    Serial.print("Glucose: "); Serial.println((float)glucose.number/100);

    red.number = (uint16_t) 231;
    green.number = (uint16_t) 203;
    blue.number = (uint16_t) 84;
    
  } else if (reqCounter == 2) {
    // Alert Doctor Patient Data
    ph.number = (uint16_t) (490); // ph = 4.9
    Serial.print("pH: "); Serial.println((float)ph.number/100);
    glucose.number = (uint16_t) (50); // glucose = 0.5
    Serial.print("Glucose: "); Serial.println((float)glucose.number/100);
        
    red.number = (uint16_t) 212;
    green.number = (uint16_t) 99;
    blue.number = (uint16_t) 31;
    
  } else {
    ph.number = (uint16_t) (770); // ph = 7.7
    Serial.print("pH: "); Serial.println((float)ph.number/100);
    glucose.number = (uint16_t) (50); // glucose = 0.5
    Serial.print("Glucose: "); Serial.println((float)glucose.number/100);
    
    getColor();
    
    red.number = (uint16_t) redFrequency;
    green.number = (uint16_t) greenFrequency;
    blue.number = (uint16_t) blueFrequency;
  }


  
  const uint8_t payloadSize = 10; //in bytes
//  byte* buf_str = (byte*) malloc (payloadSize);
  uint8_t buf_str[payloadSize];

  buf_str[0] = ph.bytes[0];
  buf_str[1] = ph.bytes[1];
  buf_str[2] = glucose.bytes[0];
  buf_str[3] = glucose.bytes[1];
  buf_str[4] = red.bytes[0];
  buf_str[5] = red.bytes[1];
  buf_str[6] = green.bytes[0];
  buf_str[7] = green.bytes[1];
  buf_str[8] = blue.bytes[0];
  buf_str[9] = blue.bytes[1];

  reqCounter = reqCounter + 1;

  Send_Pload(buf_str, payloadSize);
//  free(buf_str);
}

void reedIR(){
  Serial.println("Reed");
  timer.setTimeout(50, Send_Sensors); // send a Sigfox message after get out IRS
}

void buttonIR(){
  if (buttonCounter==0) {
    timer.setTimeout(500, checkLongPress); // check long click after 0.5s
  }
}

void checkLongPress() {
  buttonCounter++;
  if ((buttonCounter < 4)) {
    if (digitalRead(buttonPin) == 1) {
      Serial.println("Short Press");
      Send_Sensors();
      buttonCounter = 0;
    } else {
      timer.setTimeout(500, checkLongPress); // check long click after 0.5s
    }
  } else {
    Serial.println("Long Press");
    BlinkLED();
    pinMode(redLED, OUTPUT);
    if (PublicModeSF == 0) {
      Serial.println("Set public key");
      Isigfox->setPublicKey();
      PublicModeSF = 1;
  
    } else {
      Serial.println("Set private key");
      Isigfox->setPrivateKey();
      PublicModeSF = 0;
    }
    buttonCounter = 0;
  }
}


void BlinkLED() {
  ledCounter++;
  if (ledCounter<=6) {
    if (stateLED == 0){
      digitalWrite(redLED, HIGH);
      stateLED = 1;
      timer.setTimeout(200, BlinkLED);
    } else {
      digitalWrite(redLED, LOW);
      stateLED = 0;
      timer.setTimeout(200, BlinkLED);
    }
  } else {
    pinMode(redLED, INPUT);
    ledCounter = 0;
  }
  
  
}

void timeIR(){
  Serial.println("Time");
  Send_Sensors();
}

void getDLMsg(){
  recvMsg *RecvMsg;
  int result;

  RecvMsg = (recvMsg *)malloc(sizeof(recvMsg));
  result = Isigfox->getdownlinkMsg(RecvMsg);
  for (int i=0; i<RecvMsg->len; i++){
    Serial.print(RecvMsg->inData[i]);
  }
  Serial.println("");
  free(RecvMsg);
}


void Send_Pload(uint8_t *sendData, const uint8_t len){
  // No downlink message require
  recvMsg *RecvMsg;

  RecvMsg = (recvMsg *)malloc(sizeof(recvMsg));
  Isigfox->sendPayload(sendData, len, 0, RecvMsg);
  for (int i = 0; i < RecvMsg->len; i++) {
    Serial.print(RecvMsg->inData[i]);
  }
  Serial.println("");
  free(RecvMsg);


  // If want to get blocking downlink message, use the folling block instead
  /*
  recvMsg *RecvMsg;

  RecvMsg = (recvMsg *)malloc(sizeof(recvMsg));
  Isigfox->sendPayload(sendData, len, 1, RecvMsg);
  for (int i=0; i<RecvMsg->len; i++){
    Serial.print(RecvMsg->inData[i]);
  }
  Serial.println("");
  free(RecvMsg);
  */

  // If want to get non-blocking downlink message, use the folling block instead
  /*
  Isigfox->sendPayload(sendData, len, 1);
  timer.setTimeout(46000, getDLMsg);
  */
}


void GetDeviceID(){
  recvMsg *RecvMsg;
  const char msg[] = "AT$I=10";

  RecvMsg = (recvMsg *)malloc(sizeof(recvMsg));
  Isigfox->sendMessage(msg, 7, RecvMsg);

  Serial.print("Device ID: ");
  for (int i=0; i<RecvMsg->len; i++){
    Serial.print(RecvMsg->inData[i]);
  }
  Serial.println("");
  free(RecvMsg);
}


void watchdogSetup(void) { // Enable watchdog timer
  cli();  // disable all interrupts
  wdt_reset(); // reset the WDT timer
  /*
   WDTCSR configuration:
   WDIE = 1: Interrupt Enable
   WDE = 1 :Reset Enable
   WDP3 = 1 :For 8000ms Time-out
   WDP2 = 1 :For 8000ms Time-out
   WDP1 = 1 :For 8000ms Time-out
   WDP0 = 1 :For 8000ms Time-out
  */
  // Enter Watchdog Configuration mode:
  // IF | IE | P3 | CE | E | P2 | P1 | P0
  WDTCSR |= B00011000;
  WDTCSR = B01110001;
//  WDTCSR |= (1<<WDCE) | (1<<WDE);
//  // Set Watchdog settings:
//   WDTCSR = (1<<WDIE) | (1<<WDE) | (1<<WDP3) | (1<<WDP2) | (1<<WDP1) | (1<<WDP0);
  sei();
}


void watchdog_disable() { // Disable watchdog timer
  cli();  // disable all interrupts
  WDTCSR |= B00011000;
  WDTCSR = B00110001;
  sei();
}


ISR(WDT_vect) // Watchdog timer interrupt.
{
// Include your code here - be careful not to use functions they may cause the interrupt to hang and
// prevent a reset.
  Serial.print("WD reset: ");
  Serial.println(watchdogCounter);
  watchdogCounter++;
  if (watchdogCounter == 20) { // reset CPU after about 180 s
      // Reset the CPU next time
      // Enable WD reset
      cli();  // disable all interrupts
      WDTCSR |= B00011000;
      WDTCSR = B01111001;
      sei();
      wdt_reset();
  } else if (watchdogCounter < 8) {
    wdt_reset();
  }
}

void getColor() {
  // Sample color values SAMPLING_RATE times and take average for each color  
  for (int i=0; i<SAMPLING_RATE; i++) {
    redValues[i] = getRed();
    greenValues[i] = getGreen();
    blueValues[i] = getBlue();
  }
  redFrequency = averageArray(redValues, SAMPLING_RATE);
  greenFrequency = averageArray(greenValues, SAMPLING_RATE);
  blueFrequency = averageArray(blueValues, SAMPLING_RATE);

  // Reset values in array for next reading
  memset(redValues, 0, sizeof(redValues));
  memset(greenValues, 0, sizeof(redValues));
  memset(blueValues, 0, sizeof(blueValues));
}

int getRed() {
    // Setting red filtered photodiodes to be read
    digitalWrite(S2,LOW);
    digitalWrite(S3,LOW);
    
    // Reading the output frequency
    int freq = pulseIn(sensorOut, LOW);

    // Remap frequency
    freq = map(freq, 40,3,0,255);

    
    // Printing the value on the serial monitor
    Serial.print("R= ");//printing name
    Serial.print(freq);//printing RED color frequency
    Serial.print("  ");
    
    return freq;
}

int getGreen() {
    // Setting Green filtered photodiodes to be read
    digitalWrite(S2,HIGH);
    digitalWrite(S3,HIGH);
    
    // Reading the output frequency
    int freq = pulseIn(sensorOut, LOW);

    // Remap frequency
    freq = map(freq, 60,3,0,255);
    
    // Printing the value on the serial monitor
    Serial.print("G= ");//printing name
    Serial.print(freq);//printing RED color frequency
    Serial.print("  ");
    
    return freq;
}

int getBlue() {
    // Setting Blue filtered photodiodes to be read
    digitalWrite(S2,LOW);
    digitalWrite(S3,HIGH);
    
    // Reading the output frequency
    int freq = pulseIn(sensorOut, LOW);

    // Remap frequency
    freq = map(freq, 20,0,0,255);
    
    // Printing the value on the serial monitor
    Serial.print("B= ");//printing name
    Serial.print(freq);//printing RED color frequency
    Serial.println("  ");
    
    return freq;
}

/* 
 *  Average array code is by Benjamin Winiarski
 *  Published February 24, 2018 
 *  Available at: https://www.hackster.io/benwiniarski/smart-pool-alexa-controlled-pool-manager-5454c1
  */
double averageArray(int *arr, int number) {
    int i;
    int max, min;
    double avg;
    long amount = 0;
    
    if (number <= 0) {
        printf("Error number for the array to averaging!/n");
        return 0;
    }
    
    if (number < 5) { //less than 5, calculated directly statistics
        for (i = 0; i < number; i++) {
            amount += arr[i];
        }
        avg = amount / number;
        return avg;
    } else {
        if (arr[0] < arr[1]) {
            min = arr[0];
            max = arr[1];
        } else {
            min = arr[1];
            max = arr[0];
        }
        for (i = 2; i < number; i++) {
            if (arr[i] < min) {
                amount += min; //arr<min
                min = arr[i];
            } else {
                if (arr[i] > max) {
                    amount += max; //arr>max
                    max = arr[i];
                } else {
                    amount += arr[i]; //min<=arr<=max
                }
            } //if
        } //for
        avg = (double)amount / (number - 2);
    } //if
    return avg;
}
