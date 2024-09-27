import numpy as np
import matplotlib.pyplot as plt

# Skapa tidsvektor
fs = 1000  # Samplingsfrekvens i Hz
t = np.linspace(0, 1, fs)  # 1 s 

# Skapa sinusvåg
f = 5  # Frekvens i Hz
sinus = np.sin(2 * np.pi * f * t)

# Rita upp sinusvågen
plt.figure(figsize=(10, 6))
plt.plot(t, sinus, label='Ren sinus', color='blue')
plt.title('Ren sinusvåg')
plt.xlabel('Tid [s]')
plt.ylabel('Amplitud')
plt.legend()
plt.grid(True)
plt.show()


