#include <Adafruit_NeoPixel.h>


// Control panel LEDs
#define controlPanelLED_PIN 4
#define controlPanelLED_COUNT 41
Adafruit_NeoPixel controlPanelLED(controlPanelLED_COUNT, controlPanelLED_PIN, NEO_GRB + NEO_KHZ800);

// chessboard LEDs
#define chessboardLED_PIN A5
#define chessboardLED_COUNT 64
Adafruit_NeoPixel chessboardLED(chessboardLED_COUNT, chessboardLED_PIN, NEO_GRB + NEO_KHZ800);


uint32_t ledWHITE = controlPanelLED.Color(255, 255, 255);
uint32_t ledBLACK = controlPanelLED.Color(0, 0, 0);
uint32_t ledBLUE = controlPanelLED.Color(0, 0, 255);
uint32_t ledRED = controlPanelLED.Color(255, 0, 0);
uint32_t ledGREEN = controlPanelLED.Color(0, 255, 0);

const int delayTiming = 1000;
const int inputButtons[] = { 3, 5, 6, 7, 8, 9, 10, 11, 12, A1 };
const int buttonDebounceTime = 300;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);

  // Setup the buttons for input.
  for (int i = 0; i < 10; i++)  // <= represents how many buttons we are using for this to complete enough loops.
  {
    pinMode(inputButtons[i], INPUT_PULLUP);
  }

  // Setup the hint interupt pin
  attachInterrupt(digitalPinToInterrupt(3), hint, FALLING);


  // Setup for the control panels neopixels
  controlPanelLED.begin();             // INITIALIZE NeoPixel strip object (REQUIRED)
  controlPanelLED.show();              // Turn OFF all pixels ASAP
  controlPanelLED.setBrightness(100);  // Set BRIGHTNESS (max = 255)

  // Setup for the chessboard neopixels
  chessboardLED.begin();            // INITIALIZE NeoPixel strip object (REQUIRED)
  chessboardLED.show();             // Turn OFF all pixels ASAP
  chessboardLED.setBrightness(20);  // Set BRIGHTNESS (max = 255)
}

void loop() {
  int row_counter = 0;

  for (int i = 0; i < 64; i++)
  {
    if (i % 2 == 0)
    {
        chessboardLED.fill(ledWHITE, row_counter, 8);
    }
    else
    {
      chessboardLED.fill(ledBLUE, row_counter, 8);
    }

    row_counter++;
  }

  chessboardLED.show();
  delay(delayTiming);

  controlPanelLED.fill(ledWHITE, 0, 2);
  controlPanelLED.show();
  delay(delayTiming);
  controlPanelLED.fill(ledWHITE, 2, 2);
  controlPanelLED.show();
  delay(delayTiming);
  controlPanelLED.fill(ledWHITE, 4, 1);
  controlPanelLED.show();
  delay(delayTiming);
  controlPanelLED.fill(ledWHITE, 5, 1);
  controlPanelLED.show();
  delay(delayTiming);
  controlPanelLED.fill(ledWHITE, 6, 4);
  controlPanelLED.show();
  delay(delayTiming);

  while (true) {
    int detectButton();

    while (true)
    {
      if (digitalRead(5) == LOW) // A/1
      {
        Serial.println("A/1"); // Button pressed
        delay(delayTiming);   // Delay to avoid button bounce
        break;
      } else if (digitalRead(6) == LOW) // B/2
      {
        Serial.println("B/2");
        delay(delayTiming);
        break;
      } else if (digitalRead(7) == LOW) // C/3
      {
        Serial.println("C/3");
        delay(delayTiming);
        break;
      } else if (digitalRead(8) == LOW) // D/4
      {
        Serial.println("D/4");
        delay(delayTiming);
        break;
      } else if (digitalRead(9) == LOW) // E/5
      {
        Serial.println("E/5");
        delay(delayTiming);
        break;
      } else if (digitalRead(10) == LOW)  // F/6
      {
        Serial.println("F/6");
        delay(delayTiming);
        break;
      } else if (digitalRead(11) == LOW) // G/7
      {
        Serial.println("G/7");
        delay(delayTiming);
        break;
      } else if (digitalRead(12) == LOW) // H/8
      {
        Serial.println("H/8");
        delay(delayTiming);
        break;
      } else if (digitalRead(A1) == LOW) // Ok
      {
        delay(delayTiming);
        break;
      }
    }
  }
}


void hint() {
  static unsigned long last_interrupt_time = 0;
  unsigned long interrupt_time = millis();
  // If interrupts come faster than 200ms, assume it's a bounce and ignore
  if (interrupt_time - last_interrupt_time > 200) {
    Serial.println("Button connected to 'HINT' detected");
  }
  last_interrupt_time = interrupt_time;
}
