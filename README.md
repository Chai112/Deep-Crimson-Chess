# SHCR - SHallow CRimson Chess Engine
### AI/ML chess engine developed by Chaidhat Chaimongkol
### Version 2 started on 9 June, 2022

# Promises
-   100 percent my code - not copied from anywhere
-   I will not examine Stockfish or any other engine's code
-   No book moves were manually inputted which weren't calculated by the engine.

# Early Ideas/Concepts
## Concept 1: Brute Force/ Monte Carlo Search
Sounds reasonable.

## Concept 2: Evaluate Positions via DNN
Using dataset 2, train a classical NN to look at multiple positions and stockfish analysis for it.
Once it is trained, then do monte carlo search of low depth to figure out the best move to improve position.
Optimally, train for only moving as black or white.

### Concept 2.0.1: Evaluate Both Sides
Using concept 2.0, the system would only evaluate one side (black to move). This is bad when trying to see which moves in evaluating moves of the engine as it would be white to move afterwards. Need to to train a different AI to understand white to move. Or to make it fairer, accept both white AND black in training data. Or when evaluating, perform both steps and then consult engine (depth 2) instead of comapring the best move for black.

### Concept 2.1: Position Features Crosses
Create some feature crosses inorder to inform the NN some important things (how many pieces are left, position of pieces, ranks open, pieces being attacked/defended, etc)
Possibly have two NNs, one bigger one which takes in the evaluation of the smaller NN, which evaluates positions

* value of pieces on the board 1 (to give piece-based evaluations)
* number of pieces on the board 1 (to identify whether game is endgame etc)
* number of defenders/attackers on each square 8x8 (to maximize attack/defense)
* positional evaluation of second NN 1 (optional)

### Concept 2.2: Evaluate Positions via use a CNN
Chuck it in a CNN and hopefully it works. A test CNN project would be nice to start with just to check it works for other datasets.


## Concept 3: Evaluate Best Next Move
Using dataset 1, train it to compare two moves and then output how confident the AI is that it is a good move.

* have to reformat PGN to FEN in dataset 1
* have to create random wrong moves in dataset 1
* training does not have any inbetween moves (such as semi-good moves)

## Concept 4: Reinforcement Learning
Deep Q-Learning and stuff - looks hard!
See https://www.youtube.com/watch?v=gWNeMs1Fb8I&list=PLXO45tsB95cIplu-fLMpUEEZTwrDNh6Ba&index=4

# Development Logs
### Test #1: Commit 20
```
dataset: chessData-endgame 
time to train: ~10s
epochs: 50
final loss: ~5e-04
final accuracy: 0.0341
dimensions: 64x2 16x2 8x2 4x4
```
using concept 2, training for 50 epochs using a rather larger NN, it can start to tell the difference between who is winning. If a white pawn is very far up the rank, it gives a favourable chance to white of winning (around 0.74, equivalent to 48 pawns up). However sometimes it does not give equal piece advantages. For example, if black a lot of pawns and knights whereas white does not, it only gives a advantage to black (like around 0.43 (-14 pawns)). Obviously, it is exagerrating the numbers of pawns, but it may be the result of stockfish giving very exagerrated evaluations during endgames (bad data) and also when it is "mate in", it awards 1.0 (100 pawns up). It may be a better idea to use sigmoid instead.

Adding too many neurons causes the loss to stick at 0.175 and move very slowly (no! This is probably because it converged prematurely due to a bad initial condition. Other tests work well.)

### Test #2

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

### Test #3
The same as the previous one, but using sigmoid instead of reLU
Loss converges slower than with a ReLU but not by a significant amount. Seems to have no immediate benefit and probably not worth it. I changed it back to ReLU and even the final layer of the output should be a ReLU instead of a sigmoid. Hopefully this makes the final evaluation less extreme.

### Test 4
Different dimensions to Test 3
```
dataset: chessData-endgame 
time to train: ~10s
epochs: 50
final loss: ~4.2e-04
final accuracy: 0.0341
dimensions: 64x2 16x2 6x8
```

It does not recognise the pawn being high up the rank unlike the previous ones. By being up in material, it can sense that it is winning or losing but again, it does not really mind about material. Maybe the positions in the dataset are not random enough? Then again, it is hard to tell whether it is better or worse than the previous models.

### Test 5
Changed Batch size to 100 and many new things
```
dataset: chessData-small
time to train: ~18s
epochs: 50
final loss: 0.0167
final accuracy: 0.433
test loss: 0.082
test accuracy: 0.576
dimensions: 64x4 16x4 8x8
```
Performs really badly! It seems to have no concept of who is winning or losing. It seems something is wrong with the code

### Test 6
Fixed errors with the code. Now trying tanh instead of ReLU and using negative numbers. Blank squares are still 0.0, not -1
```
dataset: chessData-verysmall
time to train: ~1s
epochs: 50
final loss: 1.5e-04
final accuracy: 0.1140
test loss: 0.0347
test accuracy: 0.06
correct side: 35%
dimensions: 64x2 16x2 8x4
```
Not bad. It can evaluate positions of a full board fairly well, although still makes mistakes and doesnt not evaluate the bishop as 3 points, for example.

### Test 7
Removed the extra info thing as it is not quite useful
```
dataset: chessData-verysmall
time to train: ~1s
epochs: 50
final loss: 7.22e-05
final accuracy: 0.114
test loss: 0.043
test accuracy: 0.06
correct side: 70%
dimensions: 64x2 16x2 8x4
```
Appears to work very well in telling what side is which! But this is at a quick glance. For more nuanced positions, it still struggles a bit.

### Test 8
Ran with small dataset overnight. It stopped prematurely. The settings were lost so a lot of the values are unknown.
```
dataset: chessData-small
time to train: ?
epochs: 194 
final loss: ? (estimated around 0.0001)
final accuracy: ?
test loss: ?
test accuracy: ?
correct side: ?
dimensions: 64x2 16x2 8x4
```
very cool! Works fairly well with everything. Can analyze endgames and normal games but at some points it cannot state how much white or black is winning by in the endgame.

### Test 8 Bravo
Ran with small dataset overnight.
```
dataset: chessData-small
time to train: 21802s (6hrs, 3min)
epochs: 1000
final loss: 5.419e-04
final accuracy: 0.1283
test loss: 0.013952
test accuracy: 0.127
correct side: 54.2%
dimesnions: 64x2 16x2 8x4
```
again, very cool. However, in the opening it cannot precisely determine who is winning. I am starting to realise that in context, the absolute evaluations do not mean a lot. Actually, the relative evaluation between moves determine which move is best to be played (black is trying to minimize the evaluation) so the lowest number should be the best next move: this means the absolute evaluation accuracy is not as relevant. The engine struggles to identify moves which results in the immediate taking of the piece (it says a good move is black bishop infront of a white pawn) Additionally, proposed concept 2.0.1 and 2.2.