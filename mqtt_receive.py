import paho.mqtt.client as mqtt
from motion_detector import MotionDetector

motion = MotionDetector(window_size=30, threshold=5.0)

def on_connect(client, userdata, flags, rc):
    print("✅ Connected with result code " + str(rc))
    client.subscribe("/esp32/csi")

def on_message(client, userdata, msg):
    decoded = msg.payload.decode()
    print(f"[CSI] {decoded}")
    result = motion.update(decoded)
    print("result:", result)
    if result is not None:
        print("🚨 Motion Detected!" if result else "🟢 No Motion")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883)
print("📡 Listening for CSI data...")
client.loop_forever()
