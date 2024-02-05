#include <iostream>

int main( void    )      {
    size_t one;
    size_t two;
    size_t sum;
    std::cout << "Enter the first number: ";
    std::cin >> one;
    std::cout << "Enter the second number: ";
    std::cin >> two;
    sum = one + two;
    std::cout << "The sum of " << one << " and " << two << " is " << sum << std::endl;
 }