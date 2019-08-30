"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.hlt = False

        self.ops ={
            LDI: self.op_ldi,
            HLT: self.op_hlt,
            MUL: self.op_mul,
            PRN: self.op_prn
        }
    
    def ram_read(self,mar):
        return self.ram[mar]

    def ram_write(self,mar,mdr):    
        self.ram[mar] = mdr


    def op_ldi(self,addr,val):
        self.reg[addr] = val

    def op_mul(self,addr1,addr2):
        self.alu("MUL",addr1,addr2)

    def op_hlt(self,op_a,op_b):
        self.hlt = True
    
    def op_prn(self,addr,op_b):
        print(self.reg[addr])

    def load(self,filename):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
        with open(filename) as file:
            for line in file:
                comment_split = line.split('#')
                instruction = comment_split[0]

                if instruction == '':
                    continue
                first_bit = instruction[0]
                if first_bit == '0' or first_bit == '1':
                    self.ram[address] = int(instruction[:8],2)
                    address += 1



    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # LDI = 0b10000010
        # PRN = 0b01000111
        # HLT = 0b00000001

        while not self.hlt:
            ir = self.ram_read(self.pc)
            op_a = self.ram_read(self.pc + 1)
            op_b = self.ram_read(self.pc + 2)
            op_size = ir >> 6
            ins_set = ((ir >> 4) & 0b1) == 1
            if ir in self.ops:
                self.ops[ir](op_a,op_b)
            if not ins_set:
                self.pc += op_size + 1

