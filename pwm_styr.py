import numpy as np
import matplotlib.pyplot as plt
import scipy
import scipy.signal
#from gpiozero import PWMLED
#from gpiozero import LED

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

print(f'Length of Sinus: {len(sinus)}')
print(f'Length of Sawtooth: {len(sawtooth)}')    
print(f'Length of Square: {len(square_wave)}')

def display_plots():
    #for i in range(len(square_wave)):
    plt.plot(t, square_wave, label='SquareWave', color='green')
    plt.show()
    # Rita upp sinusvågen
    plt.figure(figsize=(10, 6))
    plt.plot(t, sinus, label='Ren sinus', color='blue')
    plt.title('Sinus')
    plt.xlabel('Tid [s]')
    plt.ylabel('Amplitud')
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(t, sawtooth, label='Sågtand', color='red')
    plt.title('Sågtand')
    plt.xlabel('Tid [s]')
    plt.ylabel('Amplitud')
    plt.legend()
    plt.grid(True)
    plt.show()

    #new_t = np.linspace(0, 0.04, fs)

    plt.figure(figsize=(100, 60))
    plt.plot(t, sinus, label='Sinus', color='blue')
    plt.plot(t, sawtooth, label='Sågtand', color='red')
    plt.plot(t, square_wave, label='Squarewave', color='green')
    plt.title('Båda')
    plt.xlabel('Tid [s]')
    plt.ylabel('Amplitud')
    plt.legend()
    plt.grid(True)
    plt.show()
'''
#pwm_pin = PWMLED(12, frequency=50)
pwm_pin = LED(12)
for j in range(20):
    for i in range(len(square_wave)):
        if square_wave[i] == 1:
            pwm_pin.on()
        else:
            pwm_pin.off()
'''
#Uncomment to display plots
display_plots()