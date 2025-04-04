#define TRIG_PIN 12
#define ECHO_PIN 13

#define ENB 5
#define IN1 7
#define IN2 8
#define IN3 9
#define IN4 11
#define ENA 6
#define carSpeed 175

long getDistance() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  long duration = pulseIn(ECHO_PIN, HIGH);
  return duration * 0.034 / 2; // cm
}

void forward() {
  analogWrite(ENA, carSpeed);
  analogWrite(ENB, carSpeed);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  Serial.println("🟢 Forward");
}

void back() {
  analogWrite(ENA, carSpeed);
  analogWrite(ENB, carSpeed);
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  Serial.println("🔴 Backward");
}

void left() {
  analogWrite(ENA, carSpeed);
  analogWrite(ENB, carSpeed);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  Serial.println("🟡 Left");
}

void right() {
  analogWrite(ENA, carSpeed);
  analogWrite(ENB, carSpeed);
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  Serial.println("🔵 Right");
}

void stop() {
  digitalWrite(ENA, LOW);
  digitalWrite(ENB, LOW);
  Serial.println("⛔ Stop");
}

void setup() {
  Serial.begin(9600);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
}

void loop() {
  long front = getDistance();
  Serial.print("📏 Front Distance: ");
  Serial.print(front);
  Serial.println(" cm");

  if (front > 30) {
    forward();
  } else {
    stop();
    delay(300);

    // Path Optimization: Scan both sides
    right();
    delay(400);
    long rightDist = getDistance();
    stop();
    delay(300);

    left();
    delay(800);
    long leftDist = getDistance();
    stop();
    delay(300);

    // Re-center
    right();
    delay(400);
    stop();

    Serial.print("🔍 Left: ");
    Serial.print(leftDist);
    Serial.print(" | Right: ");
    Serial.println(rightDist);

    // Decision-making (Path Optimization)
    if (leftDist > rightDist && leftDist > 30) {
      Serial.println("✅ Path Optimization: Going LEFT");
      left();
      delay(500);
    } else if (rightDist > 30) {
      Serial.println("✅ Path Optimization: Going RIGHT");
      right();
      delay(500);
    } else {
      Serial.println("⚠️ No clear path, backing up");
      back();
      delay(600);
    }
  }
}
