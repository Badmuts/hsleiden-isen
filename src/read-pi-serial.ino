const int ledPin = 13;
int number;

// the setup function runs once when you press reset or power the board
void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
  number = 7;
}

// the loop function runs over and over again forever
void loop() {
  if(Serial.available()){
    number = Serial.read();
  }
  
  Serial.print(number);
  Serial.print('\n');
  if(number == -1){
    number = 0;
  }
  digitalWrite(ledPin, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(number*100);              // wait for a second
  digitalWrite(ledPin, LOW);    // turn the LED off by making the voltage LOW
  delay(number*100);              // wait for a second
}
