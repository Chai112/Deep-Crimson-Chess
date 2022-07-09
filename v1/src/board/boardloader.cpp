#include "boardloader.hpp"

#include <stdio.h>
#include <string>
#include <vector>

BoardLoader::BoardLoader(
        std::string inputFen, 
        std::string inputTurn, 
        std::string inputCastling, 
        std::string inputEnPassant
)
{
    // turn
    if (inputTurn == "w")
    {
        board.turn = PieceSide::white;
    }
    else if (inputTurn == "b")
    {
        board.turn = PieceSide::black;
    }
    else
    {
        printf("invalid turn!\n");
    }

    // castling
    board.castleWhiteKingside = false;
    board.castleWhiteQueenside = false;
    board.castleBlackKingside = false;
    board.castleBlackQueenside = false;
    for (int i = 0; i < inputCastling.length(); i++)
    {
        char currentChar = inputCastling.at(i);
        switch (currentChar)
        {
            case 'K':
                board.castleWhiteKingside = true;
                break;
            case 'Q':
                board.castleWhiteQueenside = true;
                break;
            case 'k':
                board.castleBlackKingside = true;
                break;
            case 'q':
                board.castleBlackQueenside = true;
                break;
        }
    }

    int x = 0;
    int y = 7;

    int i = 0;
    for (int i = 0; i < inputFen.length(); i++)
    {
        char currentChar = inputFen.at(i);
        if (currentChar == '/')
        {
            y--;
            x = 0;
            continue;
        }
        else
        {
            bool bFound = false;
            if (isdigit(currentChar))
            {
                // offset x by the number
                x += charToInt(currentChar) - 1;
            }
            else
            {
                PieceType pieceType = (PieceType)tolower(currentChar);

                // is piece white or black
                PieceSide pieceSide = (PieceSide)(currentChar != tolower(currentChar));

                Position pos = Position(x, y);
                Piece* piece;

                switch(pieceType)
                {
                    case pawn:
                        piece = new Pawn(pos, pieceSide);
                        break;
                    case bishop:
                        piece = new Bishop(pos, pieceSide);
                        break;
                    case knight:
                        piece = new Knight(pos, pieceSide);
                        break;
                    case rook:
                        piece = new Rook(pos, pieceSide);
                        break;
                    case queen:
                        piece = new Queen(pos, pieceSide);
                        break;
                    case king:
                        piece = new King(pos, pieceSide);
                        break;
                    default:
                        printf("piece not recognized!\n");
                        break;
                }
                board.pieces.push_back(piece);
            }
        }
        x++;
    }

    std::vector<PositionPair> allLegalMoves = findAllLegalMoves();
    for (PositionPair posPair : allLegalMoves)
    {
        printf("%s%s\n", posPair.origin.toCoords().c_str(), posPair.destination.toCoords().c_str());
    }
    /*
    for (Piece* piece : board.pieces)
    {
        piece->announce();
        std::vector<Position> output = piece->findLegalMoves(board);
        for (Position pos : output)
        {
            printf("%s%s\n", piece->position.toCoords().c_str(), pos.toCoords().c_str());
        }
    }
    */
    printf("\n");
}

BoardLoader::~BoardLoader ()
{
}

std::vector<PositionPair> BoardLoader::findAllLegalMoves()
{
    std::vector<PositionPair> allSidesMoves = findAllMoves();

    // find the king of the current side
    Piece* king;
    for (Piece* piece : board.pieces)
    {
        if (piece->getType() == PieceType::king &&
            piece->side == board.turn)
        {
            king = piece;
            break;
        }
    }

    // swap sides
    board.turn = (PieceSide)!board.turn;

    // find all moves from opposite side
    std::vector<PositionPair> allOppositeSidesMoves = findAllMoves();
    std::vector<Piece*> checkers;

    for (PositionPair posPair : allOppositeSidesMoves)
    {
        if (posPair.destination.x == king->position.x &&
            posPair.destination.y == king->position.y)
        {
            printf("%s checks king\n", posPair.origin.toCoords().c_str());
            checkers.push_back(board.getPieceAt(posPair.origin));
        }
    }
    for (Piece* piece : checkers)
    {
    }

    return allSidesMoves;
}

std::vector<PositionPair> BoardLoader::findAllMoves ()
{
    std::vector<PositionPair> allLegalMoves;
    for (Piece* piece : board.pieces)
    {
        if (piece->side != board.turn)
        {
            continue; // skip this piece as it is the wrong side
        }

        std::vector<Position> legalMoves = piece->findLegalMoves(board);
        for (Position legalPos : legalMoves)
        {
            PositionPair posPair(piece->position, legalPos);
            allLegalMoves.push_back(posPair);
        }
    }
    return allLegalMoves;
}
