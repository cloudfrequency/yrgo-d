import numpy as np
import matplotlib.pyplot as plt
import scipy
import scipy.signal
from gpiozero import LED

fs = 5000  # Samplingsfrekvens i Hz
t = np.linspace(0, 0.02, fs)  # 1 s 

f = 50  # Frekvens i Hz
sinus = np.sin(2 * np.pi * f * t)

f_saw = 250 # Sawtooth Hz
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
    

pwm_pin = LED(12)
for j in range(20):
    for i in range(len(square_wave)):
        if square_wave[i] == 1:
            pwm_pin.on()
        else:
            pwm_pin.off()

display_plots()