import hashlib
from itertools import chain
import random
import timeit

def encrypt_bits(plaintext):
    return bin(int(hashlib.sha256(bytes(int(plaintext, 2))).hexdigest(), 16))[:22][2:]

def random_start():
    start = ""
    for x in range(0, 20):
        bit = random.randint(0, 1)
        start += str(bit)

    return bin(int(start, 2))[2:].zfill(20)

def recompute_chain(SP, EP, target):
    start = timeit.default_timer()
    print(f"[+] Re-computing chain")
    while SP != EP:
        prev = SP
        SP = encrypt_bits(SP)
        if SP == target:
            return prev
    
    stop = timeit.default_timer()
    diff = (stop - start) * 1000
    print(f"[+] Function recompute_chain took {diff} ms")

    return None

def tmto_attack(target, n, chains, chain_length):
    start = timeit.default_timer()
    print(f"[+] Trying to find pre-image for {target}")
    cnt = 1
    tmp = target
    vals = list(chains.values())
    while cnt <= n:
        ct = encrypt_bits(tmp)
        if ct in vals:
            SP = [i for i in chains if chains[i] == ct]
            print(f"[+] We hit an endpoint {ct}")
            print(f"[+] Corresponding SP {SP}")
            return recompute_chain(SP[0], ct, target)
        tmp = ct
        cnt += 1

    stop = timeit.default_timer()
    diff = (stop - start) * 1000
    print(f"[+] Function tmto_attack took {diff} ms")

    return "No pre-image found"

def compute_chains(n, chain_length):
    start = timeit.default_timer()
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
    
    stop = timeit.default_timer()
    diff = (stop - start) * 1000
    print(f"[+] Function compute_chains took: {diff} ms")

    return chains

def main():
    t = 20
    n = 2**t
    chain_length = 1000
    target = "11011110000001010011"
    chains = compute_chains(n, chain_length)
    print(chains)
    
    pre_image = tmto_attack(target, n, chains, chain_length)
    print(f"[+] Found pre-image for hash {pre_image}")

if __name__ == '__main__':
    main()