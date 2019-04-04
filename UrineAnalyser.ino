#define COLOUROUT A5
#define COLOURS2 A4
#define COLOURS3 A3

// Stores frequency read by the photodiodes
typedef struct {
    int red;
    int green;
    int blue;
} Colour; 

void setup() {
  Serial.begin(115200);
  pinMode(COLOUROUT, INPUT);
  pinMode(COLOURS2, OUTPUT);
  pinMode(COLOURS3, OUTPUT);
}

void loop() {
  Colour colour = {0, 0, 0};

  // Get red value
  colourRed();
  Serial.print("RED:");
  colour.red = getIntensity();
  Serial.print(colour.red);

  // Get green value
  colourGreen();
  Serial.print("GREEN:");
  colour.green = getIntensity();
  Serial.print(colour.green);

  // Get blue value
  colourBlue();
  Serial.print("BLUE:");
  colour.blue = getIntensity();
  Serial.print(colour.blue);
  
  delay(200);

  // TODO: Other sensor data extraction

  // Send the data to application
//  if (client.connect(server, 80)) {
//    client.println("POST /Api HTTP/1.1");
//    client.println("Host: 10.0.0.138");
//    client.println("User-Agent: Arduino/1.0");
//    client.println("Connection: close");
//    client.print("Content-Length: ");
//    client.println(PostData.length());
//    client.println();
//    client.println(PostData);
//  }
}

void colourRed(){             //select red
  digitalWrite(COLOURS2, LOW);
  digitalWrite(COLOURS3, LOW);
}

void colourBlue(){            //select blue
  digitalWrite(COLOURS2, LOW);
  digitalWrite(COLOURS3, HIGH);
}

void colourWhite(){           //select white
  digitalWrite(COLOURS2, HIGH);
  digitalWrite(COLOURS3, LOW);
}

void colourGreen(){           //select green
  digitalWrite(COLOURS2, HIGH);
  digitalWrite(COLOURS3, HIGH);
}

int getIntensity(){           //measure intensity with oversampling
  int a = 0;
  int b = 255;

  for (int i=0; i<10; i++){
    a = a + pulseIn(COLOUROUT, LOW);
  }

  if (a > 9) {
    b = 2550/a;
  }
  return b;
}
