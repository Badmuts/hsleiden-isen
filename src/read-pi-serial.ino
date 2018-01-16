const int ledPin = 13;

// the setup function runs once when you press reset or power the board
void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}

// the loop function runs over and over again forever
void loop() {
  String content = "";
  if(Serial.available()){
    while(Serial.available()) {
      Serial.println(Serial.readString());
      content += Serial.readString();
      
    }
  }
  if(content.length() > 6) {
    Serial.println("content: ");
    Serial.println(content);
    delay(1000);
  }
  

}