# Industrial IoT Gateway Prototype (Arduino + Raspberry Pi)

### 1. Project Overview
A mock industrial temperature and humidity monitoring system that simulates the **Edge-to-Cloud** data pipeline used in modern engineering.

This project interfaces a low-level microcontroller (**Arduino**) acting as a sensor with a Single Board Computer (**Raspberry Pi**) acting as an IoT Gateway. Data is processed at the edge and transmitted via **MQTT**.

**Real-time data visualization using standard MQTT Mobile Clients.**

| **Live Data Stream** | **Connection Status** |
|:---:|:---:|
| <img src="assets/screen_shots/mobile_phone_messages.PNG"> | <img src="assets/screen_shots/mobile_phone_connection.png"> |
| *Monitoring Temp/Humidity in real-time* | *Secure TLS Connection to HiveMQ* |

### 2. Architecture
**[Edge Device]** --> **[Python Gateway]** --> **[Cloud]** --> **[(Mobile) Client]**

1.  **Edge Node (Arduino Uno):**
    *   Reads Temperature/Humidity data (DHT11).
    *   Performs local logic (Red LED triggers if Temp > 25°C), simulating an alarm for overheating.
    *   Serializes data into JSON format.
2.  **Python Gateway (Raspberry Pi 4):**
    *   Listens to Serial/USB interface.
    *   Parses incoming JSON packets.
    *   Transmits data to the Cloud via MQTT.
3.  **Communication**
    *   Serial (USB): JSON encoded data.
    *   MQTT (WIFI): Secure TLS connection to HiveMQ Cloud.

### 3. Features:
*   **Real-Time Data Desrialization:** desrializes the incoming JSON data for further processing in real time

*   **Fault Tolerance:** Handles serial disconnections and non-JSON data without crashing.

*   **Security:** Uses environment variables (.env) for credentials and TLS for cloud transport.


### 4. Tech Stack
*   **Hardware:** Arduino Uno, Raspberry Pi 4, DHT Sensor.
*   **Embedded:** C++ (Arduino Framework).
*   **Gateway:** Python 3, PySerial, Paho-MQTT.
*   **Protocols:** UART (Serial), MQTT, JSON.

### 5. Circuit Diagram
The circuit consists of a DHT11 temperature sensor and a status LED connected to the Arduino Uno.

**1. Wiring Diagram**
<img src="assets/diagrams/wiring_arduino_iot_industrial_gateway.png">

**2. Schematic View**
<img src="assets/diagrams/wiring_schematic_iot_industrial_gateway.png">

(designed with https://www.tinkercad.com/, *note: The standard temp. sensor is a placholder for the DHT11*)


**Wiring Pinout:**
| Component | Arduino Pin |
| :--- | :--- |
| **DHT11 Data** | Pin 6 |
| **Red LED** | Pin A3 |
| **VCC** | 5V |
| **GND** | GND |

### 6. How to Run
**1. The Edge Node**
Flash the `arduino_edge/sensor_node.ino` to the Arduino Board.

**2. The Gateway**
Install dependencies on the Raspberry Pi:
`pip install -r pi_gateway/requirements.txt`

Run the gateway script:
`python3 pi_gateway/gateway.py`

### 7. Future Improvements
*   Add a local SQLite database on the Pi for offline data buffering.
*   Integrate Docker to containerize the Gateway script.
