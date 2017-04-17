# Stack Machine for my Own Assembly Language

Code: Byte array, created by comp, executed in runtime
Data: Byte array, allocated by compiler, used during runtime
Stack: array of ?, bytes is best, but we can use a union to show
Heap: ? (dynamic memory is a big separate topic)

Registers: 
	IP - instruction pointer (index -> code)
			for compilation: allocation
			for execution: current instruction
	DP - data ptr, alloc only
	SP - stack ptr, runtime only
	BP - base ptr, runtime only

void run(){
	ip = 0
	while (1){
		switch (code[ip++]){
			case:
			...
		}
	}
}

Use symbolic names for instructions
\#define op\_push 1
\#define op\_pop 2
...

Instructions:
1) data movement
   - push [1|4]bytes - [push|addr]
   - pop  [1|4]bytes - [pop|addr]
   - pushi [1|4]bytes - [pushi|val]
   - xchg [1] - swap top 2 on stack
   - dup [1] - dup top elt on stack
   - remove [1] - pop junk
2) arith
   - add [1]
   - fadd \[1\] (floating point version is implied for others)
   - sub
   - mul
   - div
   - mod
   - and
   - or
   - shiftl
   - shiftr
   - neg
   - not
   - cvr
   - cvi
   - eql
   - neq
   - lss
   - gtr
   - leq
   - geq
3) Jumps 
	- jmp [1|4]bytes - [JMP|addr]
	assign to ip the address
	- jfalse - same but takes argument from stack
	- jtrue - ""
	- call
	- ret
	- jtab
	- halt
4) I/O
	- print\_int
	- ...

5) Others
	- sin

case op\_push:
	int a = *(int*)(code + ip);
	ip += sizeof(int)
	int v = *(int*)(data + a);
	stack[sp++].i = v;

case op\_add:
	sp--;
	stack[sp].i += stack[sp-1].i;
	break;

case op\_eql:
	sp--;
	stack[sp].i = (stack[sp].i == stack[sp-1].i);
	break;

case op\_halt:
	exit()

