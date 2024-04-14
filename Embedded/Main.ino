#include <MD_Parola.h>
#include <MD_MAX72xx.h>
#include <SPI.h>
#include <iarduino_RTC.h>

#define HARDWARE_TYPE MD_MAX72XX::FC16_HW
#define MAX_DEVICES 4
#define CS_PIN 10
#define EXTRACT_DIGITS(str, idx) ((str[idx] - '0') * 10) + (str[idx + 1] - '0')

int compileHour = EXTRACT_DIGITS(_TIME_, 0);
int compileMinute = EXTRACT_DIGITS(_TIME_, 3);

MD_Parola myDisplay = MD_Parola(HARDWARE_TYPE, CS_PIN, MAX_DEVICES);

unsigned long startTime;
unsigned long startTimeClock = 67000000;
unsigned long countdownDuration = 50 * 60; // 50 minutes in seconds
int sensor;
int sensorReading;

iarduino_RTC time (RTC_DS1302,7,5,6);


const int interruptPinWorkClock = 2; // switch between work and Clock mode
const int interruptPinStopResume = 3; // stops and resumes the timer
const int sensorPin = 4; // sensor pin
volatile int FlagWork = 0; // 1 for work mode, 0 for clock mode
volatile int FlagStop = 0; // 1 for stop, 0 for resume

unsigned long lastDebounceTimeWorkClock = 0; // debounce time for work and clock mode
unsigned long lastDebounceTimeStopResume = 0; // debounce time for stop and resume
unsigned long debounceDelay = 1000;

void setup() {
  Serial.begin(9600);
  myDisplay.begin();
  myDisplay.setIntensity(1);
  myDisplay.displayClear();

  time.begin();
  time.settime(0, 8, 17, 14, 4, 2024, 0); // seconds, minutes, hours, day of the month, month, year, day of the week

  // pins and interupts
    pinMode(interruptPinWorkClock, INPUT_PULLUP);
    pinMode(interruptPinStopResume, INPUT_PULLUP);
    pinMode(sensorPin, INPUT_PULLUP);

    attachInterrupt(digitalPinToInterrupt(interruptPinWorkClock), workClock, CHANGE); // switch between work and Clock mode
    attachInterrupt(digitalPinToInterrupt(interruptPinStopResume), stopResume, CHANGE); // stops and resumes the timer
    startTime = millis(); // Initialize the start time
}

void loop() {
  if (myDisplay.displayAnimate()) {
    myDisplay.displayReset();
  }
  startpomodoro();
  clock();
  int sensorReading = digitalRead(4);
  if (sensorReading == LOW) {
    sensor = 0;
  }
  else {
    sensor = 1;
  }
  Serial.println(sensorReading);
  delay(500);
}

void startpomodoro() {
    static unsigned long pomodoroStartTime = 0;
    static unsigned long pomodoroDuration = countdownDuration;
    static bool isPomodoro = true;
      int sensorReading = digitalRead(4);
      int sensor;

    if (FlagWork == 1 || sensor == 0) {
        unsigned long currentTime = millis();
        unsigned long elapsedTime = currentTime - startTime;

        // Calculate remaining time
        unsigned long remainingTime = pomodoroDuration - (elapsedTime / 1000); // Convert milliseconds to seconds

        // Check if countdown is complete
        if (remainingTime <= 0) {
            if (isPomodoro) {
                // Pomodoro timer ended, start the 10-minute break
                pomodoroStartTime = currentTime;
                pomodoroDuration = 10.07 * 60; // 10 minutes in seconds
                isPomodoro = false;
            } else {
                // Break timer ended, start the 50-minute pomodoro
                pomodoroStartTime = currentTime;
                pomodoroDuration = countdownDuration;
                isPomodoro = true;
            }
        }

        // Convert remaining time to hours, minutes, and seconds
        int hours = remainingTime / 3600;
        int minutes = (remainingTime % 3600) / 60;
        int seconds = remainingTime % 60;

        // Format time as string (HH-MM-SS)
        char timeStr[9];
        sprintf(timeStr, "%02d:%02d", minutes, seconds);

        // Display the countdown timer
        myDisplay.displayText(timeStr, PA_CENTER, 0, 0, PA_PRINT, PA_NO_EFFECT);
    }
}

void clock() {
  int sensorReading = digitalRead(4);
  int sensor;
  // Get current time
  if (FlagWork == 0 || sensorReading == 1){
    time.gettime();
    int hours = time.Hours;
    int minutes = time.minutes;

    // Format time as string (HH:MM:SS)
    char timeStr[9];
    sprintf(timeStr, "%02d:%02d", hours, minutes);

    // Display the current time
    myDisplay.displayText(timeStr, PA_CENTER, 0, 0, PA_PRINT, PA_NO_EFFECT);
  }
}

void workClock() {
  if (millis() - lastDebounceTimeWorkClock > debounceDelay) {
    FlagWork = !FlagWork;
    lastDebounceTimeWorkClock = millis();
  }
  Serial.println(FlagWork);
}

void stopResume() {
  if (millis() - lastDebounceTimeStopResume > debounceDelay) {
    FlagStop = !FlagStop;
    lastDebounceTimeStopResume = millis();
  }
  Serial.println(FlagStop);
}