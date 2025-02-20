import asyncio
from bleak import BleakScanner, BleakClient

MESSAGE = "Hello from John..."

async def find_writable_device():
    print("🔍 Scanning for BLE devices...")

    # Step 1: Discover devices
    devices = await BleakScanner.discover()
    if not devices:
        print("❌ No BLE devices found.")
        return

    for i, device in enumerate(devices):
        print(f"{i}: {device.address} - {device.name or 'Unknown'}")

    # Step 2: Iterate through each device and check for a writable characteristic
    for device in devices:
        print(f"\n📡 Trying {device.name or 'Unknown'} ({device.address})...")

        try:
            async with BleakClient(device.address) as client:
                connected = await client.connect()
                if not connected:
                    print(f"❌ Could not connect to {device.name or 'Unknown'}")
                    continue
                print(f"✅ Connected to {device.name or 'Unknown'}!")

                # Ensure Service Discovery is completed
                await asyncio.sleep(1)
                services = await client.get_services()

                print("🔍 Searching for writable characteristics...")
                for service in services:
                    for char in service.characteristics:
                        if "write" in char.properties or "write_without_response" in char.properties:
                            print(f"🎯 Found writable characteristic: {char.uuid}")
                            print(f"✨ Device: {device.name or 'Unknown'} ({device.address})")
                            await client.write_gatt_char(char.uuid, MESSAGE.encode(), response=False)
                            print("✅ Message sent!")
                            # return device.address, char.uuid  # Stop at the first match
        except Exception as e:
            print(f"⚠️ Error with {device.address}: {e}")

    print("❌ No writable characteristic found on any device.")
    return None, None


