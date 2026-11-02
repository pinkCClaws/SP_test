import network
import time
from umqtt.simple import MQTTClient
import machine
import ubinascii

class ConexionMQTT:
    def __init__(self, ssid, password, modelo):
        self.ssid = ssid
        self.password = password
        self.modelo = modelo
        self.server = 'test.mosquitto.org'
        self.client_id = ubinascii.hexlify(machine.unique_id())
        self.client = MQTTClient(self.client_id, self.server)

    def conectar_wifi(self):
        print("Limpiando estado y conectando a WiFi", end="")
        sta_if = network.WLAN(network.STA_IF)
        
        # 1. Forzar limpieza del estado interno del WiFi
        if sta_if.active():
            sta_if.disconnect()
            sta_if.active(False)
            time.sleep(0.5)
            
        sta_if.active(True)
        
        # 2. Conectar (manejando redes abiertas vs con contraseña)
        if self.password == "":
            sta_if.connect(self.ssid)
        else:
            sta_if.connect(self.ssid, self.password)
            
        # 3. Esperar conexión
        while not sta_if.isconnected():
            print(".", end="")
            time.sleep(0.5)
        print("\n¡WiFi Conectado! IP:", sta_if.ifconfig()[0])

    def callback_recepcion(self, topic, msg):
        # Esta función decodifica lo que llega del celular
        tema = topic.decode('utf-8')
        mensaje = msg.decode('utf-8')
        
        if tema == 'casa/relevador':
            self.modelo.rele_encendido = int(mensaje)
        elif tema == 'casa/servo':
            self.modelo.servo_angulo = int(mensaje)
        elif tema == 'casa/bocina':
            self.modelo.bocina_encendida = int(mensaje)

    def iniciar_mqtt(self):
        self.client.set_callback(self.callback_recepcion)
        self.client.connect()
        # Suscripciones a los actuadores
        self.client.subscribe(b"casa/relevador")
        self.client.subscribe(b"casa/servo")
        self.client.subscribe(b"casa/bocina")
        print("¡Conectado a MQTT y suscrito a tópicos!")

    def revisar_mensajes(self):
        # check_msg() no bloquea el ESP32, permite seguir leyendo sensores
        self.client.check_msg()

    def publicar(self, topico, mensaje):
        self.client.publish(topico.encode('utf-8'), mensaje.encode('utf-8'))