import hashlib
import random

def encrypt(data, k):
    return hashlib.sha256(bytes(data)).digest()[-k:]

def recompute_chain(SP, hash, n, k):
    cnt = 0
    prev = SP
    print(hash)
    while cnt < n-1:
        ct = encrypt(prev, k)
        print(ct)
        if ct == hash:
            return prev
        prev = ct
        cnt += 1
    
    return None

def compute_chains(n, k):
    start = random.randint(1, n)
    SP = encrypt(start, k)
    cnt = 0
    tmp = SP
    print(f"[+] SP of chain is {SP}")
    while cnt < n-1:
        ct = encrypt(tmp, k)
        tmp = ct
        cnt += 1

    print(f"[+] Finished {cnt} calculations")
    print(f"[+] EP of chain is {tmp}")

    return SP, tmp

def find_preimage(hash, n, k, EP, SP):
    cnt = 0
    tmp = hash
    while cnt < n-1:
        ct = encrypt(tmp, k)
        if ct == EP:
            print(f"[+] We hit an endpoint, re-computing chain now")
            return recompute_chain(SP, hash, n, k)
        tmp = ct
        cnt += 1

def main():
    t = 16
    n = 2**t
    k = 2
    target = b'\x9c\xe2'
    SP, EP = compute_chains(n, k) #[SP, EP]
    print(f"[+] There are {n} possible hashes")
    print(f"[+] Attempting to find pre-image for hash {target}")

    pre_image = find_preimage(target, n, k, EP, SP)
    print(f"[+] We found the pre-image for the hash {pre_image}")
    

if __name__ == '__main__':
    main()