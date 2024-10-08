import pyvisa
import time
import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from threading import Thread

def init_oscilloscope():

    rm = pyvisa.ResourceManager()
    res = rm.list_resources()
    print(f'Availible resources: ', res)

    if not res:
        raise ValueError('No resources found, check connection')
    
    instrument_addr = res[0]
    oscilloscope = rm.open_resource(instrument_addr)

    identity = oscilloscope.query('*IDN?')
    print(f'Connected to: {identity}')

    oscilloscope.write('')
    oscilloscope.write('*RST')

    oscilloscope.timeout = 5000
    oscilloscope.write_termination = '\n'
    oscilloscope.read_termination = '\n'
    oscilloscope.write(':CHANnel1:PROBe 1')
    oscilloscope.write(':CHANnel1:RANGe 12')
    oscilloscope.write(':CHANnel1:OFFSet 0')
    oscilloscope.write(':TIMebase:RANGe 40E-3')
    oscilloscope.write(':TIMebase:DELay 0')
    oscilloscope.write(':TRIGger:SWEep NORMal')
    oscilloscope.write(':TRIGger:LEVel 2')
    oscilloscope.write(':TRIGger:SLOpe POSitive')

    oscilloscope.write('ACQuire:TYPE NORMal')

    return oscilloscope

def meas_freq(oscilloscope, no_of_measurments):
    frequency_data = []
    try:
        oscilloscope.write(':MEASure:FREQuency')
        for no in range(no_of_measurments):
            
            freq = oscilloscope.query(':MEASure:FREQuency?')
            print(f'Frequency: {freq} Hz')
            frequency_data.append(float(freq))
    except Exception as e:
        print(f'Failed to measure the frequency: {e}')

    return frequency_data

def analyze_freq(frequency_data, low_freq, high_freq):
    length = len(frequency_data)
    print(f'Length: {length}')
    for i in range(length):
        if frequency_data[i] < low_freq:
            print(f'Frequency is lower than {low_freq} Hz ')
        elif frequency_data[i] > high_freq:
            print(f'Frequency is higher than {high_freq} Hz')
        else:
            print(f'Frequency within range {low_freq} - {high_freq}')

def meas_voltage(oscilloscope):
    amplitude_data = []
    try:
        oscilloscope.write(':MEASure:VAMPlitude')
        for no in range(no_of_measurments):
            
            amp = oscilloscope.query(':MEASure:VAMPlitude?')
            print(f'Amplitude: {amp} V')
            amplitude_data.append(float(amp))
    except Exception as e:
        print(f'Failed to measure the amplitude: {e}')

    return amplitude_data

def meas_nduty(oscilloscope):
    nduty_data = []
    try:
        oscilloscope.write(':MEASure:NDUTy')
        for no in range(no_of_measurments):
            
            duty = oscilloscope.query(':MEASure:NDUTy?')
            print(f'Amplitude: {duty} V')
            nduty_data.append(float(duty))
    except Exception as e:
        print(f'Failed to measure the amplitude: {e}')

    return nduty_data

# -------------------------------------------------------------
# Block 4: Visualisera och exportera
# -------------------------------------------------------------
def visualisera_exportera(frequency_data, amplitude_data):
    # Skapa en graf for frekvens
    plt.plot(frequency_data, marker='o', linestyle='-', color='b')
    plt.title("Uppmätta frekvenser")
    plt.xlabel("Mätning")
    plt.ylabel("Frekvens (Hz)")
    plt.grid(True)
    plt.show()

    # Skapa en graf för amplitud
    plt.plot(amplitude_data, marker='o', linestyle='-', color='b')
    plt.title("Uppmätta amplituder")
    plt.xlabel("Mätning")
    plt.ylabel("Amplitud (V)")
    plt.grid(True)
    plt.show()

    # Exportera till CSV
    print(f'Class of data: {type(frequency_data)}')
    df = pd.DataFrame(data={'Frekvens':frequency_data, 'Amplitud':amplitude_data})
    df.to_csv("./test_data.csv", sep=',', index=False)
    print("Data har exporterats till 'frekvens_data.csv'.")


def get_raw_data(oscilloscope):

    oscilloscope.write(':WAVeform:SOURce CHANnel1')
    oscilloscope.write(':AUToscale')
    oscilloscope.write(':WAVeform:FORMat ASCII')
    #oscilloscope.write(':WAVeform:POINts:MODE RAW') 
    #oscilloscope.write(':WAVeform:POINts: 1000')
    #oscilloscope.write(':WAVeform:DATA')

    raw_data = oscilloscope.query(':WAVeform:DATA?')

    #raw_data_ = raw_data.strip(' ')
    raw_data_list = raw_data.split(',')[1:]
    
    raw_data_float = [float(val) for val in raw_data_list]

    plt.plot(raw_data_float)
    plt.show()
    df = pd.DataFrame(raw_data_float)
    df.to_csv("./raw_data.csv", index=False)
    print("Data har exporterats till 'raw_data.csv'.")

    # Get channel 2 raw data
    oscilloscope.write(':WAVeform:SOURce CHANnel2')
    oscilloscope.write(':AUToscale')
    raw_data_channel2 = oscilloscope.query(':WAVeform:DATA?')

    #raw_data_ = raw_data.strip(' ')
    raw_data_channel2_list = raw_data_channel2.split(',')[1:]
    
    raw_data_channel2_float = [float(val) for val in raw_data_channel2_list]

    plt.plot(raw_data_channel2_float)
    plt.show()
    df = pd.DataFrame(raw_data_channel2_float)
    df.to_csv("./raw_data_channel2.csv", index=False)
    print("Data har exporterats till 'raw_data_channel2.csv'.")

def show_raw_data():
    t = np.linspace(0, 0.02, 5000) 
    fig, ax = plt.subplots(2)
    ax[0].plot(t, pd.read_csv('./raw_data.csv'), color='blue')
    ax[0].plot(t, pd.read_csv('./raw_data_channel2.csv'), color='red')
    plt.show()

# Main below

# Variables:

low_freq = 40
high_freq = 60
frequency = 0
#channel = 1
no_of_measurments = 5

# Init the oscilloscope.
try:
    oscilloscope = init_oscilloscope()
except Exception as e:
    print(f"Initialize failed: {e}")
  
# Read the frequency  
try:
    frequency_data = meas_freq(oscilloscope, no_of_measurments)
except Exception as e:
    print(f'Measurement failed: {e}')


analyze_freq(frequency_data, low_freq, high_freq)

try:
    amplitude_data = meas_voltage(oscilloscope)
except Exception as e:
    print(f'Measurement failed: {e}')

#Try to get Raw-data

get_raw_data(oscilloscope)
show_raw_data()

# Här ska all data vara hämtad

# Close the connection
oscilloscope.close()