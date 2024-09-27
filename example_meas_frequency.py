# -------------------------------------------------------------
# Importera bibliotek
# -------------------------------------------------------------
import pyvisa
import time
import matplotlib.pyplot as plt
import pandas as pd

# -------------------------------------------------------------
# Block 1: Initialisera
# -------------------------------------------------------------
def initialisera():
    # Initialiserar anslutningen till oscilloskopet och returnerar instrumentobjektet
    rm = pyvisa.ResourceManager()
    resurser = rm.list_resources()
    print("Tillgängliga resurser:", resurser)

    if not resurser:
        raise ValueError("Inga resurser hittades. Kontrollera anslutningen.")

    instrument_adress = resurser[0]
    oscilloskop = rm.open_resource(instrument_adress)
    idn = oscilloskop.query('*IDN?')
    print(f"Ansluten till: {idn}")

    oscilloskop.timeout = 5000
    oscilloskop.write_termination = '\n'
    oscilloskop.read_termination = '\n'

    return oscilloskop

# -------------------------------------------------------------
# Block 2: Mätning
# -------------------------------------------------------------
def mata(oscilloskop, antal_mätningar=10, intervall=1):
    mätdata = []

    for _ in range(antal_mätningar):
        try:
            oscilloskop.write(':MEASure:FREQuency')
            frekvens = oscilloskop.query(':MEASure:FREQuency?')
            print(f"Frekvens: {frekvens} Hz")
            mätdata.append(float(frekvens))
        except Exception as e:
            print(f"Misslyckades med att mäta frekvens: {e}")

        time.sleep(intervall)

    return mätdata

# -------------------------------------------------------------
# Block 3: Analysera
# -------------------------------------------------------------
def analysera(mätdata):
    print("\n--- Analysera data ---")
    for frekvens in mätdata:
        if frekvens < 50 or frekvens > 60:
            print(f"Varning: Frekvensen {frekvens} Hz ligger utanför det förväntade intervallet (50-60 Hz).")
        else:
            print(f"Frekvensen {frekvens} Hz ligger inom förväntat intervall.")

# -------------------------------------------------------------
# Block 4: Visualisera och exportera
# -------------------------------------------------------------
def visualisera_exportera(mätdata):
    # Skapa en graf
    plt.plot(mätdata, marker='o', linestyle='-', color='b')
    plt.title("Uppmätta frekvenser")
    plt.xlabel("Mätning")
    plt.ylabel("Frekvens (Hz)")
    plt.grid(True)
    plt.show()

    # Exportera till CSV
    df = pd.DataFrame(mätdata, columns=["Frekvens"])
    df.to_csv("frekvens_data.csv", index=False)
    print("Data har exporterats till 'frekvens_data.csv'.")

# -------------------------------------------------------------
# Huvudprogram
# -------------------------------------------------------------
def main():
    try:
        oscilloskop = initialisera()
    except Exception as e:
        print(f"Initialisering misslyckades: {e}")
        return

    try:
        mätdata = mata(oscilloskop, antal_mätningar=30, intervall=1)
    except Exception as e:
        print(f"Mätning misslyckades: {e}")
        return

    analysera(mätdata)
    visualisera_exportera(mätdata)

    oscilloskop.close()

if __name__ == "__main__":
    main()
