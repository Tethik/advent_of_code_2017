import sys
from queue import Queue
from collections import defaultdict



class Process(object):
    def __init__(self, p):
        self.sp = 0
        self.messages = Queue()
        self.other_process = None
        self.locked = False
        self.registry = defaultdict(lambda: 0)
        self.stack = list()
        self.instructions = dict()
        self.pid = p
        self.registry['p'] = p
        self.times_sent = 0
        print(self.registry)

    def step(self):
        if self.sp >= len(self.stack):
            return

        _sp = self.sp
        current = self.stack[self.sp]
        parts = current.split()

        inst = parts[0]
        args = parts[1:]

        print(self.pid, self.sp, inst, args)
        self.instructions[inst](*args)
        print(self.registry)
        print()

        self.locked = inst == "rcv" and self.sp == _sp


class Instruction(object):
    name = "nop"

    def __init__(self, process):
        self.process = process
        self.process.instructions[self.name] = self

    def value(self, y):
        try:
            return int(y)
        except:
            return self.process.registry[y]


class SetInstruction(Instruction):
    name = "set"

    def __call__(self, x, y):
        self.process.registry[x] = self.value(y)
        self.process.sp += 1



class AddInstruction(Instruction):
    name = "add"

    def __call__(self, x, y):
        self.process.registry[x] += self.value(y)
        self.process.sp += 1


class MulInstruction(Instruction):
    name = "mul"

    def __call__(self, x, y):
        self.process.registry[x] *= self.value(y)
        self.process.sp += 1


class ModInstruction(Instruction):
    name = "mod"

    def __call__(self, x, y):
        self.process.registry[x] = self.process.registry[x] % self.value(y)
        self.process.sp += 1


class JgzInstruction(Instruction):
    name = "jgz"

    def __call__(self, x, y):
        if self.value(x) > 0:
            self.process.sp += self.value(y)
        else:
            self.process.sp += 1


class RcvInstruction(Instruction):
    name = "rcv"

    def __call__(self, x):
        if not self.process.messages.empty():
            self.process.registry[x] = self.process.messages.get(block=False)
            self.process.sp += 1
        # will block until it receives. So dont advance sp.


class SndInstruction(Instruction):
    name = "snd"

    def __call__(self, x):
        print(f'sent {self.value(x)}')
        self.process.other_process.messages.put_nowait(self.value(x))
        self.process.sp += 1
        self.process.times_sent += 1




process1 = Process(0)
process2 = Process(1) # ugly
process2.other_process = process1
process1.other_process = process2

def attach_instructions(p):
    SndInstruction(p)
    SetInstruction(p)
    AddInstruction(p)
    MulInstruction(p)
    ModInstruction(p)
    RcvInstruction(p)
    JgzInstruction(p)

attach_instructions(process1)
attach_instructions(process2)


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
    process1.stack.append(line.strip())
    process2.stack.append(line.strip())

while True:
    process1.step()
    process2.step()

    print()
    print('********************************')

    if process1.locked and process2.locked:
        print('Deadlock detected')
        break

print(process1.times_sent, process2.times_sent)