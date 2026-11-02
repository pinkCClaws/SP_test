from hal import Hal
from modelo import Modelo
from vista import Vista
from conexion_mqtt import ConexionMQTT
import time

# --- CONFIGURA TU RED WIFI AQUÍ ---
WIFI_SSID = "Alumnos-TecNM-D-UF"
WIFI_PASS = ""

def main():
    hal = Hal()
    modelo = Modelo()
    vista = Vista(hal)
    
    # Iniciar Red y MQTT
    mqtt = ConexionMQTT(WIFI_SSID, WIFI_PASS, modelo)
    mqtt.conectar_wifi()
    mqtt.iniciar_mqtt()
    
    print("Iniciando bucle de control independiente...")
    
    while True:
        # 1. Leer MQTT (revisa si el celular envió comandos a los actuadores)
        mqtt.revisar_mensajes()
        
        # 2. Actualizar hardware (Actuadores) según lo que dictó MQTT
        vista.actualizar_actuadores(modelo)
        
        # 3. Leer Sensores físicos
        lectura_pir = hal.leer_pir()
        lectura_rf = hal.leer_rf()
        lectura_ldr = hal.leer_ldr()
        
        # 4. Publicar en MQTT solo si el valor del sensor cambió
        if lectura_pir != modelo.pir_estado:
            modelo.pir_estado = lectura_pir
            mensaje_pir = "SI" if lectura_pir == 1 else "NO"
            mqtt.publicar("casa/pir", mensaje_pir)
            
        if lectura_rf != modelo.rf_estado:
            modelo.rf_estado = lectura_rf
            mensaje_rf = "VIVO" if lectura_rf == 1 else "MUERTO"
            mqtt.publicar("casa/rf", mensaje_rf)
            
        if lectura_ldr != modelo.ldr_estado:
            modelo.ldr_estado = lectura_ldr
            mqtt.publicar("casa/ldr", lectura_ldr)
            
        # Pequeña pausa para no saturar el servidor MQTT público
        time.sleep(0.1)

if __name__ == "__main__":
    main()