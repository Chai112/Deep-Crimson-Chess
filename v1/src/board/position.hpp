#ifndef board_position_hpp
#define board_position_hpp

#include <string>

// converts numbers to letters (e.g., 1 -> 'a')
char numToLetter (int number);

// conversts char to int
int charToInt (char number);

// converts int to char
char intToChar (int number);

// A 2D coordinate container
struct Position
{
    int x, y;
    Position();
    Position(int x, int y);
    ~Position();

    std::string toCoords();

    // operator overloads to make life easier
    Position operator+(const Position&);
    Position operator-(const Position&);
};

struct PositionPair
{
    Position origin, destination;

    PositionPair();
    PositionPair(Position origin, Position destination);
    ~PositionPair();
};

#endif
