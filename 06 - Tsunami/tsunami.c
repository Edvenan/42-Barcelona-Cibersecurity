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
