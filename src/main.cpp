#include <stdio.h>
#include <string>
#include <vector>

#include "board/boardloader.hpp"

int main (int argc, char* argv[])
{
    // no inputs
    if (argc == 1)
    {
        printf("\n");
        printf("\n");
        printf("\n");
        printf("Please give a FEN as an argument. This will return the best move as a FEN back.\n");
        printf("Made by Chaidhat Chaimongkol.\n");
        printf("\n");
        printf("Promises:\n");
        printf("- 100 percent my code - not copied from anywhere.\n");
        printf("- I will not closely examine Stockfish or any other engine's code.\n");
        printf("- No book moves were used which weren't calculated by the engine.\n");
        printf("\n");
        printf("\n");
        printf("\n");
    }
    // one or more input
    else if (argc == 7)
    {
        std::string inputFen(argv[1]);
        std::string inputTurn(argv[2]);
        std::string inputCastling(argv[3]);
        std::string inputEnPassant(argv[4]);
        BoardLoader chessBoard = BoardLoader(inputFen, inputTurn, inputCastling, inputEnPassant);
    }
    else
    {
        printf("invalid FEN!!! Copy paste THE ENTIRE THING.\n");
    }
    return 1;
}
