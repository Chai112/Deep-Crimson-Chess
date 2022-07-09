#ifndef board_piece_hpp
#define board_piece_hpp

#include <stdio.h>
#include <string>
#include <vector>
#include "position.hpp"

enum PieceType 
{
    pawn = 'p',
    bishop = 'b',
    knight = 'n',
    rook = 'r',
    queen = 'q',
    king = 'k',
};

enum PieceSide
{
    white = true,
    black = false,
};

class Board; // forward declaration

class Piece 
{
public:
    PieceSide side;
    Position position = Position(1,1);

    Piece();
    Piece(Position position, PieceSide side);
    ~Piece();

    // virtual keyword prevents static linkage - so it uses the child constructors yay
    // announce positons for debugging
    virtual void announce() = 0;

    // encapitsulation
    // accessors only, no mutators
    virtual PieceType getType() = 0;

    // show all legal moves
    virtual std::vector<Position> findLegalMoves(Board& board) = 0;
private:
    PieceType type;
};

class Board 
{
public:
    PieceSide turn;
    std::vector<Piece*> pieces;

    // accessors
    Piece* getPieceAt(Position position);
    bool isSquareFree(Position position);
    bool isLegal(Position position);

    // castling
    bool castleWhiteKingside = false;
    bool castleWhiteQueenside = false;
    bool castleBlackKingside = false;
    bool castleBlackQueenside = false;
};

class Pawn : public Piece
{
public:
    using Piece::Piece; // use base constructor
    PieceType type = PieceType::pawn;
    void announce();
    PieceType getType();
    std::vector<Position> findLegalMoves(Board& board);
};

class Bishop : public Piece
{
public:
    using Piece::Piece; // use base constructor
    PieceType type = PieceType::bishop;
    void announce();
    PieceType getType();
    std::vector<Position> findLegalMoves(Board& board);
};

class Knight : public Piece
{
public:
    using Piece::Piece; // use base constructor
    PieceType type = PieceType::knight;
    void announce();
    PieceType getType();
    std::vector<Position> findLegalMoves(Board& board);
};

class Rook : public Piece
{
public:
    using Piece::Piece; // use base constructor
    PieceType type = PieceType::rook;
    void announce();
    PieceType getType();
    std::vector<Position> findLegalMoves(Board& board);
};

class Queen : public Piece
{
public:
    using Piece::Piece; // use base constructor
    PieceType type = PieceType::queen;
    void announce();
    PieceType getType();
    std::vector<Position> findLegalMoves(Board& board);
};

class King : public Piece
{
public:
    using Piece::Piece; // use base constructor
    PieceType type = PieceType::king;
    void announce();
    PieceType getType();
    std::vector<Position> findLegalMoves(Board& board);
};

#endif
