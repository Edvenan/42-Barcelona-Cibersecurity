section .data
    cmdline db 'calc.exe', 0

section .text
    global _start

_start:
    ; Cargar dirección de la cadena cmdline en ECX
    mov ecx, cmdline

    ; Llamar a la función WinExec para ejecutar la calculadora
    push 0
    push ecx
    mov eax, 0x77d8ffbd  ; Dirección de la función WinExec en la biblioteca kernel32.dll
    call eax

    ; Salir del programa
    mov eax, 1
    xor ebx, ebx
    int 0x80
 