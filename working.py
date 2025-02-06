import asyncio
from bleak import BleakScanner, BleakClient

# List of known working device UUIDs
DEVICES_THAT_WORKED = [
    "AD23D6E5-D431-26E6-EFE2-8234C46E4FB0",
    "2E5E49B6-E118-8DE1-2D8C-4CA765BCEB9C",
    "B6B03CF1-2351-8899-EF90-112C2EFF6D46"
]

MESSAGE = "Hello from Python!"


async def send_to_specific_devices():
    print("🔍 Scanning for BLE devices...")

    # Step 1: Discover devices
    devices = await BleakScanner.discover()
    if not devices:
        print("❌ No BLE devices found.")
        return

    # Step 2: Iterate through each device and check if it's in our list
    for device in devices:
        if device.address in DEVICES_THAT_WORKED:
            print(f"\n📡 Found matching device: {device.name or 'Unknown'} ({device.address})")

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

                                # Step 3: Send the message
                                await client.write_gatt_char(char.uuid, MESSAGE.encode())
                                print("✅ Message sent!")
                                return  # Stop after successfully sending a message

            except Exception as e:
                print(f"⚠️ Error with {device.address}: {e}")

    print("❌ No writable characteristic found on the matching devices.")


# Run the process
asyncio.run(send_to_specific_devices())
