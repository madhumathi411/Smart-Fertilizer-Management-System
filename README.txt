SMART FERTILIZER MANAGEMENT SYSTEM

FLOW
Login -> Farmer Profile -> Farm Data Entry -> Analysis -> Fertilizer Recommendation -> Download Report

CURRENT HARDWARE METHOD
Arduino Uno + sensors -> LCD -> manually read values -> enter values into dashboard.

No Wi-Fi, cloud, Blynk, Firebase, or live Arduino-to-dashboard connection is used in this version.

RUN
1. Open this folder in VS Code.
2. Terminal:
   pip install -r requirements.txt
3. Start:
   python app.py
4. Browser:
   http://127.0.0.1:5000

Demo:
Username: demo
Password: demo
Crop: Rice
Farm area: 2
Moisture: 45
N: 25
P: 35
K: 40
Temperature: 28
Humidity: 70

IMPORTANT:
The nutrient thresholds and recommendations are prototype/demo logic. They should not be treated as real agronomic prescriptions. Final fertilizer dose should use crop, soil-test units, farm area, local agronomic guidance, and fertilizer formulation.
