#Importa las librerias
import RPi.GPIO as GPIO
import time
from Adafruit_IO import Client, Feed

#Define los puertos en Base a los GPIOS
GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24
LED = 17
 
 
print ("Distance Measurement In Progress")
#Inicializa los Puertos
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(LED,GPIO.OUT)

#Apaga el Trigger
GPIO.output(TRIG, False)
print ("Waiting For Sensor To Settle")

READ_TIMEOUT = 5

#Introduce tus datos de cuenta
ADAFRUIT_IO_KEY = "aio_SxLr54GsCf9mQ9XTAGt370X5IZN2"
ADAFRUIT_IO_USERNAME = "DR424"
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

#Obtener feeds
feed1 = aio.feeds('ultrasonico')
feed2 = aio.feeds('led')

#Sensar Distancia
def distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    while GPIO.input(ECHO)==0:
        pulse_start = time.time()
    while GPIO.input(ECHO)==1:
        pulse_end = time.time() 
 
    pulse_duration = pulse_end - pulse_start   
 
    distance = round((pulse_duration * 17150), 2)

    print ("Distance:",distance,"cm")
    return distance

#Correr
if True:
    try:
        while True:
            dist = distance()
            time.sleep(0.5)
            #Enviar y Recibir de los feeds
            aio.send(feed1.key, str(dist))
            data = aio.receive(feed2.key)
            if int(data.value) == 1:
                print('ON/n')
            elif int(data.value) == 0:
                print('OFF/n')
            GPIO.output(LED, bool(data.value))
    except KeyboardInterrupt:
        print("The End")
        GPIO.cleanup() 
