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
        self.chains.update({1 : SP, 2 : EP})
        print(f"[+] Chain SP: {self.chains[1]}")
        print(f"[+] Chain EP: {self.chains[2]}")

    def truncate(self, ciphertext, n):
        return ciphertext[:32 - n]

    def compute_chains(self):
        cnt = {2 : 99, 3 : 999, 4 : 9999}
        starting_point = random.randint(0, cnt[self.t / 8])
        chain_sp = self.truncate(hashlib.sha256(str(starting_point).encode("utf-8")).hexdigest(), 16)
        print(f"[+] Starting chain generation at: {chain_sp}")

        counter = 1
        tmp = chain_sp
        while counter <= cnt[self.t / 8]:
            ciphertext = self.truncate(hashlib.sha256(str(tmp).encode("utf-8")).hexdigest(), 16)
            tmp = ciphertext
            if counter == cnt[self.t/8]:
                print(f"[+] Finished {counter} SHA256 calculations")
                print("[+] Reached end of chain calculation, storing SP and EP")
                chain_ep = tmp
                self.add_SP_EP(chain_sp, chain_ep)
            counter += 1


def main():
    tmto_attack = TMTO(16)
    tmto_attack.compute_chains()

if __name__ == '__main__':
    main()
