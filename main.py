from time import sleep
import paho.mqtt.client as mqtt
from gpiozero import LED, Button
from signal import pause
from mcpi import minecraft, block, event

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
    sleep(0.1)
sleep(0.3)

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

mc = minecraft.Minecraft.create()

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

    msg = str(message.payload.decode("utf-8"))
    pos = mc.player.getPos()

    if msg == "0":
      ledRed.on()
      mc.setBlocks(pos.x-1, pos.y-1, pos.z-1, pos.x+1, pos.y+2, pos.z+1, block.TNT.id, 1)
      sleep(0.5)
      ledRed.off()

    if msg == "1":
        ledYellow.on()
        mc.player.setPos(pos.x, pos.y+10, pos.z)
        sleep(0.5)
        ledYellow.off()

    if msg == "2":
        ledGreen.on()
        sleep(0.5)
        ledGreen.off()

    if msg == "3":
        ledBlue.on()
        sleep(0.5)
        ledBlue.off()


mqttc.on_message = on_message
mqttc.subscribe("pi/buttons")

print("Minecraft Ready")
print("Ready")

for led in leds:
    led.off()

mqttc.loop_forever()