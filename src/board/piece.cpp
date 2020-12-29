#include "piece.hpp"
#include "boardloader.hpp"

Piece::Piece ()
{
}

Piece::Piece (Position position, PieceSide side)
{
    this->position = position;
    this->side = side;
}

Piece* Board::getPieceAt(Position position)
{
    // check positions are in range
    if (!(
        (position.x >= 0 && position.x <= 7) &&
        (position.y >= 0 && position.y <= 7)
       ))
    {
        // invalid position
        return nullptr;
    }

    // find the piece
    for (Piece* piece : pieces)
    {
        if (piece->position.x == position.x &&
            piece->position.y == position.y)
        {
            // return the piece which positions matches
            return piece;
        }
    }
    // not found (return false)
    return nullptr;
}

bool Board::isLegal(Position position)
{
    // check positions are in range
    if (!(
        (position.x >= 0 && position.x <= 7) &&
        (position.y >= 0 && position.y <= 7)
       ))
    {
        // invalid position
        return false;
    }
    Piece* pieceAt = getPieceAt(position);
    if (pieceAt)
    {
        if (pieceAt->side == turn)
        {
            // cannot take your own pieces
            return false;
        }
    }
    // ok position
    return true;
}

bool Board::isSquareFree(Position position)
{
    // check positions are in range
    if (!(
        (position.x >= 0 && position.x <= 7) &&
        (position.y >= 0 && position.y <= 7)
       ))
    {
        // invalid position
        return false;
    }

    // find the piece
    for (Piece* piece : pieces)
    {
        if (piece->position.x == position.x &&
            piece->position.y == position.y)
        {
            if (piece->getType() == PieceType::king)
            {
                // kings are transparent
                return true;
            }
            // there is a piece there
            return false;
        }
    }
    return true;
}

std::vector<Position> Pawn::findLegalMoves(Board& board)
{
    std::vector<Position> legalMoves;
    Position testPos;
    // is there a piece at ahead and to the left?
    // capturable
    testPos = Position(position + Position(-1, side ? 1 : -1));
    if (!board.isSquareFree(testPos) && board.isLegal(testPos))
    {
        legalMoves.push_back(testPos);
    }
    // is there a piece at ahead and to the right?
    // capturable
    testPos = Position(position + Position(1, side ? 1 : -1));
    if (!board.isSquareFree(testPos) && board.isLegal(testPos))
    {
        legalMoves.push_back(testPos);
    }

    // is there a piece ahead?
    testPos = Position(position + Position(0, side ? 1 : -1));
    // is it free?
    if (board.isSquareFree(testPos))
    {
        legalMoves.push_back(testPos);
    }

    // is there a piece two moves ahead?
    if ((position.y == 1  && side) || // the piece must be either on 2nd or 6th rank, black and white respectively
        (position.y == 6 && !side))
    {

        testPos = Position(position + Position(0, side ? 2 : -2));
        // is it free?
        if (board.isSquareFree(testPos))
        {
            legalMoves.push_back(testPos);
        }
    }

    return legalMoves;
}

std::vector<Position> Bishop::findLegalMoves(Board& board)
{
    std::vector<Position> legalMoves;
    Position testPos;

    // top right
    testPos = position;
    do 
    {
        testPos = testPos + Position(1, 1);
        if (board.isLegal(testPos))
            legalMoves.push_back(testPos);
    } while (board.isSquareFree(testPos));
    // top left
    testPos = position;
    do 
    {
        testPos = testPos + Position(-1, 1);
        if (board.isLegal(testPos))
            legalMoves.push_back(testPos);
    } while (board.isSquareFree(testPos));
    // bottom right
    testPos = position;
    do 
    {
        testPos = testPos + Position(1, -1);
        if (board.isLegal(testPos))
            legalMoves.push_back(testPos);
    } while (board.isSquareFree(testPos));
    // bottom left
    testPos = position;
    do 
    {
        testPos = testPos + Position(-1, -1);
        if (board.isLegal(testPos))
            legalMoves.push_back(testPos);
    } while (board.isSquareFree(testPos));

    return legalMoves;
}

std::vector<Position> Knight::findLegalMoves(Board& board)
{
    std::vector<Position> legalMoves;
    Position testPositions[] = {
        Position(-1, 2),
        Position(-2, 1),
        Position(1, 2),
        Position(2, 1),
        Position(-1, -2),
        Position(-2, -1),
        Position(1, -2),
        Position(2, -1),
    };

    for (Position testPos : testPositions)
    {
        // is there a piece ahead?
        testPos = Position(position + testPos);
        // is it free?
        if (board.isSquareFree(testPos))
        {
            // add the move as legal
            legalMoves.push_back(testPos);
        }
    }
    return legalMoves;
}

std::vector<Position> Rook::findLegalMoves(Board& board)
{
    std::vector<Position> legalMoves;
    Position testPos;

    // up
    testPos = position;
    do 
    {
        testPos = testPos + Position(0, 1);
        if (board.isLegal(testPos))
            legalMoves.push_back(testPos);
    } while (board.isSquareFree(testPos));
    // right
    testPos = position;
    do 
    {
        testPos = testPos + Position(1, 0);
        if (board.isLegal(testPos))
            legalMoves.push_back(testPos);
    } while (board.isSquareFree(testPos));
    // down
    testPos = position;
    do 
    {
        testPos = testPos + Position(0, -1);
        if (board.isLegal(testPos))
            legalMoves.push_back(testPos);
    } while (board.isSquareFree(testPos));
    // left
    testPos = position;
    do 
    {
        testPos = testPos + Position(-1, 0);
        if (board.isLegal(testPos))
            legalMoves.push_back(testPos);
    } while (board.isSquareFree(testPos));
    return legalMoves;
}

std::vector<Position> Queen::findLegalMoves(Board& board)
{
    std::vector<Position> legalMoves;
    Position testPos;

    // BISHOP
    // top right
    testPos = position;
    do 
    {
        testPos = testPos + Position(1, 1);
        if (board.isLegal(testPos))
            legalMoves.push_back(testPos);
    } while (board.isSquareFree(testPos));
    // top left
    testPos = position;
    do 
    {
        testPos = testPos + Position(-1, 1);
        if (board.isLegal(testPos))
            legalMoves.push_back(testPos);
    } while (board.isSquareFree(testPos));
    // bottom right
    testPos = position;
    do 
    {
        testPos = testPos + Position(1, -1);
        if (board.isLegal(testPos))
            legalMoves.push_back(testPos);
    } while (board.isSquareFree(testPos));
    // bottom left
    testPos = position;
    do 
    {
        testPos = testPos + Position(-1, -1);
        if (board.isLegal(testPos))
            legalMoves.push_back(testPos);
    } while (board.isSquareFree(testPos));

    // ROOK
    // up
    int i; // offset to prevent pushing the same squares.
    i = 0;
    testPos = position;
    do 
    {
        testPos = testPos + Position(0, 1);
        if (board.isLegal(testPos) && i++ > 1)
            legalMoves.push_back(testPos);
    } while (board.isSquareFree(testPos));
    // right
    i = 0;
    testPos = position;
    do 
    {
        testPos = testPos + Position(1, 0);
        if (board.isLegal(testPos) && i++ > 1)
            legalMoves.push_back(testPos);
    } while (board.isSquareFree(testPos));
    // down
    i = 0;
    testPos = position;
    do 
    {
        testPos = testPos + Position(0, -1);
        if (board.isLegal(testPos) && i++ > 1)
            legalMoves.push_back(testPos);
    } while (board.isSquareFree(testPos));
    // left
    i = 0;
    testPos = position;
    do 
    {
        testPos = testPos + Position(-1, 0);
        if (board.isLegal(testPos) && i++ > 1)
            legalMoves.push_back(testPos);
    } while (board.isSquareFree(testPos));
    return legalMoves;
}

std::vector<Position> King::findLegalMoves(Board& board)
{
    std::vector<Position> legalMoves;
    Position testPositions[] = {
        Position(0, 1),
        Position(1, 1),
        Position(1, 0),
        Position(1, -1),
        Position(0, -1),
        Position(-1, -1),
        Position(-1, 0),
        Position(-1, 1),
    };

    for (Position testPos : testPositions)
    {
        // is there a piece ahead?
        testPos = Position(position + testPos);
        // is it free?
        if (board.isSquareFree(testPos))
        {
            // add the move as legal
            legalMoves.push_back(testPos);
        }
    }
    return legalMoves;
}

void Pawn::announce ()
{
    printf("type: %c, pos: %s\n", side ? toupper(type) : type, position.toCoords().c_str());
}

void Bishop::announce ()
{
    printf("type: %c, pos: %s\n", side ? toupper(type) : type, position.toCoords().c_str());
}

void Knight::announce ()
{
    printf("type: %c, pos: %s\n", side ? toupper(type) : type, position.toCoords().c_str());
}

void Rook::announce ()
{
    printf("type: %c, pos: %s\n", side ? toupper(type) : type, position.toCoords().c_str());
}

void Queen::announce ()
{
    printf("type: %c, pos: %s\n", side ? toupper(type) : type, position.toCoords().c_str());
}

void King::announce ()
{
    printf("type: %c, pos: %s\n", side ? toupper(type) : type, position.toCoords().c_str());
}

PieceType Pawn::getType()
{
    return PieceType::pawn;
}

PieceType Bishop::getType()
{
    return PieceType::bishop;
}

PieceType Knight::getType()
{
    return PieceType::knight;
}

PieceType Rook::getType()
{
    return PieceType::rook;
}

PieceType Queen::getType()
{
    return PieceType::queen;
}

PieceType King::getType()
{
    return PieceType::king;
}

