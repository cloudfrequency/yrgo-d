import numpy as np
import matplotlib.pyplot as plt
import scipy
import scipy.signal
from gpiozero import LED
import time

# Change 
fs = 5000  # Number of samples to take
f = 50  # Base frequency of sinus
f_saw = f*20 # Sawtooth Hz, change multiplier to test new frequencies
t = np.linspace(0, (1/f), fs)  
sinus = np.sin(2 * np.pi * f * t)
pause_timer = fs / (1/f)

sawtooth = scipy.signal.sawtooth(2 * np.pi * f_saw * t)

# Square wave created from sinus and sawtooth wave
square_wave = []
for i in range(len(sinus)):
    if sinus[i] > sawtooth[i]:
        square_wave.append(1)
    else:
        square_wave.append(0)

# Plots the created graphs for easier analysis
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

# Run the PWM for 60 seconds, then stop
start_time = time.time()
pwm_pin = LED(12)
while time.time() - start_time < 60: 
    #for j in range(20):
    for i in range(len(square_wave)):
        if square_wave[i] == 1:
            pwm_pin.on()
            #time.sleep((1/f) / fs)
        else:
            pwm_pin.off()
            #time.sleep((1/f) / fs)


display_plots()