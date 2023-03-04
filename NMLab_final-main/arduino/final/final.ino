#include <Servo.h>
#include "config.h"
#include "Arduino.h"
#include "SoftwareSerial.h"
#include "DFRobotDFPlayerMini.h"

# define ACTIVATED LOW

//SoftwareSerial mySoftwareSerial(10, 11); // RX, TX
//DFRobotDFPlayerMini myDFPlayer;
Servo myservo;

void setup() {
  // put your setup code here, to run once:
  myservo.attach(SERVO);
//  mySoftwareSerial.begin(9600);

//  int Volume = 10;//analogRead(buttonVolume) / 34.1;
//  myDFPlayer.volume(Volume);
  pinMode(LED_BUILTIN, OUTPUT);
  
  // start serial port at 9600 bps:
  Serial.begin(115200);
  // initialize digital pin LED_BUILTIN as an output.
  while (!Serial) {
    ;
  }
//  servo_turn(myservo, 90);
//  delay(300);
//  servo_turn(myservo, 0);
//  myDFPlayer.play();
}

void loop() {
  // put your main code here, to run repeatedly:
  // if we get a command, turn the LED on or off:
  if (Serial.available() > 0) {
    byte buffer[16];
    int size = Serial.readBytesUntil('\n', buffer, 12);
    Serial.println(buffer[0]);
//    digitalWrite(LED_BUILTIN, HIGH);
//    delay(200);
    
    if (buffer[0] == 48) {
      servo_turn(myservo, 0);
    }else if (buffer[0] == 49) {
      servo_turn(myservo, 90);
    }//else if (buffer[0] == 50) {
//      myDFPlayer.play(4);
//    }else if (buffer[0] == 51) {
//      myDFPlayer.play(3);
//    }else if (buffer[0] == 52) {
//      myDFPlayer.play(1);
//    }
  }
}

void servo_turn(Servo myservo, int angle){
  myservo.write(angle);
}

void servo_reset(Servo myservo){
  myservo.attach(SERVO);
}
