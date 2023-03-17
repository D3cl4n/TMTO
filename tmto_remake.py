import hashlib
import random

def encrypt(data, k):
    return hashlib.sha256(bytes(data)).digest()[-k:]

def encrypt_bits(data, k):
    return (int(hashlib.sha256(bytes(data)).hexdigest(), 16) % (2**20))

def recompute_chain(SP, hash, n, k, flag):
    cnt = 0
    prev = SP
    print(hash)
    while cnt < n:
        if flag == 0:
            ct = encrypt(prev, k)
            if ct == hash:
                return prev
        elif flag == 1:
            ct = encrypt_bits(prev, k)
            if bytes(ct) == bytes(hash):
                return prev
        prev = ct
        cnt += 1
    
    return None

def non_trivial_find_pre_image(target, chains, n, k):
    cnt = 0
    tmp = target
    values_list = chains.values()
    while cnt < n:
        ct = encrypt_bits(tmp, k)
        if ct in values_list:
            print(f"[+] We hit an endpoint {ct} recomputing chain now")
            SP = [i for i, v in chains.items() if v == ct][0]
            pre_image = recompute_chain(SP, target, n, k, 1)
            return pre_image
        tmp = ct
        cnt += 1
    
    return None

'''
@param n: number of possible hashes
@param k: bits to truncate hash to
@param l: length for each chain
'''
def multiple_chains(n, k, l):
    cnt = 1
    chains = {}
    start = random.randint(1, n)
    SP = encrypt_bits(start, k)
    tmp = SP
    while cnt <= n:
        if cnt % l == 0:
            chains.update({SP : tmp})
            SP = encrypt_bits(tmp, k)
            tmp = SP
            cnt += 1
            continue

        ct = encrypt_bits(tmp, k)
        tmp = ct
        cnt += 1

    return chains

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
            return recompute_chain(SP, hash, n, k, 0)
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
    print(f"[+] We found the pre-image for the hash {pre_image}\n")

    t = 20
    n = 2**t
    l = 2000
    target = bytearray.fromhex(str(0x84a8a))
    print(f"[+] There are {n} possible hashes")
    print(f"[+] Attempting to find the pre-image for the hash {target}")
    chains = multiple_chains(n, k, l)
    pre_image = non_trivial_find_pre_image(target, chains, n, k)
    print(f"[+] We found the pre-image for the hash {pre_image}\n")
    

if __name__ == '__main__':
    main()