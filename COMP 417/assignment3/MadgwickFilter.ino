//Ethan Lim 261029610
#include <Arduino_LSM6DS3.h>
#include <MadgwickAHRS.h>

Madgwick filter;
float ax, ay, az, gx, gy, gz;


void setup() {
  Serial.begin(115200);
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
  filter.begin(100); // Set filter update rate (e.g., 100 Hz)
}


void loop() {
  if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {
    IMU.readAcceleration(ax, ay, az);
    IMU.readGyroscope(gx, gy, gz);

    filter.updateIMU(gx, gy, gz, ax, ay, az);

    // Assuming the library provides methods to get roll, pitch, and yaw
    float roll = filter.getRoll();
    float pitch = filter.getPitch();
    float yaw = filter.getYaw();

    // Convert to degrees
    roll *= 180.0 / PI;
    pitch *= 180.0 / PI;
    yaw *= 180.0 / PI;

    // Normalize yaw to 0-360 degrees
    if (yaw < 0) {
      yaw += 360;
    }

    Serial.print(roll);
    Serial.print("\t");
    Serial.print(pitch);
    Serial.print("\t");
    Serial.println(yaw);

  }
  delay(10); // Adjust based on update rate
}


