# SHCR - SHallow CRimson Chess Engine
### AI/ML chess engine developed by Chaidhat Chaimongkol
### Version 2 started on 9 June, 2022

# Promises
-   100 percent my code - not copied from anywhere
-   I will not examine Stockfish or any other engine's code
-   No book moves were manually inputted which weren't calculated by the engine.

# Early Ideas/Concepts
### Concept 1: Brute Force/ Monte Carlo Search
Sounds reasonable.

### Concept 2: Evaluate Positions via DNN
Using dataset 2, train a classical NN to look at multiple positions and stockfish analysis for it.
Once it is trained, then do monte carlo search of low depth to figure out the best move to improve position.
Optimally, train for only moving as black or white.

### Concept 3: Evaluate Best Next Move
Using dataset 1, train it to compare two moves and then output how confident the AI is that it is a good move.

* have to reformat PGN to FEN in dataset 1
* have to create random wrong moves in dataset 1
* training does not have any inbetween moves (such as semi-good moves)

### Concept 4: Reinforcement Learning
Deep Q-Learning and stuff - looks hard!
See https://www.youtube.com/watch?v=gWNeMs1Fb8I&list=PLXO45tsB95cIplu-fLMpUEEZTwrDNh6Ba&index=4

# Development Logs
### Commit 20: 
```
dataset: chessData-endgame 
time to train: ~10s
epochs: 50
final loss: ~5e-04
final accuracy: 0.0341
dimensions: 64x2 16x2 8x2 4x4
```
using concept 2, training for 50 epochs using a rather larger NN, it can start to tell the difference between who is winning. If a white pawn is very far up the rank, it gives a favourable chance to white of winning (around 0.74, equivalent to 48 pawns up). However sometimes it does not give equal piece advantages. For example, if black a lot of pawns and knights whereas white does not, it only gives a advantage to black (like around 0.43 (-14 pawns)). Obviously, it is exagerrating the numbers of pawns, but it may be the result of stockfish giving very exagerrated evaluations during endgames (bad data) and also when it is "mate in", it awards 1.0 (100 pawns up). It may be a better idea to use sigmoid instead.

Adding too many neurons causes the loss to stick at 0.175 and move very slowly

### Commit 21:

The same as the previous one but with altered dimensions
```
dataset: chessData-endgame 
time to train: ~10s
epochs: 50
final loss: ~3.8e-04
final accuracy: 0.0341
dimensions: 64x2 16x4
```
This one proved to be somewhat the same as the old one, expect with a lower loss value (better). It can obviously tell which side is winning based on material. However, it cannot really accurately tell which side is winning by how much. For example, if white has a queen and black has only the king, it says it could be around 4 pawns up but if the black king moves around the board on the black side, its evaluation still says that white is ahead, but the value shifts by a lot. If black has a really obvious amount of material up, especially with rooks or queens, it will say that black is winning and vice versa and will state it is winning by quite a margin. Did not test the pawn rank thing, but will be interesting to try.