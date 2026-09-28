#!/usr/bin/env python3
"""
Educational MQTT Message Publisher
Modern Cryptography Course · Crypto Chat Lab
---------------------------------------------
Publishes encrypted or plaintext messages to MQTT topics
('crypto/classroom/broadcast' or 'crypto/direct/<recipient>').
Demonstrates how external Python clients, IoT nodes, and servers
can inject cryptographic payloads into the central chat ecosystem.

Prerequisites:
    pip install paho-mqtt

Usage:
    python3 mqtt_publisher.py --sender "IoT_Sensor_1" --cipher caesar --shift 3 --message "HELLO CLASS"
    python3 mqtt_publisher.py --sender "PythonBot" --cipher vigenere --key "SECRET" --message "CONFIDENTIAL REPORT"
    python3 mqtt_publisher.py --help
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
    print("Please install paho-mqtt to run this MQTT publisher:")
    print("    pip install paho-mqtt")
    print("=" * 65 + "\n")
    sys.exit(1)

def caesar_encrypt(plaintext: str, shift: int) -> str:
    res = []
    shift = shift % 26
    for char in plaintext:
        if 'a' <= char <= 'z':
            res.append(chr((ord(char) - 97 + shift) % 26 + 97))
        elif 'A' <= char <= 'Z':
            res.append(chr((ord(char) - 65 + shift) % 26 + 65))
        else:
            res.append(char)
    return "".join(res)

def vigenere_encrypt(plaintext: str, key: str) -> str:
    if not key:
        return plaintext
    res = []
    clean_key = "".join([c for c in key if c.isalpha()])
    if not clean_key:
        return plaintext
    
    key_idx = 0
    for char in plaintext:
        if char.isalpha():
            is_upper = char.isupper()
            base = 65 if is_upper else 97
            k_char = clean_key[key_idx % len(clean_key)]
            k_shift = ord(k_char.upper()) - 65
            encoded = chr((ord(char) - base + k_shift) % 26 + base)
            res.append(encoded)
            key_idx += 1
        else:
            res.append(char)
    return "".join(res)

def main():
    parser = argparse.ArgumentParser(description="Crypto Chat Lab - MQTT Message Publisher")
    parser.add_argument("--host", default="127.0.0.1", help="MQTT Broker host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=1883, help="MQTT TCP port (default: 1883)")
    parser.add_argument("--sender", default="Python_Agent", help="Sender username")
    parser.add_argument("--recipient", default="Classroom Broadcast", help="Recipient username or 'Classroom Broadcast'")
    parser.add_argument("--cipher", choices=["plaintext", "caesar", "vigenere", "raw"], default="caesar", help="Cipher type")
    parser.add_argument("--message", default="Hello from external Python MQTT client!", help="Plaintext message to encrypt and send")
    parser.add_argument("--shift", type=int, default=3, help="Shift for Caesar cipher (default: 3)")
    parser.add_argument("--key", default="CRYPTO", help="Keyword for Vigenère cipher (default: CRYPTO)")

    args = parser.parse_args()

    # Determine encryption
    cipher_type = "Plaintext"
    key_value = ""
    if args.cipher == "caesar":
        cipher_type = "Caesar"
        key_value = str(args.shift)
        ciphertext = caesar_encrypt(args.message, args.shift)
    elif args.cipher == "vigenere":
        cipher_type = "Vigenere"
        key_value = args.key
        ciphertext = vigenere_encrypt(args.message, args.key)
    elif args.cipher == "raw":
        cipher_type = "Raw"
        ciphertext = args.message
    else:
        cipher_type = "Plaintext"
        ciphertext = args.message

    is_broadcast = (args.recipient == "Classroom Broadcast" or args.recipient == "broadcast")
    topic = "crypto/classroom/broadcast" if is_broadcast else f"crypto/direct/{args.recipient}"

    payload = {
        "sender": args.sender,
        "recipient": "Classroom Broadcast" if is_broadcast else args.recipient,
        "ciphertext": ciphertext,
        "cipherType": cipher_type,
        "key": key_value
    }

    payload_json = json.dumps(payload)

    print("=" * 65)
    print(" 🚀 MQTT CRYPTOGRAPHIC MESSAGE PUBLISHER")
    print("=" * 65)
    print(f"Target Broker: {args.host}:{args.port}")
    print(f"Destination:   {topic}")
    print(f"Sender:        {args.sender}")
    print(f"Cipher:        {cipher_type} (Key/Shift: {key_value or 'None'})")
    print(f"Original Text: {args.message}")
    print(f"Ciphertext:    {ciphertext}")
    print("-" * 65)

    try:
        try:
            client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"pub_{args.sender}")
        except AttributeError:
            client = mqtt.Client(client_id=f"pub_{args.sender}")

        client.connect(args.host, args.port, keepalive=60)
        client.loop_start()
        
        info = client.publish(topic, payload_json, qos=0)
        info.wait_for_publish()
        
        client.loop_stop()
        client.disconnect()

        print("✓ Packet published successfully into MQTT broker!")
        print("Check the web chat interface or instructor wiretap dashboard to view it live.")
        print("=" * 65)
    except ConnectionRefusedError:
        print(f"\n[ERROR] Connection refused by {args.host}:{args.port}!")
        print("Please ensure the central lab server is running on port 3005 (embedded MQTT port 1883).")
    except Exception as e:
        print(f"\n[ERROR] Failed to publish: {e}")

if __name__ == "__main__":
    main()
