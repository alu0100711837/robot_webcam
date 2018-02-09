/*  Arduino servo control by serial port.
    Alexis Rodríguez Casañas.
    Last update: 09.02.2018
*/


#include <Servo.h>

#define MOVEMENT 3
#define XSERVOPIN 9
#define CENTER 90

Servo xServo, yServo;
int xServoPos, yServoPos;

char readByte;


void moveXServo(char direction)
{
  if (direction == 'a')
  {
    if (xServoPos > 3)
      xServoPos-= MOVEMENT;
      xServo.write(xServoPos);
  }
  else
  {
    if (xServoPos < 180)
      xServoPos+= MOVEMENT;
      xServo.write(xServoPos);
  }
}

void moveYServo(char direction)
{
  if (direction == 'c')
  {
    if (yServoPos > 0)
      yServoPos-= MOVEMENT;
      yServo.write(yServoPos);
  }
  else
  {
    if (yServoPos < 180)
      yServoPos+= MOVEMENT;
      yServo.write(yServoPos);
  }
}

void setup()
{

  xServo.attach(XSERVOPIN);
  //yServo.attach();

  xServoPos = CENTER;
  yServoPos = CENTER;

  Serial.begin(9600);
}

void loop()
{
  if (Serial.available() > 0)
  {
     readByte = Serial.read();
     switch(readByte)
     {
      case('a'):
      case('b'):
        moveXServo(readByte);
        break;

      case('c'):
      case('d'):
        moveYServo(readByte);
        break;
     }
  }
}

