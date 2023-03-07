import math
import hashlib
import random

class TMTO:
    def __init__(self, t):
        self.t = t
        self.modulus = 2^self.t
        self.chains = {}

    def decimal_to_bin(self, n):
        return bin(n)[2:]

    def add_SP_EP(self, SP, EP):
        self.chains.update({SP : EP})

    def truncate(self, ciphertext, n):
        return ciphertext[:32 - n]

    def compute_chains(self):
        cnt = {2 : 99, 3 : 999, 4 : 9999}
        starting_point = random.randint(0, cnt[self.t / 8])
        chain_sp = self.truncate(hashlib.sha256(str(starting_point).encode("utf-8")).hexdigest(), 16)
        print(f"[+] Starting chain generation at: {chain_sp}")

        while starting_point <= cnt[self.t / 8]:

            starting_point += 1


def main():
    tmto_attack = TMTO(16)
    tmto_attack.compute_chains()

if __name__ == '__main__':
    main()
