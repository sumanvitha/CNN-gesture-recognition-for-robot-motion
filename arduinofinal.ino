




#include <AFMotor.h>


#define trigPin 9 // define the pins of your sensor
#define echoPin 10 

AF_DCMotor motor1(2);
AF_DCMotor motor2(1);
char k='A';
void setup() {
  
  pinMode(LED_BUILTIN, OUTPUT);
  motor1.setSpeed(250);
  motor2.setSpeed(250);
  pinMode(trigPin, OUTPUT);// set the trig pin to output (Send sound waves)
  pinMode(echoPin, INPUT);// set the echo pin to input (recieve sound waves)
  Serial.begin(9600);
   Serial.write('1');
  
}
int i=0;
// the loop function runs over and over again forever
void loop() {
  long duration, distance; 
  k='A';
  if(Serial.available()>0) {
         k=Serial.read();
        Serial.println(k);
  }
 
        if(k=='S') {
           // start the scan
  digitalWrite(trigPin, LOW);  
  delayMicroseconds(2); // delays are required for a succesful sensor operation.
  digitalWrite(trigPin, HIGH);
   

  delayMicroseconds(10); //this delay is required as well!
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = (duration/2) / 29.1;
  
          if(distance>20)
          {
          Serial.println(k);
         digitalWrite(LED_BUILTIN, HIGH);
         motor1.run(BACKWARD);
         motor2.run(BACKWARD);
          }
          else
          {
            motor1.run(RELEASE);
            motor2.run(RELEASE);
             
          }
        }
        else if(k=='B'){
          
          Serial.println(k);
            digitalWrite(LED_BUILTIN, LOW);
            motor1.run(FORWARD);
            motor2.run(FORWARD);
                    }

                 else if(k=='L'){
                  
          Serial.println(k);
            digitalWrite(LED_BUILTIN, LOW);
          
            motor2.run(FORWARD);
            motor1.run(BACKWARD);
            delay(1500);
            motor2.run(RELEASE);
            motor1.run(RELEASE);
            delay(1000);
          
          
                    }
              else if(k=='R'){
                
          Serial.println(k);
            digitalWrite(LED_BUILTIN, LOW);
            motor2.run(BACKWARD);
            motor1.run(FORWARD);
            delay(1500);
            motor2.run(RELEASE);
            motor1.run(RELEASE);
            delay(1000);
            
                    }
              else if(k=='T'){
                
          Serial.println(k);
            digitalWrite(LED_BUILTIN, LOW);
            motor1.run(RELEASE);
            motor2.run(RELEASE);
                    }



                   
                   // wait for a second
}
