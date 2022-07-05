# SHCR - SHallow CRimson Chess Engine
### AI/ML chess engine developed by Chaidhat Chaimongkol
### Version 2 started on 9 June, 2022

# Promises
- Program must evaluate moves by itself (no using Stockfish/other engines during runtime)
- Program must not use book moves
- No closely copying ideas/code from Stockfish or any other well-known engines

Extra handicap opportunity:
- The computer should have 1/10th of the time of the human.

# Early Ideas/Concepts
## Concept 1: Brute Force/ Monte Carlo Search/Min-max/Alpha-beta pruning
Sounds reasonable.

## Concept 2: Evaluate Positions via DNN
Using dataset 2, train a classical NN to look at multiple positions and stockfish analysis for it.
Once it is trained, then do monte carlo search of low depth to figure out the best move to improve position.
Optimally, train for only moving as black or white.

### Concept 2.0.1: Evaluate Both Sides
Using concept 2.0, the system would only evaluate one side (black to move). This is bad when trying to see which moves in evaluating moves of the engine as it would be white to move afterwards. Need to to train a different AI to understand white to move. Or to make it fairer, accept both white AND black in training data. Or when evaluating, perform both steps and then consult engine (depth 2) instead of comapring the best move for black.

### Concept 2.1: Position Features
Create some feature inorder to inform the NN some important things

Material:
* `pawns_remaining (1)` - number of pawns on the board (1 is {9 white, 0 black}, -1 is {0 white, 9 black})
* `knights_remaining (1)` - number of knights on the board (1 is {2 white, 0 black}, -1 is {0 white, 2 black})
* `bishops_remaining (1)` - number of bishops on the board (1 is {2 white, 0 black}, -1 is {0 white, 2 black})
* `queens_remaining (1)` - number of queens on the board (1 is {1 white, 0 black}, -1 is {0 white, 1 black})

Features (for white):
* `activity_white (8x8)` - number of available legal white move squares
* `activity_white_sum (1)` - sum of above
* `defense_white (1)` - value of white pieces are being defended by other white pieces
* `pressure_white (1)` - value of pieces white are attacking, ignoring pieces blocking other pieces
* `attack_white (1)` - value of white pieces are legally attacking black pieces
* `is_white_castled (1)` - determine safety of opposite side
* `white_check (1)` - is white in check right now?

Features (for black):
* `activity_black (8x8)`
* `activity_black_sum (1)`
* `defense_black (1)`
* `pressure_black (1)`
* `attack_black (1)`
* `is_black_castled (1)`
* `black_check (1)`

16 + 8*8*2 = 144 features

Possibly combine with the hot encoding of pieces seen on the first one.


### Concept 2.2: Evaluate Positions via use a CNN
Chuck it in a CNN and hopefully it works. A test CNN project would be nice to start with just to check it works for other datasets.

04/07/22: Found an [interesting youtube video](https://www.youtube.com/watch?v=ffzvhe97J4Q) which seems to use a CNN to draw stockfish(!). This seems to support that it would work. I looked at the code and it seems very elegant, but they did not code the chess engine themselves. I think I will try a CNN as it seems very elegant but I do want to encorporate master games into the dataset so that my engine is more "human."

### Concept 2.1.1:
Instead of one-hot encoding features as one grid for each piece and colour, encode them as 0 - no piece, -1 black, 1 white. Do not do this for the pawns though as their attack is one-facing: instead, make sure that they are two different grids. This reduces the matrix down to 8*8*(6+ 1) = 448 instead of 8*8*12 = 768 (58% of original) and also logically makes sense as the severity of positions should be around the same.


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
dimensions: 64x2 16x2 8x4
```
again, very cool. However, in the opening it cannot precisely determine who is winning. I am starting to realise that in context, the absolute evaluations do not mean a lot. Actually, the relative evaluation between moves determine which move is best to be played (black is trying to minimize the evaluation) so the lowest number should be the best next move: this means the absolute evaluation accuracy is not as relevant. The engine struggles to identify moves which results in the immediate taking of the piece (it says a good move is black bishop infront of a white pawn) Additionally, proposed concept 2.0.1 and 2.2.

### Test 9
Major changes were made to the encoding of features
* allow white to move to be considered
* material counts be considered
* black materials are now encoded in the same grid as white, but with -1 instead of +1
* removed correct side analysis
* change dimensions

```
dataset: chessData-small
time to train: 11357s (3hrs, 9min)
epochs: 1000
final loss: 0.0208
final accuracy: 0.1175
test loss: 0.0265
test accuracy: 0.12
dimensions: 16x1 8x1 4x2
```
Loss seems too high, probably because of the lack of neurons. The training time seems significantly less, probably due to the lack of dimensions and inputs, despite almost doubling the training set size (200k -> 400k) because white to move is now accepted. More training data, lower batch sizes or larger dimensions may be a good idea. On some testing, it seems more accurate than previous models on positions. Positions were taken from games and pawns and structures were moved (but not taken away or added). The direction of increase/decrease in evaluation matched Stockfish. There is still doubt that previous models overfitted to training set due to the sheer size of training set, but this model does seem to perform well but may risk underfitting due to lack of hidden layers. A VERY good idea is to only change ONE variables at a time (ceteris paribus) and do not mess with so many variables since it is difficult to tell how the NN improved.

### Test 10
Same as Test 9 but with different dimensions
```
dataset: chessData-small
time to train:  21812s (6hrs, 3min)
epochs: 1000
final loss: 0.0092
final accuracy: 0.1214
test loss: 0.0293
test accuracy: 0.12
dimensions: 64x1 32x1 16x2 4x2
```

### Test 11
Major changes
* replace with Convolutional Neural Network!!
* white to move are not considered
* material is no longer added (reverse changes from test 9)
```
dataset: chessData-small
time to train: >6 hours, stopped before end
epochs: 152
final loss: 0.0028
final accuracy: 0.0203
dimensions:
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
conv2d (Conv2D)              (None, 8, 8, 32)          1760      
_________________________________________________________________
max_pooling2d (MaxPooling2D) (None, 4, 4, 32)          0         
_________________________________________________________________
conv2d_1 (Conv2D)            (None, 4, 4, 64)          18496     
_________________________________________________________________
max_pooling2d_1 (MaxPooling2 (None, 2, 2, 64)          0         
_________________________________________________________________
conv2d_2 (Conv2D)            (None, 2, 2, 64)          36928     
_________________________________________________________________
flatten (Flatten)            (None, 256)               0         
_________________________________________________________________
dense (Dense)                (None, 64)                16448     
_________________________________________________________________
dense_1 (Dense)              (None, 1)                 65        
=================================================================
```
Does not seem to go for centre control at all. It does not seem to mind losing material either. It does recognize more pattern based moves such as fianchetto'ing the bishop, which is nice. It seems like there are too many parameters and it is overfitting.