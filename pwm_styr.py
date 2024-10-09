import numpy as np
import matplotlib.pyplot as plt
import scipy
import scipy.signal
from gpiozero import LED
import time

fs = 5000  # Samplingsfrekvens i Hz
f = 50  # Frekvens i Hz
t = np.linspace(0, (1/f), fs)  # 0.02 s 
sinus = np.sin(2 * np.pi * f * t)
pause_timer = fs / (1/f)
f_saw = f*5 # Sawtooth Hz
sawtooth = scipy.signal.sawtooth(2 * np.pi * f_saw * t)

square_wave = []
for i in range(len(sinus)):
    if sinus[i] > sawtooth[i]:
        square_wave.append(1)
    else:
        square_wave.append(0)

def display_plots():
    fig, ax = plt.subplots(2, 2)
    ax[0][0].plot(t, sinus, color='blue')
    ax[0][1].plot(t, sawtooth, color='red')
    ax[1][0].plot(t, square_wave, color='green')
    ax[1][1].plot(t, sinus, color='blue')
    ax[1][1].plot(t, sawtooth, color='red')
    ax[1][1].plot(t, square_wave, color='green')
    fig.savefig('theoretic_waves.pdf')
    plt.show()
    
start_time = time.time()
pwm_pin = LED(12)
while time.time() - start_time < 120: 
    #for j in range(20):
    for i in range(len(square_wave)):
        if square_wave[i] == 1:
            pwm_pin.on()
            #time.sleep((1/f) / fs)
        else:
            pwm_pin.off()
            #time.sleep((1/f) / fs)

# Debug
#display_plots()