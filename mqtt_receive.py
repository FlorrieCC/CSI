import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("✅ Connected with result code " + str(rc))
    client.subscribe("/esp32/csi")

def on_message(client, userdata, msg):
    decoded = msg.payload.decode()
    print(f"[CSI] {decoded}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.3.3", 1883)
print("📡 Listening for CSI data...")
client.loop_forever()
