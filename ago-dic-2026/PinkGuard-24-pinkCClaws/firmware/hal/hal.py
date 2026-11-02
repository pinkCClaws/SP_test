from machine import Pin, PWM, ADC
import time
from dfplayer import DFPlayer

class Hal:
    def __init__(self, pin_servo=26, pin_pir=27, pin_ldr=32, pin_rf=14, pin_rele=25, tx_df=17, rx_df=16):
        # Servomotor
        self.servo = PWM(Pin(pin_servo), freq=50)
        self.mover_servo(0)
        
        # Sensores (Entradas)
        self.pir = Pin(pin_pir, Pin.IN)
        self.adc_ldr = ADC(Pin(pin_ldr))
        self.adc_ldr.atten(ADC.ATTN_11DB)
        self.rf_btn = Pin(pin_rf, Pin.IN, Pin.PULL_DOWN)
        
        # Relevador (Salida, Active LOW)
        self.rele = Pin(pin_rele, Pin.OUT)
        self.rele.value(1) # Apagado inicial
        
        # DFPlayer Mini (Configurado con pines 17 y 16)
        self.df = DFPlayer(uart_id=1, tx_pin_id=tx_df, rx_pin_id=rx_df)
        time.sleep(0.5)
        self.df.volume(25)

    def mover_servo(self, angulo):
        min_duty = 40
        max_duty = 115
        duty = int(min_duty + (angulo / 180) * (max_duty - min_duty))
        self.servo.duty(duty)

    def activar_rele(self, estado):
        self.rele.value(0 if int(estado) == 1 else 1)

    def df_control(self, estado):
        if int(estado) == 1:
            # Reproduce carpeta 01, archivo 001.mp3
            self.df.play(1, 1)

    def df_ajustar_volumen(self, volumen):
        self.df.volume(volumen)

    def leer_pir(self):
        return self.pir.value()

    def leer_rf(self):
        return self.rf_btn.value()

    def leer_ldr(self):
        return "NOCHE" if self.adc_ldr.read() > 2000 else "DIA"