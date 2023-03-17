import hashlib

def encrypt(data, k):
    return hashlib.sha256(bytes(data)).digest()[-k:]

def encrypt_bits(data, k):
    return (int(hashlib.sha256(bytes(data)).hexdigest(), 16) % (2**20))

def recompute_chain(SP, hash, n, k, flag):
    cnt = 1
    prev = SP
    print(hash)
    print(n)
    while cnt <= n:
        ct = encrypt_bits(prev, k)
        if flag == 0:
            if ct == hash:
                return prev
            cnt += 1
            prev = ct
        elif flag == 1:
            print(type(ct))
            if bytes(ct) == bytes(hash):
                return prev
            cnt += 1
            prev = ct
    
    return None

def non_trivial_find_pre_image(target, chains, n, k):
    cnt = 1
    tmp = target
    values_list = chains.values()
    while cnt <= n:
        ct = encrypt_bits(tmp, k)
        if ct in values_list:
            print(f"[+] We hit an endpoint {ct} recomputing chain now")
            SP = [k for k, v in chains.items() if v == ct][0]
            print("SP is: ", SP)
            pre_image = recompute_chain(SP, target, n, k, 1)
            print("returning")
            return pre_image
        tmp = ct
        cnt += 1
    
    return None

def main():
    t = 20
    n = 2**t
    k = 2
    target = bytearray.fromhex(str(0x812c4))
    chain = {270661 : 502005}
    pre_image = non_trivial_find_pre_image(target, chain, n, k)
    print(f"[+] We found the pre-image for the hash {pre_image}\n")

if __name__ == '__main__':
    main()