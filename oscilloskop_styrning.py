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
    print(f'Oscilloscope reset.')

    oscilloscope.timeout = 1000
    oscilloscope.write_termination = '\n'
    oscilloscope.read_termination = '\n'
    
    # Initiazlize the oscilloscope to the expected ratio
    oscilloscope.write(':CHANnel1:PROBe 1')
    oscilloscope.write(':CHANnel2:PROBe 1')
    oscilloscope.write(':AUToscale')
    oscilloscope.timeout = 1000
    oscilloscope.write(':CHANnel1:RANGe 12')
    oscilloscope.write(':CHANnel2:RANGe 12')
    oscilloscope.write(':CHANnel1:OFFSet 0')
    oscilloscope.write(':CHANnel2:OFFSet 0')
    oscilloscope.write(':TIMebase:RANGe 0.2')
    oscilloscope.write(':TIMebase:DELay 0')
    oscilloscope.write(':TIMebase:MODE MAIN')
    oscilloscope.write(':TRIGger:SWEep NORMal')
    oscilloscope.write(':TRIGger:LEVel 2')
    oscilloscope.write(':TRIGger:SLOpe POSitive')

    oscilloscope.write('ACQuire:TYPE NORMal')

    return oscilloscope

# Not used
def meas_freq(oscilloscope, no_of_measurments):
    frequency_data = []
    try:
        print(f'Meas_freq')
        oscilloscope.write(':MEASure:FREQuency')
        for no in range(no_of_measurments):
            freq = oscilloscope.query(':MEASure:FREQuency?')
            print(f'Frequency: {freq} Hz')
            frequency_data.append(float(freq))
    except Exception as e:
        print(f'Failed to measure the frequency: {e}')

    return frequency_data

# Not used
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

# Not used
def meas_voltage(oscilloscope):
    amplitude_data = []
    print(f'Meas_volt')
    try:
        oscilloscope.write(':MEASure:VAMPlitude')
        for no in range(no_of_measurments):
            amp = oscilloscope.query(':MEASure:VAMPlitude?')
            print(f'Amplitude: {amp} V')
            amplitude_data.append(float(amp))
    except Exception as e:
        print(f'Failed to measure the amplitude: {e}')

    return amplitude_data

# Not used
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

# Not used
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
    
    oscilloscope.write(":WAVeform:SOURce CHANnel1")
    oscilloscope.write(':CHANnel1:RANGe 8')
    oscilloscope.write(':TIMebase:RANGe 100E-3')
    oscilloscope.write(":WAVeform:FORMat ASCII")
    
    # Get preamble from Channel 1
    oscilloscope.timeout = 10000
    preamble = oscilloscope.query(":WAVeform:PREamble?")
    oscilloscope.timeout = 10000 
    preamble_list = preamble.split(',')
    preamble_list = [float(val) for val in preamble_list]
    df = pd.DataFrame(preamble_list)
    df.to_csv("./preamble_raw_data.csv", index=False)
    
    # Get raw data from Channel 1
    raw_data = oscilloscope.query(':WAVeform:DATA?')
    raw_data_list = raw_data.split(',')[1:]
    raw_data_float = [float(val) for val in raw_data_list]
    df = pd.DataFrame(raw_data_float)
    df.to_csv("./raw_data.csv", index=False)
    print("Data har exporterats till 'raw_data.csv'.")

    # Get channel 2 raw data
    oscilloscope.timeout = 1000
    oscilloscope.write(':WAVeform:SOURce CHANnel2')
    oscilloscope.write(':CHANnel2:RANGe 8')
    oscilloscope.write(':TIMebase:DELay 0')
    oscilloscope.write(':TIMebase:RANGe 100E-3')
    oscilloscope.write(':WAVeform:FORMat ASCII')
    oscilloscope.timeout = 10000

    # Get preamble from channel 2
    preamble = oscilloscope.query(':WAVeform:PREamble?')
    preamble_list = preamble.split(',')
    preamble_list = [float(val) for val in preamble_list]
    df = pd.DataFrame(preamble_list)
    df.to_csv("./preamble_raw_data_channel2.csv", index=False)
    
    # Get raw data from channel 2
    raw_data_channel2 = oscilloscope.query(':WAVeform:DATA?')
    raw_data_channel2_list = raw_data_channel2.split(',')[1:]
    raw_data_channel2_float = [float(val) for val in raw_data_channel2_list]
    df = pd.DataFrame(raw_data_channel2_float)
    df.to_csv("./raw_data_channel2.csv", index=False)
    print("Data har exporterats till 'raw_data_channel2.csv'.")

    plt.plot(raw_data_channel2_float)
    plt.show()

def show_raw_data(): 
    fig, ax = plt.subplots(3)
    fig.suptitle(f"Data acquired from: {oscilloscope.query('*IDN?')}")
    
    # Read the csv-files
    pre_amble_channel1 = pd.read_csv('./preamble_raw_data.csv')
    pre_amble_channel2 = pd.read_csv('./preamble_raw_data_channel2.csv')
    raw_data_channel1 = pd.read_csv('./raw_data.csv')
    raw_data_channel2 = pd.read_csv('./raw_data_channel2.csv')

    # Set all the parameters for the graphs, calculated from the preamble data of oscilloscope
    ax[0].set_ylim(raw_data_channel1['0'].min(), raw_data_channel1['0'].max())
    ax[1].set_ylim(raw_data_channel2['0'].min(), raw_data_channel2['0'].max())

    # Combined graph needs gets the highest amplitude as the scale
    if raw_data_channel1['0'].min() > raw_data_channel2['0'].min():
        pre_amble_min = raw_data_channel2['0'].min()
    else:
        pre_amble_min = raw_data_channel1['0'].min()
    if raw_data_channel1['0'].max() > raw_data_channel2['0'].max():
        pre_amble_max = raw_data_channel1['0'].max()
    else:
        pre_amble_max = raw_data_channel2['0'].max()
    
    ax[2].set_ylim(pre_amble_min, pre_amble_max)

    # X-axis is calculated from (number of ticks) * (time of each tick) 
    xlim = pre_amble_channel1['0'][4] * pre_amble_channel1['0'][2]
    x_ticks = []
    x_positions = []
    x_ticks.append(0)
    for i in range(1,6,1):
        x_ticks.append(round((xlim / 5)*i, 3))
        
    x_positions = [0, 12500, 25000, 37500, 50000, 62500]
    ax[0].set_xticks(x_positions,x_ticks)
    ax[1].set_xticks(x_positions,x_ticks)
    ax[2].set_xticks(x_positions, x_ticks)
    ax[0].set_title('Channel 1: Pre-filter')
    ax[1].set_title('Channel 2: Post-filter')
    ax[2].set_title('Channel 1 & 2 combined')
    
    # Post data from Channel 1
    
    ax[0].plot(raw_data_channel1, color='blue')
    ax[2].plot(raw_data_channel1, color='blue')
    
    # Post data from channel 2
    
    ax[1].plot(raw_data_channel2, color='red')
    ax[2].plot(raw_data_channel2, color='red')
        
    fig.savefig('output_data.pdf')
    plt.show()

# Main below

# Variables: (Not used anymore)
low_freq = 40
high_freq = 60
frequency = 0
no_of_measurments = 1

# Init the oscilloscope.

try:
    oscilloscope = init_oscilloscope()
except Exception as e:
    print(f"Initialize failed: {e}")
'''
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
'''
#Try to get Raw-data

get_raw_data(oscilloscope)
show_raw_data()

# Close the connection
oscilloscope.close()