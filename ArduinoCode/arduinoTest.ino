#include <Servo.h>
int pwm_value=0;
String val_string="";
Servo PWM2;
Servo PWM3;
Servo PWM4;
Servo PWM5;
int pwmwidth2=1500;
int pwmwidth3=1500;
int pwmwidth4=1000;
int pwmwidth5=1500;
void setup(){
  PWM2.attach(2);//pin no. 1 of receiver..
  PWM3.attach(3);
  PWM4.attach(4);
  PWM5.attach(5);
  PWM2.writeMicroseconds(1500);
  PWM3.writeMicroseconds(1500);
  PWM4.writeMicroseconds(1000);
  PWM5.writeMicroseconds(1500);
  Serial.begin(128000);
  while(!Serial);
  Serial.println("Format channel:val(1000-2000)E");
}
void loop(){
  PWM2.writeMicroseconds(pwmwidth2);
  PWM3.writeMicroseconds(pwmwidth3);
  PWM4.writeMicroseconds(pwmwidth4);
  PWM5.writeMicroseconds(pwmwidth5);
  if(Serial.available()){
    int state=Serial.readStringUntil(':').toInt();
    if(state==1){
      int val=Serial.readStringUntil('E').toInt();
      PWM2.writeMicroseconds(val);
      pwmwidth2=val;
    }
    if(state==2){
      int val=Serial.readStringUntil('E').toInt();
      PWM3.writeMicroseconds(val);
      pwmwidth3=val;
    }
    if(state==3){
      int val=Serial.readStringUntil('E').toInt();
      PWM4.writeMicroseconds(val);
      pwmwidth4=val;
    }
    if(state==4){
      int val=Serial.readStringUntil('E').toInt();
      PWM5.writeMicroseconds(val);
      pwmwidth5=val;
    }
  }
}
