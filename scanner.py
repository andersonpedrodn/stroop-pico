import machine
import time

print("--- INICIANDO ESCANEAMENTO I2C ---")

# Lista de pares de pinos comuns na BitDogLab e Raspberry Pico
# Formato: (id_i2c, sda, scl)
combinacoes = [
    (1, 14, 15), # Padrão BitDogLab (SDA=14, SCL=15)
    (0, 4, 5),   # Padrão alternativo (SDA=4, SCL=5)
    (0, 0, 1),   # Padrão Pico (SDA=0, SCL=1)
    (1, 2, 3),   # Outro padrão Pico (SDA=2, SCL=3)
    (1, 26, 27)  # Às vezes usado em displays externos
]

encontrou_algo = False

for id_i2c, sda_pin, scl_pin in combinacoes:
    print(f"\nTestando I2C{id_i2c} | SDA: {sda_pin} | SCL: {scl_pin} ...")
    
    try:
        # Tenta inicializar o barramento I2C
        i2c = machine.I2C(id_i2c, sda=machine.Pin(sda_pin), scl=machine.Pin(scl_pin), freq=100000)
        
        # Escaneia endereços
        dispositivos = i2c.scan()
        
        if dispositivos:
            print(f"   ✅ SUCESSO! Encontrado {len(dispositivos)} dispositivo(s)!")
            for dispositivo in dispositivos:
                print(f"      -> Endereço Decimal: {dispositivo} | Hex: {hex(dispositivo)}")
                encontrou_algo = True
                
                # Se achou o display (endereço padrão é 60 ou 0x3c), tenta limpar a tela
                if dispositivo == 60: 
                    try:
                        import ssd1306
                        oled = ssd1306.SSD1306_I2C(128, 64, i2c)
                        oled.fill(0) # Limpa (pinta de preto)
                        oled.text("ACHEI!", 30, 30)
                        oled.show()
                        print("      -> Tentei limpar a tela. O chuvisco sumiu?")
                    except ImportError:
                        print("      -> (Biblioteca ssd1306 não encontrada para teste visual)")
        else:
            print("   ❌ Nenhum dispositivo respondeu.")
            
    except Exception as e:
        print(f"   ⚠️ Erro ao configurar pinos: {e}")

print("\n--- FIM DO ESCANEAMENTO ---")