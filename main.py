import machine
import neopixel
import time
import random
import ssd1306

# --- CONFIGURAÇÕES DO JOGO ---
TEMPO_TOTAL_JOGO = 30  # Segundos que a partida dura
TEMPO_RODADA_MAX = 2.0 # Segundos para responder cada cor (reduzido para ser ágil)
BRILHO_MAX = 5         # Intensidade dos LEDs

# --- HARDWARE ---
PINO_BUZZER_A = 21
PINO_BUZZER_B = 10 
PINO_MATRIZ = 7
NUM_LEDS_MATRIZ = 25
PINO_LED_PLACA = 12 
NUM_LEDS_PLACA = 1
I2C_SDA = 14
I2C_SCL = 15

# Botões
PINO_BOTAO_A = 5 # Esquerda (Diferente)
PINO_BOTAO_B = 6 # Direita (Igual)

# --- INICIALIZAÇÃO ---
np_matriz = neopixel.NeoPixel(machine.Pin(PINO_MATRIZ), NUM_LEDS_MATRIZ)
botao_a = machine.Pin(PINO_BOTAO_A, machine.Pin.IN, machine.Pin.PULL_UP)
botao_b = machine.Pin(PINO_BOTAO_B, machine.Pin.IN, machine.Pin.PULL_UP)
i2c = machine.I2C(1, sda=machine.Pin(I2C_SDA), scl=machine.Pin(I2C_SCL), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# --- CORES ---
def cor_ajustada(r, g, b):
    fator = BRILHO_MAX / 255
    return (int(r * fator), int(g * fator), int(b * fator))

LISTA_CORES = [
    {"nome": "ROSA",   "rgb": cor_ajustada(255, 0, 100)},
    {"nome": "BRANCA", "rgb": cor_ajustada(255, 255, 255)},
    {"nome": "VERDE",  "rgb": cor_ajustada(0, 255, 0)},
    {"nome": "AZUL",   "rgb": cor_ajustada(0, 0, 255)}
]

# --- UTILITÁRIOS ---
def obter_pixel_index(x, y):
    if y % 2 == 0:
        return y * 5 + x
    else:
        return y * 5 + (4 - x)

def silenciar_tudo():
    buzzer_a = machine.PWM(machine.Pin(PINO_BUZZER_A))
    buzzer_a.duty_u16(0)
    buzzer_b = machine.PWM(machine.Pin(PINO_BUZZER_B))
    buzzer_b.duty_u16(0)
    np_placa = neopixel.NeoPixel(machine.Pin(PINO_LED_PLACA), NUM_LEDS_PLACA)
    np_placa[0] = (0, 0, 0)
    np_placa.write()
    return buzzer_a

buzzer_ativo = silenciar_tudo()

def tocar_som(frequencia, duracao):
    if frequencia > 0:
        buzzer_ativo.freq(frequencia)
        buzzer_ativo.duty_u16(32768) 
    time.sleep(duracao)
    buzzer_ativo.duty_u16(0)

# --- VISUAIS ---
def animacao_tetris():
    for i in range(NUM_LEDS_MATRIZ): np_matriz[i] = (0,0,0)
    np_matriz.write()
    cor_tetris = cor_ajustada(255, 100, 0)
    
    for coluna in range(5):
        altura_final = random.randint(1, 5)
        for y in range(4, 4 - altura_final, -1):
             idx = obter_pixel_index(coluna, y)
             np_matriz[idx] = cor_tetris
             np_matriz.write()
             time.sleep(0.04)
             if y > (5 - altura_final):
                 np_matriz[idx] = (0,0,0)
        for y in range(altura_final):
            idx = obter_pixel_index(coluna, y)
            np_matriz[idx] = cor_tetris
        np_matriz.write()
        tocar_som(100 + (coluna * 100), 0.05)
    time.sleep(0.5)
    for i in range(NUM_LEDS_MATRIZ):
        np_matriz[i] = (0,0,0)
        np_matriz.write()
        time.sleep(0.01)

def introducao():
    oled.fill(0)
    oled.text("INICIANDO", 25, 20)
    oled.text("STROOP...", 30, 35)
    oled.show()
    tocar_som(600, 0.1)
    tocar_som(800, 0.1)
    tocar_som(1200, 0.2)
    animacao_tetris()

def mostrar_tela_jogo(texto, tempo_restante):
    oled.fill(0)
    # Mostra tempo no canto superior
    oled.text(f"T: {int(tempo_restante)}s", 0, 0)
    
    # Instruções rápidas
    oled.text("A:DIF  B:IGUAL", 10, 55)
    
    # Palavra centralizada
    largura = len(texto) * 8
    oled.text(texto, (128 - largura) // 2, 25)
    oled.show()

def mostrar_placar(acertos, erros):
    oled.fill(0)
    oled.text("FIM DE JOGO!", 15, 5)
    oled.text(f"ACERTOS: {acertos}", 15, 25)
    oled.text(f"ERROS:   {erros}", 15, 35)
    
    saldo = acertos - erros
    msg_final = "BOM!" if saldo > 5 else "TENTE DNV"
    oled.text(msg_final, 30, 55)
    oled.show()
    
    # Som final
    if saldo > 0:
        tocar_som(1000, 0.1); tocar_som(1500, 0.1); tocar_som(2000, 0.2)
    else:
        tocar_som(300, 0.3); tocar_som(150, 0.5)

# --- LOOP PRINCIPAL DO JOGO ---
silenciar_tudo()
introducao()

while True: # Loop para reiniciar o jogo quando acabar
    acertos = 0
    erros = 0
    inicio_jogo = time.time()
    
    # Contagem regressiva visual na matriz
    for i in range(3, 0, -1):
        oled.fill(0)
        oled.text(f"COMECA EM {i}", 20, 30)
        oled.show()
        tocar_som(500, 0.1)
        time.sleep(0.9)
    
    # --- PARTIDA VALENDO ---
    while True:
        tempo_decorrido = time.time() - inicio_jogo
        tempo_restante = TEMPO_TOTAL_JOGO - tempo_decorrido
        
        # Verifica se o tempo acabou
        if tempo_restante <= 0:
            break
            
        # 1. Sorteio da Rodada
        cor_real = random.choice(LISTA_CORES)
        if random.random() < 0.5:
            texto_mostrado = cor_real           # CASO IGUAL
            resposta_correta = "B"              # Botão B (Igual)
        else:
            texto_mostrado = random.choice(LISTA_CORES) # CASO DIFERENTE
            while texto_mostrado["nome"] == cor_real["nome"]:
                texto_mostrado = random.choice(LISTA_CORES)
            resposta_correta = "A"              # Botão A (Diferente)

        # 2. Atualiza Hardware
        # Matriz
        for i in range(NUM_LEDS_MATRIZ): np_matriz[i] = cor_real["rgb"]
        np_matriz.write()
        # Display
        mostrar_tela_jogo(texto_mostrado["nome"], tempo_restante)

        # 3. Aguarda Resposta
        inicio_rodada = time.ticks_ms()
        acao_usuario = None
        
        while time.ticks_diff(time.ticks_ms(), inicio_rodada) < (TEMPO_RODADA_MAX * 1000):
            if botao_b.value() == 0:
                acao_usuario = "B"
                break
            if botao_a.value() == 0:
                acao_usuario = "A"
                break
            time.sleep(0.01)

        # 4. Verifica Resultado
        if acao_usuario == resposta_correta:
            acertos += 1
            tocar_som(2000, 0.05) # Som Feliz
        else:
            erros += 1
            tocar_som(100, 0.2)   # Som Triste
            # Feedback visual de erro rápido
            oled.fill(0)
            oled.text("X", 60, 25)
            oled.show()
            time.sleep(0.2)

        # Pequeno intervalo para soltar o botão
        for i in range(NUM_LEDS_MATRIZ): np_matriz[i] = (0,0,0)
        np_matriz.write()
        time.sleep(0.2)

    # --- FIM DA PARTIDA ---
    # Apaga tudo
    for i in range(NUM_LEDS_MATRIZ): np_matriz[i] = (0,0,0)
    np_matriz.write()
    
    mostrar_placar(acertos, erros)
    
    # Espera apertar qualquer botão para jogar de novo
    time.sleep(2) # Trava forçada para ler o placar
    oled.text("Aperte p/ reiniciar", 0, 0)
    oled.show()
    
    while botao_a.value() == 1 and botao_b.value() == 1:
        time.sleep(0.1)