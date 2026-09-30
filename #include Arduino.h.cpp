#include <Arduino.h>

#define SENSOR_PIN    PA0   
#define STEPPER_DIR   PA1   
#define STEPPER_STEP  PA2   
#define STEPPER_EN    PA3   
#define MCB_BTN_PIN   PA4   

const int STEPS_FOR_1_3_TURNS = 260; 
const float CALIBRATION_FACTOR = 0.0488; 

void rotateStepper(bool direction, int steps) {
  digitalWrite(STEPPER_EN, LOW); // Active LOW on DRV8825/A4988
  digitalWrite(STEPPER_DIR, direction ? HIGH : LOW);
  delayMicroseconds(10);
  
  for (int i = 0; i < steps; i++) {
    digitalWrite(STEPPER_STEP, HIGH);
    delayMicroseconds(800);
    digitalWrite(STEPPER_STEP, LOW);
    delayMicroseconds(800);
  }
  
  digitalWrite(STEPPER_EN, HIGH); // Disable outputs to prevent overheating
}

void sampleAndStream1SecCurrent() {
  unsigned long startTime = millis();
  
  // Collect data over 1000ms in 20ms chunks (50 data points total)
  while (millis() - startTime < 5000) {
    unsigned long chunkStart = millis();
    double sumSq = 0;
    long sampleCount = 0;
    
    // Sample high-speed for 20 milliseconds
    while (millis() - chunkStart < 20) {
      int rawADC = analogRead(SENSOR_PIN);
      int offsetADC = rawADC - 2048; // Offset around 1.65V bias
      sumSq += (double)offsetADC * offsetADC;
      sampleCount++;
      delayMicroseconds(100);
    }
    
    double meanSq = sumSq / sampleCount;
    float currentRMS = sqrt(meanSq) * CALIBRATION_FACTOR;
    
    // Filter out floating/idle noise floor
    if (currentRMS < 0.3) currentRMS = 0.0;
    
    unsigned long elapsedTimeMs = millis() - startTime;
    
    // Send time (ms) and current (A) over serial
    Serial.print("DATA:");
    Serial.print(elapsedTimeMs);
    Serial.print(",");
    Serial.println(currentRMS, 2);
  }
  
  Serial.println("GRAPH_COMPLETE");
}

void setup() {
  Serial.begin(9600);
  
  pinMode(STEPPER_DIR, OUTPUT);
  pinMode(STEPPER_STEP, OUTPUT);
  pinMode(STEPPER_EN, OUTPUT);
  digitalWrite(STEPPER_EN, HIGH); 
  
  pinMode(MCB_BTN_PIN, INPUT_PULLUP);
  analogReadResolution(12); 
}

void loop() {
  // Read multi-character string commands over Serial
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    
    if (cmd == "CW") {
      rotateStepper(true, STEPS_FOR_1_3_TURNS);
      Serial.println("STATUS: Rotated 1.3 turns CW");
    } 
    else if (cmd == "CCW") {
      rotateStepper(false, STEPS_FOR_1_3_TURNS);
      Serial.println("STATUS: Rotated 1.3 turns CCW");
    }
  }
  
  // Hardware Button Check
  if (digitalRead(MCB_BTN_PIN) == LOW) {
    delay(50); // Debounce
    if (digitalRead(MCB_BTN_PIN) == LOW) {
      Serial.println("EVENT: MCB Switch Tripped! Measuring...");
      sampleAndStream1SecCurrent();
      while(digitalRead(MCB_BTN_PIN) == LOW); 
    }
  }
}