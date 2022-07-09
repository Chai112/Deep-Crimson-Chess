#ifndef board_boardloader_hpp
#define board_boardloader_hpp

#include <string>
#include <vector>
#include "piece.hpp"

class BoardLoader
{
public:
    BoardLoader(
                std::string inputFen, 
                std::string inputTurn, 
                std::string inputCastling, 
                std::string inputEnPassant
    );
    ~BoardLoader();

    // find all (legal) moves considering check
    std::vector<PositionPair> findAllLegalMoves();

private:
    // find all moves
    std::vector<PositionPair> findAllMoves();
    Board board;
};

#endif
