import math
import hashlib

class TMTO:
    def __init__(self, t):
        self.t = t
        self.modulus = 2^self.t
        self.chains = {}

    def add_SP_EP(self, SP, EP):
        self.chains.update({SP : EP})

    def compute_chains(self):
        pass

def main():
    tmto_attack = TMTO(16)
    tmto_attack.compute_chains()

if __name__ == '__main__':
    main()
