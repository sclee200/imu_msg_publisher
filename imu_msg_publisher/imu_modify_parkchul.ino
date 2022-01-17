/*
  Range   : +/- 2 g
  Scale   : 16384 = 1 g
 */
#include <IMU.h>

cIMU    IMU;

uint8_t   led_tog = 0;
uint8_t   led_pin = 13;

double angleAcX;
double angleAcY;
double angleAcZ;

const double RADIAN_TO_DEGREE = 180 / 3.14159;
void setup()
{
  Serial.begin(115200);

  IMU.begin();

  pinMode( led_pin, OUTPUT );
}





void loop()
{
  static uint32_t tTime[3];
  static uint32_t imu_time = 0;


  if( (millis()-tTime[0]) >= 500 )
  {
    tTime[0] = millis();

    digitalWrite( led_pin, led_tog );
    led_tog ^= 1;
  }

  tTime[2] = micros();
  if( IMU.update() > 0 ) imu_time = micros()-tTime[2];



  if( (millis()-tTime[1]) >= 50 )
  {
    tTime[1] = millis();
#if 0
    Serial.print(imu_time);
    Serial.print(" \t");
    Serial.print(IMU.accRaw[0]);    // ACC X
    Serial.print(" \t");
    Serial.print(IMU.accRaw[1]);    // ACC Y
    Serial.print(" \t");
    Serial.print(IMU.accRaw[2]);    // ACC Z
    Serial.println(" ");
#endif


    // 삼각함수를 이용한 롤(Roll)의 각도 구하기 
    angleAcX = atan(IMU.accRaw[1] / sqrt(pow(IMU.accRaw[0], 2) + pow(IMU.accRaw[2], 2)));
    angleAcX *= RADIAN_TO_DEGREE;
    // 삼각함수를 이용한 피치(Pitch)의 각도 구하기
    angleAcY = atan(-IMU.accRaw[0] / sqrt(pow(IMU.accRaw[1], 2) + pow(IMU.accRaw[2], 2)));
    angleAcY *= RADIAN_TO_DEGREE;
    //angleAcZ값(Yaw)은 아래의 삼각함수 공식은 있으나, 가속도 센서만 이용해서는 원하는 데이터를 얻을 수 없어 생략
    angleAcZ = atan(sqrt(pow(IMU.accRaw[0], 2) + pow(IMU.accRaw[1], 2)) / IMU.accRaw[2] );
    angleAcZ *= RADIAN_TO_DEGREE;

    Serial.print("Angle x : ");
    Serial.print(angleAcX);
    Serial.print("\t\t Angle y : ");
    Serial.print(angleAcY);
    Serial.print("\t\t Angle z : ");
    Serial.println(angleAcZ);
  }
}
