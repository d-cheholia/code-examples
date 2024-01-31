#include <iostream>
#include <chrono>
#include <format>

int main(   )   {
    // Get the current time point from the system clock
    auto now =    std::chrono::system_clock::now( );

    // Convert time_point to a time_t for compatibility with traditional C++ time functions
    auto current_time = std::chrono::system_clock::to_time_t(now);

    // Format the time as a human-readable string
    std::string time_str = std::format("{:%Y-%m-%d %H:%M:%S}", *std::localtime(&current_time));

    std::cout << "Current time: " << time_str << std::endl;

    return 0;
}
