from microqiskit import QuantumCircuit, simulate
import random
import numpy as np
import math

class bb84:
    #TODO - maybe seperate classes into bob and alice

    def __init__(self, n):
        #self.qc = device
        self.n = n

        self.e_t = 0
        self.e_m = 0

        self.p = 0.1

        self.alice_bits = []
        self.alice_bases = []

        self.bob_bases = []
        self.bob_bits = []


    def run_protocol(self, distance):
        #alice_bits = randint(2, size=self.n)
        #alice_bases = randint(2, size=self.n)

        n_sent = 0
        n_received = 0

        while n_received < self.n:          #alice prepares random bits in random bases and sends them to bob
            qc = QuantumCircuit(1,1)
            alice_bit = random.choice("01")
            self.alice_bits.append(alice_bit)
            alice_base = random.choice("zx") #TODO: could make user choice?
            self.alice_bases.append(alice_base)
            if alice_base == "z": # Prepare qubit in Z-basis
                if alice_bit == "0":
                    pass 
                else:
                    qc.x(0)
            else: # Prepare qubit in X-basis
                if alice_bit == "0":
                    qc.h(0)
                else:
                    qc.x(0)
                    qc.h(0)
            n_sent += 1
            print("sent:", n_sent)
            n_received += self.send(qc, loss=min(self.p * math.exp(distance-1), 1)) #loss scales exponentially with distance
            print("received:", n_received)

        print("Alice: 'my bases were\t", self.alice_bases, "'")
        print("Bob: 'my bases were\t", self.bob_bases, "'")
        key_indexes = input("What are the indexes of the ones that were the same?").split() #maybe add a check?
        #key = [self.alice_bases[i] for i in range(self.n) if str(i) in key_indexes]
        new_a_bits = [self.alice_bits[i] for i in range(self.n) if str(i) in key_indexes]
        new_b_bits = [self.bob_bits[i] for i in range(self.n) if str(i) in key_indexes]




        k = int(input("how much of your key do you want to publish to check with Bob?"))
        print("Alice: 'here are my first", k, " bits:\t", new_a_bits[:k], "'")
        print("Bob: 'ok, here are mine:\t", new_b_bits[:k])

        if "y" not in input("do they match"):
            print("then we have failed")
        else:
            print("success! We shall use the rest of our bits as our secret key!!")
            key = new_a_bits[k:]


    def send(self, qc, loss=0.1):
        if random.random() < self.e_t: 
            qc.x(0)
            qc.z(0)
            print("qubit was contaminated")

        if random.random() > loss:
            self.b_measure(qc)
            return 1
        else:
            self.bob_bases.append(-1)
            self.bob_bits.append(-1)
            return 0 # qubit didnt make the journey

    def b_measure(self, qc):
        bob_base = random.choice("zx")
        self.bob_bases.append(bob_base)
        if bob_base == 'x': qc.h(0)
        qc.measure(0,0)
        counts = simulate(qc, shots=1)
        result = '1' in counts
        if random.random() < self.e_m: result = not(result)
        self.bob_bits.append(int(result))


