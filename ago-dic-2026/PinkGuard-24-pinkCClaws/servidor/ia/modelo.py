class Modelo:
    def __init__(self):
        # Estados para enviar a MQTT (Sensores)
        self.pir_estado = -1
        self.rf_estado = -1
        self.ldr_estado = ""

        # Estados recibidos de MQTT (Actuadores)
        self.servo_angulo = 0
        self.rele_encendido = 0
        self.bocina_encendida = 0