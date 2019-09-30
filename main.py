from time import sleep
import paho.mqtt.client as mqtt
from gpiozero import LED, Button
from signal import pause

print("Initializing...")

# This happens when connecting
def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))

# Getting a message from subscribe
def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

# When something is published
def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))

# On subscribing to messages
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# Taking care of logging
def on_log(mqttc, obj, level, string):
    print(string)

mqttc = mqtt.Client("Pi")
mqttc.username_pw_set(username="DAeAD91yDJJrGk9TyQPyTr2rXcfrxQf0fjoIid6KMDZiNZ0aDFykWqBHqGZNl4Cq", password="")

mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
mqttc.on_log = on_log

mqttc.connect("mqtt.flespi.io", 1883)

ledRed = LED(18)
ledYellow = LED(19)
ledGreen = LED(20)
ledBlue = LED(21)

btnRed = Button(17)
btnYellow = Button(16)
btnGreen = Button(13)
btnBlue = Button(12)

leds = [ ledRed, ledYellow, ledGreen, ledBlue ]

for led in leds:
    led.on()
    sleep(0.2)
    led.off()

def buttonPressed(led, value):
    print("Button Clicked, publishing " + str(value))
    mqttc.publish("test/review", value, 0)
    led.on()

btnRed.when_pressed = lambda: buttonPressed(ledRed, 0)
btnRed.when_released = ledRed.off

btnYellow.when_pressed = lambda : buttonPressed(ledYellow, 1)
btnYellow.when_released = ledYellow.off

btnGreen.when_pressed = lambda : buttonPressed(ledGreen, 2)
btnGreen.when_released = ledGreen.off

btnBlue.when_pressed = lambda : buttonPressed(ledBlue, 3)
btnBlue.when_released = ledBlue.off

for led in leds:
    led.on()

sleep(1)

for led in leds:
    led.off()

print("READY")

mqttc.loop_forever()