from time import sleep
import paho.mqtt.client as mqtt
from gpiozero import LED, Button
from signal import pause

print("Initializing...")

print("Connecting MQTT")
mqttc = mqtt.Client("Pi")
mqttc.username_pw_set(username="DAeAD91yDJJrGk9TyQPyTr2rXcfrxQf0fjoIid6KMDZiNZ0aDFykWqBHqGZNl4Cq", password="")

mqttc.connect("mqtt.flespi.io", 1883)

print("Setting up LEDs and Buttons")
ledRed = LED(18)
ledYellow = LED(19)
ledGreen = LED(20)
ledBlue = LED(21)

btnRed = Button(17)
btnYellow = Button(16)
btnGreen = Button(13)
btnBlue = Button(12)

leds = [ ledRed, ledYellow, ledGreen, ledBlue ]

print("Checking LEDs")
for led in leds:
    led.on()
    sleep(0.2)
    led.off()

print("Defining Button's Behavior")
def buttonPressed(value):
    print("Button Clicked, publishing " + str(value))
    mqttc.publish("pi/buttons", value, 0)

btnRed.when_pressed = lambda: buttonPressed(0)
btnYellow.when_pressed = lambda : buttonPressed(1)
btnGreen.when_pressed = lambda : buttonPressed(2)
btnBlue.when_pressed = lambda : buttonPressed(3)

print("Pi Ready")

print("Setting up minecraft environment")
def on_mqtt_message(input):
    print(input)

mqttc.subscribe("pi/buttons")

mqttc.loop_forever()