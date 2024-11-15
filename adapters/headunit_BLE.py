import asyncio
from bleak import BleakScanner, BleakClient

# UUID-er for tjeneste og karakteristikk
SERVICE_UUID = "12345678-1234-1234-1234-1234567890ab"
CHARACTERISTIC_UUID = "abcdefab-cdef-abcd-efab-cdefabcdefab"


# Funksjon for å skanne etter BLE-enheter
async def scan_ble_devices():
    print("Skanner etter BLE-enheter...")
    devices = await BleakScanner.discover()
    esp32_devices = [d for d in devices if d.name and "ESP32" in d.name]
    print(f"Fant {len(esp32_devices)} ESP32-enheter")
    return esp32_devices

# Funksjon for å lese data fra enheten
async def read_data_from_device(address, client):
    try:
        value = await client.read_gatt_char(CHARACTERISTIC_UUID)
        try:
            decoded_value = value.decode('utf-8')
            print(f"Verdi fra {address}: {decoded_value}")
        except UnicodeDecodeError:
            print(f"Verdi fra {address} (rå bytes): {value}")
    except Exception as e:
        print(f"Feil ved lesing av data fra {address}: {e}")


# Funksjon for å sende data til enheten
async def send_data_to_device(address, client, message):
    try:
        await client.write_gatt_char(CHARACTERISTIC_UUID, message.encode('utf-8'))
        print(f"Sendte data til {address}: {message}")
    except Exception as e:
        print(f"Feil ved sending av data til {address}: {e}")


# Funksjon for å kommunisere med en BLE-enhet basert på adresse
async def communicate_with_device(address, message):
    try:
        async with BleakClient(address) as client:
            if await client.is_connected():
                print(f"Koblet til {address}")
                if message:
                    await send_data_to_device(address, client, message)
                else:
                    print("Ingen melding å sende.")
            else:
                print(f"Kunne ikke koble til {address}")
    except Exception as e:
        print(f"Feil under kommunikasjon med {address}: {e}")

async def data_communication(device, device_name, message):
    if device.name == device_name:
        print(f"Kommuniserer med enhet: {device.name} ({device.address})")
        # Send "lock_door" melding til alle enhetene
        await communicate_with_device(device.address, message)
        await asyncio.sleep(1)  # Litt pause mellom hver kommunikasjon

# Hovedfunksjon for å håndtere flere enheter samtidig
async def main():
    device_name = "ESP32_BLE_autoDoorLock"
    while True:
        # Skann etter enheter
        devices = await scan_ble_devices()
        for device in devices:
            if device.name == device_name:
                await data_communication(device, device_name, "lock_door")
                await asyncio.sleep(10)  # Vent i 10 sekunder før neste runde
                await data_communication(device, device_name, "unlock_door")

# Kjør hovedfunksjonen
if __name__ == "__main__":
    asyncio.run(main())
