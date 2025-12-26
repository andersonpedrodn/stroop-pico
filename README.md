# 🧠 Stroop Test - BitDogLab Edition

![MicroPython](https://img.shields.io/badge/MicroPython-blue?logo=python&logoColor=white)
![Hardware](https://img.shields.io/badge/Hardware-BitDogLab-green)
![Status](https://img.shields.io/badge/Status-Completed-success)

> **"Uma fusão entre Neuropsicologia Cognitiva e Sistemas Embarcados."**

## 📖 Sobre o Projeto

Este projeto é uma implementação física e gamificada do **Teste de Stroop**, uma ferramenta clássica da psicologia utilizada para avaliar a atenção seletiva, o controle inibitório e a velocidade de processamento cognitivo.

O objetivo foi transpor um teste clínico tradicionalmente feito em papel ou computador para um **sistema embarcado**, utilizando a placa de desenvolvimento educacional **BitDogLab** (baseada no Raspberry Pi Pico/RP2040).

### 🎯 O Desafio Cognitivo
O usuário é confrontado com um conflito sensorial:
1.  A **Matriz de LEDs** exibe uma cor (ex: Vermelho).
2.  O **Display OLED** exibe o nome de uma cor (ex: "AZUL").
3.  O jogador deve decidir rapidamente se a **cor da luz** corresponde ao **texto escrito**.

---

## 🛠️ Hardware Utilizado

* **Microcontrolador:** Raspberry Pi Pico (RP2040).
* **Placa de Desenvolvimento:** BitDogLab v6.3.
* **Display:** OLED 0.96" I2C (SSD1306).
* **Visual:** Matriz de LEDs 5x5 endereçáveis (WS2812B/Neopixel).
* **Áudio:** Buzzer passivo (PWM).
* **Input:** Botões táteis (A e B).

## ✨ Funcionalidades

* **Intro Animada:** Sequência de inicialização com animação estilo "Tetris" na matriz de LEDs e música chiptune.
* **Modo Time Attack:** Partidas cronometradas de 30 segundos.
* **Feedback Sensorial:**
    * ✅ **Acerto:** Som agudo curto + Pontuação.
    * ❌ **Erro:** Som grave + Feedback visual no display.
* **Mecânica de Jogo:**
    * Botão **B (Direita)**: Confirma que Cor e Texto são **IGUAIS**.
    * Botão **A (Esquerda)**: Confirma que Cor e Texto são **DIFERENTES**.
* **Placar Final:** Exibe total de acertos, erros e avaliação de desempenho.

---

## 🚀 Como Executar

### Pré-requisitos
* Placa Raspberry Pi Pico com firmware **MicroPython** instalado.
* VS Code com extensão **MicroPico** (ou Thonny IDE).

### Instalação
1.  Clone este repositório:
    ```bash
    git clone [https://github.com/andersonpedrodn/stroop-pico.git](https://github.com/andersonpedrodn/stroop-pico.git)
    ```
2.  Conecte a placa via USB.
3.  Envie o arquivo de driver do display (`ssd1306.py`) para a raiz da placa.
4.  Abra o arquivo `main.py` e envie para a placa (ou salve como `main.py` na raiz para execução automática ao ligar).

---

## 🕹️ Controles

| Botão | Função |
| :--- | :--- |
| **Botão A (GPIO 5)** | Indica que a cor e o texto são **DIFERENTES**. |
| **Botão B (GPIO 6)** | Indica que a cor e o texto são **IGUAIS**. |

---

## 🧠 Background do Autor

Desenvolvido por **Anderson Pedro**.
* 🎓 Estudante de Tecnologia da Informação (UFRN).
* 🧠 Psicólogo em transição de carreira para a área Tech.

Este projeto faz parte dos meus estudos em **Sistemas Embarcados**, buscando aplicar conceitos de psicologia em interfaces tangíveis e IoT.

---


https://github.com/user-attachments/assets/47353fc3-117a-41c6-b29b-cf5586e028b3



*Desenvolvido em Dezembro de 2025.*
