#include <Arduino.h>
#include <MD_Parola.h>
#include <MD_MAX72xx.h>
#include <SPI.h>

// Konfigurationswerte
#define BUTTON_PIN     4
boolean suspend        = false;
int prevButtonValue    = LOW;
boolean firstRun       = true;

#define DISPLAY_TYPE   MD_MAX72XX::FC16_HW
#define MAX_DISPLAYS   4
#define CLK_PIN        5
#define DATA_PIN       6
#define CS_PIN         7
#define TEXT           "Hallo, Arduino und hallo, AVR!"

//MD_Parola display = MD_Parola(DISPLAY_TYPE, CS_PIN, MAX_DISPLAYS);                     // Hardware SPI (Pins je nach Arduino-Modell unterschiedlich, dafür schneller)
MD_Parola display = MD_Parola(DISPLAY_TYPE, DATA_PIN, CLK_PIN, CS_PIN, MAX_DISPLAYS);    // Software SPI (Pins frei auswählbar, dafür CPU-Hungriger)


/**
 * Hardware initialisieren. Diese Funktion wird zum Einschalten
 * automatisch einmal aufgerufen.
 */
void setup(void) {
  Serial.begin(9600);
  Serial.println("Setup");

  pinMode(BUTTON_PIN, INPUT_PULLUP);
  display.begin();
}


/**
 * Haupfunktion des Programms. Diese Funktion wird automatisch in
 * einer Endlosschleife aufgerufen.
 */
void loop(void) {
  // Taster zum Anhalten/Fortsetzen der Animation abfragen
  int buttonValue = digitalRead(BUTTON_PIN);
  
  if (buttonValue != prevButtonValue) {
    prevButtonValue = buttonValue;

    if (buttonValue == HIGH && !firstRun) {
      Serial.println("Button pressed - toggle animation on/off");
      suspend = !suspend;
      display.displaySuspend(suspend);
    } else {
      firstRun = false;
    }
  }

  // Animation neustarten, sobald sie zu Ende gelaufen ist
  if (!suspend && display.displayAnimate()) {    
    display.displayScroll(TEXT, PA_CENTER, PA_SCROLL_LEFT, 100);
  }
}
