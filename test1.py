import hashlib
import random

def encrypt_bits(plaintext):
    return bin(int(hashlib.sha256(bytes(int(plaintext, 2))).hexdigest(), 16))[:22][2:]

def random_start():
    start = ""
    for x in range(0, 20):
        bit = random.randint(0, 1)
        start += str(bit)

    return bin(int(start, 2))[2:].zfill(20)

def compute_chains(n, chain_length):
    print(f"[+] Computing chains of length {chain_length}")
    chains = {}
    cnt = 1
    SP = random_start()
    tmp = SP
    while cnt <= n:
        if cnt % chain_length == 0:
            chains.update({SP : tmp})
            SP = tmp
        ct = encrypt_bits(tmp)
        cnt += 1
        tmp = ct
    
    return chains

def verify_chains(chains, chain_length):
    print("[+] Verifying chains were computed correctly")
    SP = list(chains.keys())[1]
    EP = chains[next(next(iter(chains)))]

    flag = 1
    tmp = SP
    for x in range(1, chain_length):
        ct = encrypt_bits(tmp)
        tmp = ct

    if tmp == EP:
        flag = 0

    return flag

def main():
    t = 20
    n = 2**t
    chain_length = 2000
    target = random_start()
    chains = compute_chains(n, chain_length)
    print(chains)
    if verify_chains(chains, chain_length) != 0:
        print("[+] Chains were not computed correctly")
        exit(-1)
    else:
        print("[+] Chains were computed correctly")

if __name__ == '__main__':
    main()