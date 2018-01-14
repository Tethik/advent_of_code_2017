import sys
from collections import defaultdict

instructions = dict()

class Process(object):
    registry = defaultdict(lambda: 0)
    stack = list()
    sp = 0
    sounds_played = list()


    def process(self):
        while self.sp < len(self.stack):
            _sp = self.sp
            current = self.stack[self.sp]
            parts = current.split()

            inst = parts[0]
            args = parts[1:]

            print(inst, args)
            instructions[inst](*args)
            print(self.registry)
            print()
            # print(self.sp)

            if _sp == self.sp: # dont move stack pointer if we performed a jump
                self.sp += 1


process = Process()

class Instruction(object):
    name = "nop"

    def __init__(self, process):
        self.process = process
        instructions[self.name] = self

    def value(self, y):
        try:
            return int(y)
        except:
            return self.process.registry[y]

class SndInstruction(Instruction):
    name = "snd"

    def __call__(self, x):
        self.process.last_sound_played = self.process.registry[x]

SndInstruction(process)

class SetInstruction(Instruction):
    name = "set"

    def __call__(self, x, y):
        self.process.registry[x] = self.value(y)

SetInstruction(process)

class AddInstruction(Instruction):
    name = "add"

    def __call__(self, x, y):
        self.process.registry[x] += self.value(y)

AddInstruction(process)

class MulInstruction(Instruction):
    name = "mul"

    def __call__(self, x, y):
        self.process.registry[x] *= self.value(y)

MulInstruction(process)

class ModInstruction(Instruction):
    name = "mod"

    def __call__(self, x, y):
        self.process.registry[x] = self.process.registry[x] % self.value(y)

ModInstruction(process)

class RcvInstruction(Instruction):
    name = "rcv"

    def __call__(self, x):
        if self.process.registry[x] > 0:
             print(self.process.last_sound_played)
             self.process.sp = 1337

RcvInstruction(process)

class JgzInstruction(Instruction):
    name = "jgz"

    def __call__(self, x, y):
        if self.process.registry[x] > 0:
             self.process.sp += self.value(y)


JgzInstruction(process)

# process.stack = """
# set a 1
# add a 2
# mul a a
# mod a 5
# snd a
# set a 0
# rcv a
# jgz a -1
# set a 1
# jgz a -2
# """.strip().split('\n')
# print(process.stack)

for line in sys.stdin:
    process.stack.append(line.strip())

process.process()
