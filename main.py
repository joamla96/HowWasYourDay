from time import sleep
import paho.mqtt.client as mqtt
from gpiozero import LED, Button
from signal import pause

print("Initializing...")

mqttc = mqtt.Client()
mqttc.username_pw_set(username="DAeAD91yDJJrGk9TyQPyTr2rXcfrxQf0fjoIid6KMDZiNZ0aDFykWqBHqGZNl4Cq", password="")

mqttc.connect("mqtt.flespi.io", 8883)

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
    mqttc.publish("test", value)
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