import pyvisa

def list_resources():
    # Skapa en Visa Resource Manager
    rm = pyvisa.ResourceManager()

    # Lista alla tillgängliga resurser
    resources = rm.list_resources()

    if resources:
        print("Tillgängliga resurser:")
        for resource in resources:
            print(resource)
    else:
        print("Inga resurser är tillgängliga.")

    # Stäng resurshanteraren
    rm.close()

if __name__ == "__main__":
    list_resources()
