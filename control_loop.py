import time
import json
from datetime import datetime
import RPi.GPIO as GPIO 
from pipyadc import ADS1256
from pipyadc.ADS1256_definitions import *
import waveshare_config


# diferencial entre canal 1 e 0
ADC_DIFF = POS_AIN1 | POS_AIN0 

GPIO.setmode(GPIO.BCM)
INPUT_PINS = [21, 20, 6, 5]
[GPIO.setup(pin, GPIO.IN) for pin in INPUT_PINS]

CH_ADDR_PINS = [16, 13, 19, 26]
[GPIO.setup(pin, GPIO.IN) for pin in CH_ADDR_PINS]

SAIDAS = {
  "MODO": 21, # 0 = AUTO, 1 = MANUAL
  "CICLO_CANAL": 20,
  "GRAVACAO": 6,
  "EXECUTA_LEITURA": 5
}

# inicializa ADC
ads = ADS1256(waveshare_config)
ads.drate = DRATE_30000
#ads.drate = DRATE_2000
#ads.drate = DRATE_15

def append_to_data(obj):
  with open("data.txt", "a") as myfile:
    myfile.write(json.dumps(obj)+'\n')

def leitura_adc():
  # Gain and offset self-calibration can be triggered at any time
  ads.cal_self()
  # Returns list of integers, one result for each configured channel
  raw_channels = ads.read_sequence((ADC_DIFF,))
  #raw_channels = ads.read_continue(CH_SEQUENCE)
  # Text-mode output
  voltages = [i * ads.v_per_digit for i in raw_channels]
  print(voltages[0])


def modo_automatico(pin):
  if not GPIO.input(pin):
    print('modo automatico')
  else:
    print('modo manual')
  append_to_data({"modoAuto": GPIO.input(pin)})
GPIO.add_event_detect(SAIDAS["MODO"], GPIO.BOTH, bouncetime=20)
GPIO.add_event_callback(SAIDAS["MODO"], modo_automatico)


def gravacao(pin):
  if GPIO.input(pin):
    print('grava')
  else:
    print('nao grava')
  append_to_data({"gravacaoDeDados": GPIO.input(pin)})

GPIO.add_event_detect(SAIDAS["GRAVACAO"], GPIO.BOTH, bouncetime=20)
GPIO.add_event_callback(SAIDAS["GRAVACAO"], gravacao)



def ciclo_canal(pin):
  bits_canais_ativos = [GPIO.input(x) for x in CH_ADDR_PINS]
  addr = 0x00
  #print(bits_canais_ativos)
  for i, x in enumerate(bits_canais_ativos):
    if x:
      addr = addr | (0x01 << i)
  
  if GPIO.input(pin):
    print('\n')
    print('ciclo_canal prepara')
    print(f'Estamos no canal: {addr}')
    # notamos que se a chave auto/manual for alterada ao mesmo tempo que o pulso do canal é enviado,
    # a status do modo auto/manual é detectado errado. 
    # Como solução, esperamos um tempo e conferimos a saída do modo auto/manual    
    time.sleep(0.05)
    append_to_data({"activeChannelId": f"ch{addr}", "modoAuto": GPIO.input(SAIDAS["MODO"])})
  else:
    print('ciclo_canal ativa')
    print(f'Vamos realizar a leitura do canal {addr}...')



GPIO.add_event_detect(SAIDAS["CICLO_CANAL"], GPIO.BOTH, bouncetime=20)
GPIO.add_event_callback(SAIDAS["CICLO_CANAL"], ciclo_canal)


def executa_leitura(pin):
  bits_canais_ativos = [GPIO.input(x) for x in CH_ADDR_PINS]
  addr = 0x00
  #print(bits_canais_ativos)
  for i, x in enumerate(bits_canais_ativos):
    if x:
      addr = addr | (0x01 << i)
  print(f"leitura do canal: {addr}")
  leitura_adc()

    
GPIO.add_event_detect(SAIDAS["EXECUTA_LEITURA"], GPIO.RISING, bouncetime=20)
GPIO.add_event_callback(SAIDAS["EXECUTA_LEITURA"], executa_leitura)


def main():
  prev_output = []
  while True:
    time.sleep(1)

if __name__ == '__main__':
  main()
