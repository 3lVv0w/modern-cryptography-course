#!/usr/bin/env python3
"""
Educational MQTT Wiretap & Packet Sniffer
Modern Cryptography Course · Crypto Chat Lab
---------------------------------------------
Subscribes to MQTT topics ('crypto/#') on the Centralized Broker
and logs live encrypted packets as they traverse the network.

Prerequisites:
    pip install paho-mqtt

Usage:
    python3 mqtt_sniffer.py [--host HOST] [--port PORT] [--topic TOPIC]
"""

import sys
import json
import argparse
from datetime import datetime

try:
    import paho.mqtt.client as mqtt
except ImportError:
    print("\n" + "=" * 65)
    print("❌ Missing dependency: 'paho-mqtt'")
    print("Please install paho-mqtt to run this MQTT sniffer:")
    print("    pip install paho-mqtt")
    print("=" * 65 + "\n")
    sys.exit(1)

# Color terminal formatting
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
MAGENTA = "\033[35m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"{GREEN}{BOLD}✓ Connected successfully to MQTT Broker!{RESET}")
        topic = userdata.get("topic", "crypto/#")
        client.subscribe(topic)
        print(f"📡 Subscribed to topic pattern: {CYAN}{BOLD}{topic}{RESET}")
        print(f"{DIM}Awaiting inbound cryptographic transmissions... (Press Ctrl+C to exit){RESET}\n")
        print(f"{'-' * 70}")
    else:
        print(f"{RED}Connection failed with error code: {rc}{RESET}")

def on_message(client, userdata, msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    topic = msg.topic
    raw_payload = msg.payload.decode('utf-8', errors='replace')
    
    print(f"\n{BOLD}[{timestamp}] {CYAN}PACKET INTERCEPTED{RESET} on topic: {YELLOW}{topic}{RESET}")

    try:
        data = json.loads(raw_payload)
        sender = data.get("sender", "Unknown")
        recipient = data.get("recipient", "Unknown")
        cipher_type = data.get("cipherType", "Raw")
        ciphertext = data.get("ciphertext", raw_payload)
        is_tampered = data.get("isTampered", False)
        is_spoofed = data.get("isSpoofed", False)
        status = data.get("status", "DELIVERED")

        print(f"  • {BOLD}Sender:{RESET}     {sender}")
        print(f"  • {BOLD}Recipient:{RESET}  {recipient}")
        print(f"  • {BOLD}Cipher:{RESET}     {MAGENTA}{cipher_type}{RESET}")
        print(f"  • {BOLD}Status:{RESET}     {status}")
        if is_tampered:
            print(f"  • {RED}{BOLD}TAMPER WARNING:{RESET} Message integrity violated by MITM!")
        if is_spoofed:
            print(f"  • {RED}{BOLD}SPOOF WARNING:{RESET} Identity spoofing detected!")
            
        print(f"  • {BOLD}Payload on Wire:{RESET}")
        print(f"    {YELLOW}{ciphertext}{RESET}")

    except json.JSONDecodeError:
        print(f"  • {BOLD}Raw Payload (Non-JSON):{RESET} {YELLOW}{raw_payload}{RESET}")

    print(f"{DIM}{'-' * 70}{RESET}")

def main():
    parser = argparse.ArgumentParser(description="Crypto Chat Lab - MQTT Packet Sniffer")
    parser.add_argument("--host", default="127.0.0.1", help="MQTT Broker hostname or IP (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=1883, help="MQTT TCP port (default: 1883)")
    parser.add_argument("--topic", default="crypto/#", help="MQTT topic pattern to subscribe to (default: crypto/#)")
    args = parser.parse_args()

    print("=" * 70)
    print(f"   🕵️  {BOLD}MQTT CRYPTOGRAPHIC WIRE SNIFFER & PACKET ANALYZER{RESET}")
    print("=" * 70)
    print(f"Target Broker: {BOLD}{args.host}:{args.port}{RESET}")
    print(f"Listening on:  {BOLD}{args.topic}{RESET}")
    print("=" * 70)

    try:
        # Paho MQTT v2 / v1 compatibility
        try:
            client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="PythonMqttSniffer", userdata={"topic": args.topic})
        except AttributeError:
            client = mqtt.Client(client_id="PythonMqttSniffer", userdata={"topic": args.topic})

        client.on_connect = on_connect
        client.on_message = on_message

        client.connect(args.host, args.port, keepalive=60)
        client.loop_forever()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Wire sniffer stopped by user. Goodbye!{RESET}")
    except ConnectionRefusedError:
        print(f"\n{RED}[ERROR] Connection refused by {args.host}:{args.port}!{RESET}")
        print("Please verify that your Centralized Lab Server is running:")
        print("    npm start (or ./start.sh)")
        print(f"Embedded Aedes broker should be active on port {args.port}.")
    except Exception as e:
        print(f"\n{RED}[ERROR] {e}{RESET}")

if __name__ == "__main__":
    main()
