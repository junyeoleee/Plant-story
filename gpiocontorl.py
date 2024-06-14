#gpiotest
import RPi.GPIO as g
import time
g.setwarnings(False)
g.setmode(g.BCM)
Motor1 = 20
Motor2 = 21
LED =26
water1 = 19
water2= 21
g.setup(LED, g.OUT)

def motorcontorl(t):
    g.setup(Motor1,g.OUT)
    motor_pwm = g.PWM(Motor1,21)
    g.output(Motor1,False)
    time.sleep(t)
    g.output(Motor1,True)

def LEDon():
    g.output(LED,False)

def LEDoff():
    g.output(LED,True)
    


