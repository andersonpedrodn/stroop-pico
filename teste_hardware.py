import machine
import neopixel
import time
import ssd1306

# --- Configurações da BitDogLab v6.3 ---
PINO_MATRIZ = 7
NUM_LEDS = 25
I2C_SDA = 14
I2C_SCL = 15

# 1. TENTATIVA DA MATRIZ (Vamos fazer isso PRIMEIRO)
print("1. Testando Matriz de LEDs...")
try:
    np = neopixel.NeoPixel(machine.Pin(PINO_MATRIZ), NUM_LEDS)
    # Acende os 5 primeiros LEDs de VERDE
    for i in range(5):
        np[i] = (0, 50, 0) 
    np.write()
    print("   -> Matriz deve estar com 5 luzes verdes agora.")
except Exception as e:
    print("   -> ERRO na Matriz:", e)

time.sleep(1)

# 2. TENTATIVA DO DISPLAY
print("2. Testando Display OLED...")
try:
    # Usando frequência menor (100000) para garantir estabilidade
    i2c = machine.I2C(1, sda=machine.Pin(I2C_SDA), scl=machine.Pin(I2C_SCL), freq=100000)
    
    # Verifica se o display responde
    devices = i2c.scan()
    if devices:
        print(f"   -> Display encontrado no endereço: {hex(devices[0])}")
        
        oled = ssd1306.SSD1306_I2C(128, 64, i2c)
        oled.fill(0) # Limpa a estática (pinta de preto)
        oled.text("FUNCIONOU!", 20, 30)
        oled.show()
        print("   -> Tela deve estar preta com texto escrito.")
    else:
        print("   -> NENHUM dispositivo I2C encontrado. Verifique conexões.")

except Exception as e:
    print("   -> ERRO no Display:", e)

# Pisca a matriz para mostrar que o código chegou ao fim
while True:
    np[0] = (0, 0, 50) # Azul piscando no primeiro LED
    np.write()
    time.sleep(0.5)
    np[0] = (0, 0, 0)
    np.write()
    time.sleep(0.5)