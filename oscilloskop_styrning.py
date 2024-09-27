import pyvisa
import time

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
    oscilloscope.write(':CHANnel1:PROBe 10')
    oscilloscope.write(':CHANnel1:RANGe 10')
    oscilloscope.write(':CHANnel1:OFFSet 0')
    oscilloscope.write(':TIMebase:MODE MAIN')
    oscilloscope.write(':TIMebase:RANGe 1E-3')
    oscilloscope.write(':TIMebase:DELay 0')
    oscilloscope.write(':TRIGger:SWEep NORMal')
    oscilloscope.write(':TRIGger:LEVel 2')
    oscilloscope.write(':TRIGger:SLOpe POSitive')

    oscilloscope.write('ACQuire:TYPE NORMal')



    return oscilloscope

def meas_freq(oscilloscope):

    try:
        oscilloscope.write(':MEASure:FREQuency')
        freq = oscilloscope.query(':MEASure:FREQuency?')
        print(f'Frequency: {freq} Hz')
    except Exception as e:
        print(f'Failed to measure the frequency: {e}')

    return float(freq)

def analyze_freq(frequency, low_freq, high_freq):

    if frequency > low_freq:
        print(f'Frequency is lower than {low_freq} Hz ')
    elif frequency < high_freq:
        print(f'Frequency is higher than {high_freq} Hz')
    else:
        print(f'Frequency within range {low_freq} - {high_freq}')

def meas_phase(oscilloscope, channel):
     
    try:
        oscilloscope.write(':MEASure:PHASe CHANnel{channel}')
        phase = oscilloscope.query('MEASure:PHASe? CHANnel{channel}')
    except Exception as e:
        print(f'Failed to measure phase: {e}')
    
    return float(phase)

def digitize(oscilloscope):
    oscilloscope.write(':DIGItize CHANnel1')
    oscilloscope.write(':WAVeform:SOURce CHANnel1')
    oscilloscope.write(':WAVeform:FORMat BYTE')
    oscilloscope.write(':WAVeform:POINts 500')

    result = oscilloscope.query(':WAVeform:DATA?')

    return result

# Main below

# Variables:

low_freq = 50
high_freq = 60
frequency = 0
channel = 2

# Init the oscilloscope.
try:
    oscilloscope = init_oscilloscope()
except Exception as e:
    print(f"Initialize failed: {e}")
  
try:
    frequency = meas_freq(oscilloscope)
except Exception as e:
    print(f'Measurement failed: {e}')


analyze_freq(frequency, low_freq, high_freq)

try: 
    phase = meas_phase(oscilloscope, channel)
except Exception as e:
    print(f'Measurement failed: {e}')

print(f'Digitized: {digitize(oscilloscope)}')
# Close the connection
oscilloscope.close()