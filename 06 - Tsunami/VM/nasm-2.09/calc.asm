section .data
    calcPath db 'calc.exe', 0

section .text
    global _start

_start:
    ; Create the command line for the calculator
    mov eax, calcPath
    xor ecx, ecx
    mov cl, 0x0
    mov edx, 0x0

    ; Launch the calculator
    mov eax, 0x0B ; Windows API system call number for executing a program
    int 0x80      ; Call the operating system

    ; Exit the program
    mov eax, 0x1  ; Windows API system call number for program exit
    xor ebx, ebx
    int 0x80      ; Call the operating system