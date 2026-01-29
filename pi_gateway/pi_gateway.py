import json
import time
import sys
import serial
import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv


# --- CONFIGURATION CONSTANTS ---
load_dotenv()
SERVICE_PORT = os.getenv("SERIAL_PORT")
BAUD_RATE = 115200

MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PW = os.getenv("MQTT_PW")
MQTT_URL = os.getenv("MQTT_URL")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC")
MQTT_CLIENT_ID = "MacGateway"

def connect_serial():
    """
    Establishes the connection to the physical device (Arduino) via USB.
    Returns:
        serial.Serial: The active serial connection object.
    """
    try: 
        # Initialize serial connection using the constants defined above
        serial_instance = serial.Serial(SERVICE_PORT, BAUD_RATE)
        
        # Wait for the Arduino to reboot after connection is opened
        time.sleep(2)
        print("SUCCESS: Serial Port Connected")
        return serial_instance
    except serial.SerialException as e:
        print(f"FAILURE: Could not open serial port {SERVICE_PORT}")
        sys.exit()

def connect_mqtt():
    """
    Initializes the MQTT client, sets up security (TLS), and connects to the Cloud Broker.
    Returns:
        mqtt.Client: The active, connected MQTT client object.
    """
    
    # Callback: Executed when the broker responds to our connection request
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Cloud Connected Successfully!")
        else:
            print(f"Cloud Connection Failed (Code: {rc})")

    # Callback: Executed when a message is successfully sent to the cloud
    def on_publish(client, userdata, mid):
        print(f" >> Message {mid} sent to cloud!")

    # 1. Initialize Client
    # We use VERSION1 to ensure compatibility with simpler callbacks
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, MQTT_CLIENT_ID)

    # 2. Security Setup
    # TLS is required for HiveMQ Cloud connections
    client.tls_set()
    client.username_pw_set(MQTT_USERNAME, MQTT_PW)

    # 3. Attach Callbacks
    client.on_connect = on_connect
    client.on_publish = on_publish

    try: 
        # Connect to the broker
        client.connect(MQTT_URL, MQTT_PORT, 60)
        
        # Start the background thread (network loop) to handle sending/receiving automatically
        client.loop_start()
        return client
    except Exception as e:
        print(f"MQTT CONNECTION ERROR: {e}")
        sys.exit()

def main():
    """
    Main execution loop:
    1. Reads raw data from Serial (USB).
    2. Parses it to ensure it is valid JSON.
    3. Prints it to the console.
    4. Publishes it to the MQTT Cloud.
    """
    serial_instance = connect_serial()
    mqtt_instance = connect_mqtt()

    print("Gateway is running...")

    while True:
        # Check if there are bytes waiting in the serial buffer
        if serial_instance.in_waiting > 0:
            
            # Read line, decode bytes to string, and remove whitespace
            raw_data = serial_instance.readline().decode("utf-8", errors="ignore").strip()

            # Skip loop if the line is empty
            if not raw_data:
                continue

            try: 
                # Parse JSON (Validation Step)
                # We load it into a dict to ensure it's not corrupted data
                clean_data = json.loads(raw_data)
                
                # Print local status
                print("\n--- NEW MESSAGE RECEIVED ---")
                print(f"Device:      {clean_data.get('device_id', 'Unknown')}")
                print(f"Temperature: {clean_data.get('temperature')} °C")
                print(f"Humidity:    {clean_data.get('humidity')} %")

                # Publish the raw string to the cloud topic
                mqtt_instance.publish(MQTT_TOPIC, raw_data)

            except json.JSONDecodeError:
                # Handle cases where Arduino sends incomplete lines (e.g. during startup)
                print(f"Warning: Received non-JSON data: {raw_data}")

if __name__ == "__main__":
    main()