import math
import hashlib
import random

class TMTO:
    def __init__(self, t):
        self.t = t
        self.modulus = 2^self.t
        self.cnt = {2 : 2**16, 3 : 999, 4 : 9999}
        self.chains = {}

    def decimal_to_bin(self, n):
        return bin(n)[2:]

    def add_SP_EP(self, SP, EP):
        self.chains.update({1 : SP, 2 : EP})
        print(f"[+] Chain SP: {self.chains[1]}")
        print(f"[+] Chain EP: {self.chains[2]}")

    def truncate(self, ciphertext, n):
        return ciphertext[:n]

    def recompute_chain(self, SP, sha_hash):
        print(f"[+] Re-computing the chain now looking for {sha_hash}")
        tmp = SP
        print(f"Starting at {SP}")
        cnt = 0
        while cnt < self.cnt[self.t / 8]:
            ciphertext = self.truncate(hashlib.sha256(str(tmp).encode("utf-8")).hexdigest(), 4)
            print(ciphertext)
            if ciphertext == sha_hash:
                print("[+] We hit an endpoint")
                return tmp #this is the previous input to SHA256 and the plaintext
            tmp = ciphertext
            cnt += 1

    def compute_chains(self):
        starting_point = random.randint(0, self.cnt[self.t / 8])
        chain_sp = self.truncate(hashlib.sha256(str(starting_point).encode("utf-8")).hexdigest(), 4)
        print(f"[+] Starting chain generation at: {chain_sp}")

        counter = 1
        tmp = chain_sp
        while counter <= self.cnt[self.t / 8]: #99 since we truncate SHA256 hash to 16 bits
            ciphertext = self.truncate(hashlib.sha256(str(tmp).encode("utf-8")).hexdigest(), 4)
            tmp = ciphertext
            if counter == self.cnt[self.t/8]:
                print(f"[+] Finished {counter} SHA256 calculations")
                print("[+] Reached end of chain calculation, storing SP and EP")
                chain_ep = tmp
                self.add_SP_EP(chain_sp, chain_ep)
            counter += 1

    def find_preimage(self, sha_hash):
        print("[+] Now attempting to find pre-image")
        tmp = sha_hash
        counter = 0
        while counter <= self.cnt[self.t/8]:
            tmp = self.truncate(hashlib.sha256(str(tmp).encode("utf-8")).hexdigest(), 4)
            if self.chains[2] == tmp:
                print(f"[+] Found endpoint {tmp} re-computing chain now")
                plaintext = self.recompute_chain(self.chains[1], sha_hash)
                print(f"[+] Recovered plaintext {plaintext} for hash {sha_hash} verifying...")
                return

            counter += 1

'''
Description: Driver code for the attack
'''
def main():
    tmto_attack = TMTO(16)
    tmto_attack.compute_chains()
    tmto_attack.find_preimage("55e1")

if __name__ == '__main__':
    main()
