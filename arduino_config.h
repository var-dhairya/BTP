/*
 * Adaptive Quiz System - Arduino/ESP32 Configuration
 * Optimized for embedded hardware deployment
 */

#ifndef ARDUINO_CONFIG_H
#define ARDUINO_CONFIG_H

// System Configuration
#define QUIZ_SYSTEM_VERSION "1.0.0"
#define MAX_QUESTIONS_PER_SESSION 10
#define MAX_STUDENTS 50
#define MAX_QUESTIONS_IN_MEMORY 100

// ML Model Configuration (Optimized for embedded systems)
#define ML_MODEL_TYPE "RandomForest"
#define ML_FEATURE_COUNT 5
#define ML_MAX_ESTIMATORS 25  // Reduced for memory efficiency
#define ML_MAX_DEPTH 8        // Reduced for speed

// Difficulty Levels
#define MIN_DIFFICULTY 1.0
#define MAX_DIFFICULTY 10.0
#define DIFFICULTY_STEP 0.5

// Performance Tracking
#define MAX_PERFORMANCE_HISTORY 50  // Reduced for memory efficiency
#define RESPONSE_TIME_TIMEOUT 300   // 5 minutes in seconds
#define MIN_QUESTIONS_FOR_TRAINING 5

// Storage Configuration
#define USE_SD_CARD true
#define USE_SPIFFS false
#define DATA_FILE_PATH "/quiz_data/"
#define MODEL_FILE_PATH "/ml_model.bin"

// Network Configuration (for ESP32)
#define WIFI_SSID "YourWiFiSSID"
#define WIFI_PASSWORD "YourWiFiPassword"
#define API_SERVER_PORT 80

// Display Configuration
#define DISPLAY_TYPE "OLED_128x64"  // or "TFT_240x320" or "LCD_16x2"
#define USE_TOUCH_INPUT true

// Input/Output Configuration
#define BUTTON_DEBOUNCE_MS 50
#define LED_INDICATOR_PIN 2
#define BUZZER_PIN 4

// Memory Optimization
#define USE_JSON_STREAMING true
#define COMPRESS_MODEL_WEIGHTS true
#define USE_FLOAT_32 true  // Use 32-bit floats instead of 64-bit

// Debug Configuration
#define DEBUG_MODE false
#define SERIAL_BAUD_RATE 115200
#define LOG_LEVEL 1  // 0=Error, 1=Warning, 2=Info, 3=Debug

// Feature Flags
#define ENABLE_REAL_TIME_ANALYTICS false
#define ENABLE_CLOUD_SYNC false
#define ENABLE_OFFLINE_MODE true
#define ENABLE_BATTERY_OPTIMIZATION true

// Pin Definitions (ESP32)
#define BUTTON_1_PIN 12
#define BUTTON_2_PIN 13
#define BUTTON_3_PIN 14
#define BUTTON_4_PIN 15
#define BUTTON_5_PIN 16

#define LED_RED_PIN 17
#define LED_GREEN_PIN 18
#define LED_BLUE_PIN 19

// I2C Configuration
#define I2C_SDA_PIN 21
#define I2C_SCL_PIN 22
#define I2C_FREQUENCY 100000

// SPI Configuration (for SD card)
#define SPI_MISO_PIN 19
#define SPI_MOSI_PIN 23
#define SPI_SCK_PIN 18
#define SPI_CS_PIN 5

#endif // ARDUINO_CONFIG_H
