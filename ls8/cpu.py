"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
CMP = 0b10000010
JMP = 0b01000111
JEQ = 0b00000001
JNE = 0b10100010
RET = 0b00010001

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.FL = 0b00000000
        self.hlt = False

        self.ops ={
            LDI: self.op_ldi,
            HLT: self.op_hlt,
            MUL: self.op_mul,
            PRN: self.op_prn,
            JMP: self.op_jmp,
            CMP: self.op_cmp,
            JEQ: self.op_jeq,
            JNE: self.op_jne,
            RET: self.op_ret


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
    
    def op_jne(self,op_a,op_b):
        flag = (self.FL & 0b1) == 1
        if not flag:
            self.op_jmp(op_a,op_b)

    def op_cmp(self,addr1,addr2):
        self.alu("CMP",addr1,addr2)

    def op_jmp(self,op_a,op_b):
        register_address = self.ram[op_a]
        address_to_jump_to = self.reg[register_address]
        self.pc = address_to_jump_to

    def op_ret(self,op_a,op_b):
        SP = self.reg[7]
        address_to_return_to = self.ram[SP]
        self.reg[7] = (SP + 1) % 243

    def op_jeq(self,op_a,op_b):
        flag = (self.FL & 0b1) == 1
        if flag:
            self.op_jmp(op_a,op_b)


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
        print(self.reg[reg_a],"here")
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] > self.reg[reg_b]:
                print(self.reg[reg_a])
                self.FL = 0b00000010
            if self.reg[reg_a] == self.reg[reg_b]:
                self.FL = 0b00000001
            if self.reg[reg_a] < self.reg[reg_b]:
                self.FL = 0b00000100
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

