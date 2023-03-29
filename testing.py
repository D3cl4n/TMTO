import hashlib

def encrypt_bits(plaintext):
    return bin(int(hashlib.sha256(bytes(int(plaintext, 2))).hexdigest(), 16))[:22][2:]

def main():
    start = "11010000110101101101"
    for x in range(0, 1000):
        start = encrypt_bits(start)
        print(start)

    if start == "11001000011110101110":
        print("Chains computed successfully")

if __name__ == '__main__':
    main()