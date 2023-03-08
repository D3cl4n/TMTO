import math
import hashlib
import random

class TMTO:
    def __init__(self, t):
        self.t = t
        self.modulus = 2^self.t
        self.cnt = {2 : 99, 3 : 999, 4 : 9999}
        self.chains = {}

    def decimal_to_bin(self, n):
        return bin(n)[2:]

    def add_SP_EP(self, SP, EP):
        self.chains.update({1 : SP, 2 : EP})
        print(f"[+] Chain SP: {self.chains[1]}")
        print(f"[+] Chain EP: {self.chains[2]}")

    def truncate(self, ciphertext, n):
        return ciphertext[:32 - n]

    def compute_chains(self):
        starting_point = random.randint(0, self.cnt[self.t / 8])
        chain_sp = self.truncate(hashlib.sha256(str(starting_point).encode("utf-8")).hexdigest(), 16)
        print(f"[+] Starting chain generation at: {chain_sp}")

        counter = 1
        tmp = chain_sp
        while counter <= self.cnt[self.t / 8]:
            ciphertext = self.truncate(hashlib.sha256(str(tmp).encode("utf-8")).hexdigest(), 16)
            tmp = ciphertext
            if counter == cnt[self.t/8]:
                print(f"[+] Finished {counter} SHA256 calculations")
                print("[+] Reached end of chain calculation, storing SP and EP")
                chain_ep = tmp
                self.add_SP_EP(chain_sp, chain_ep)
            counter += 1

    def find_preimage(self, hash):
        random_start = random.randint(0, self.cnt[self.t / 8])
        ciphertext = self.truncate(hashlib.sha256(str(random_start).encode("utf-8")).hexdigest(), 16)
        tmp = ciphertext
        counter = 0
        while counter < self.cnt[self.t/8]:
            tmp = self.truncate(hashlib.sha256(str(tmp).encode("utf-8")).hexdigest(), 16)
            if self.chains[2] == tmp:
                print("[+] ")

'''
Description: Driver code for the attack
'''
def main():
    tmto_attack = TMTO(16)
    tmto_attack.compute_chains()
    tmto_attack.find_preimage("6f4b6612125fb3a0")

if __name__ == '__main__':
    main()
