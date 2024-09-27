import numpy as np
import csv

# Skapa tidsvektor
fs = 1000  # Samplingsfrekvens i Hz
t = np.linspace(0, 1, fs)  # 1 s

# Skapa sinusvåg
f = 5  # Frekvens i Hz
sinus = np.sin(2 * np.pi * f * t)

# Skriv tid och sinusvärden till CSV-fil
with open('test.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Tid (s)', 'Sinus'])  # Header-rad
    for time, sin_value in zip(t, sinus):
        writer.writerow([time, sin_value])

print("Tid och sinusvärden har skrivits till test.csv.")
