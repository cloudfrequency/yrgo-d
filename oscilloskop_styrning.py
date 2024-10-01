import pyvisa
import time
import csv
import matplotlib.pyplot as plt
import pandas as pd

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

    oscilloscope.timeout = 5000
    oscilloscope.write_termination = '\n'
    oscilloscope.read_termination = '\n'
    oscilloscope.write(':CHANnel1:PROBe 1')
    oscilloscope.write(':CHANnel1:RANGe 12')
    oscilloscope.write(':CHANnel1:OFFSet 0')
    oscilloscope.write(':TIMebase:MODE MAIN')
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
        for no in range(no_of_measurments):
            oscilloscope.write(':MEASure:FREQuency')
            freq = oscilloscope.query(':MEASure:FREQuency?')
            print(f'Frequency: {freq} Hz')
            time.sleep(0.5)
            #time.sleep(0.04)
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

def meas_phase(oscilloscope, channel):
     
    try:
        oscilloscope.write(':MEASure:PHASe')
        phase = oscilloscope.query(':MEASure:PHASe?')
        print(f'Phase: {phase}')
    except Exception as e:
        print(f'Failed to measure phase: {e}')
    
    return float(phase)

def meas_voltage(oscilloscope):
    
    amplitude_data = []
    try:
        for no in range(no_of_measurments):
            oscilloscope.write(':MEASure:VAMPlitude')
            amp = oscilloscope.query(':MEASure:VAMPlitude?')
            print(f'Amplitude: {amp} V')
            #time.sleep(0.5)
            time.sleep(0.04)
            amplitude_data.append(float(amp))
    except Exception as e:
        print(f'Failed to measure the amplitude: {e}')

    return amplitude_data

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
    df = pd.DataFrame(data={'Frekvens':frequency_data, 'Amplitud':amplitude_data})
    df.to_csv("./frekvens_data.csv", sep=',', index=False)
    print("Data har exporterats till 'frekvens_data.csv'.")

'''
def digitize(oscilloscope):
    oscilloscope.write(':DIGItize CHANnel1')
    oscilloscope.write(':WAVeform:SOURce CHANnel1')
    oscilloscope.write(':WAVeform:FORMat BYTE')
    oscilloscope.write(':WAVeform:POINts 500')

    result = oscilloscope.query(':WAVeform:DATA?')

    return result
'''
# Main below

# Variables:

low_freq = 40
high_freq = 60
frequency = 0
channel = 1
no_of_measurments = 10

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

# Read the phase
'''try: 
    phase = meas_phase(oscilloscope, 1)
except Exception as e:
    print(f'Measurement failed: {e}')
'''

try:
    amplitude_data = meas_voltage(oscilloscope)
except Exception as e:
    print(f'Measurement failed: {e}')

visualisera_exportera(frequency_data, amplitude_data)
#Try to get Raw-dat
'''
with open('test.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer = digitize(oscilloscope)
'''

#print(f'Digitized: {digitize(oscilloscope)}')
# Close the connection
oscilloscope.close()