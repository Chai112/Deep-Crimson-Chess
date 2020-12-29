#include "position.hpp"

// converts numbers to letters (e.g., 1 -> 'a')
char numToLetter (int number)
{
    return number + 'a';
}

// conversts char to int
int charToInt (char number)
{
    return number - '0';
}

// converts int to char
char intToChar (int number)
{
    return (char)number + '0';
}



// Position class
Position::Position () {}
Position::Position (int x, int y) {this->x = x; this->y = y;}
Position::~Position () {}

std::string Position::toCoords ()
{
    char xPos = numToLetter(x);
    char yPos = intToChar(y + 1);

    char output[3];
    output[0] = xPos;
    output[1] = yPos;
    output[2] = '\0'; // termination
    std::string outputStr(output);
    return outputStr;
}

// Position operator overloading 
Position Position::operator+ (const Position& positionIn)
{
    Position positionOut(
        this->x + positionIn.x,
        this->y + positionIn.y
    );
    return positionOut;
}

// Position operator overloading 
Position Position::operator- (const Position& positionIn)
{
    Position positionOut(
        this->x - positionIn.x,
        this->y - positionIn.y
    );
    return positionOut;
}

PositionPair::PositionPair ()
{
}

PositionPair::PositionPair (Position origin, Position destination)
{
    this->origin = origin;
    this->destination = destination;
}

PositionPair::~PositionPair()
{
}
