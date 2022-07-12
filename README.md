# Deep Crimson
### A deep neural network chess analysis engine -- by Chaidhat Chaimongkol
Deep Crimson 1 started on 2020, 26 December\
Deep Crimson 2 started on 2022, 9 June

# Promises
- Program must evaluate moves by itself (no using Stockfish/other engines during runtime)
- Program must not use book moves
- No closely copying ideas/code from Stockfish or any other well-known engines

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

### Concept 2.2.1: Evaluate white/black to move
At the moment, the program only evaluates black to move. The program can double its training data by simply reversing the board and reversing the signs of the pieces: black becomes white and vice versa. This also would allow the engine to play as white as well

### Concept 2.2.2: Feed attributes into FC layer
Extra attributes such as the pieces remaining should be fed into the Fully Connected (FC) layer as a second input. See [this](https://pyimagesearch.com/2019/02/04/keras-multiple-inputs-and-mixed-data/) for reference.

### Concept 2.1.1: One-Hot Encoding Optimization
Instead of one-hot encoding features as one grid for each piece and colour, encode them as 0 - no piece, -1 black, 1 white. Do not do this for the pawns though as their attack is one-facing: instead, make sure that they are two different grids. This reduces the matrix down to 8*8*(6+ 1) = 448 instead of 8*8*12 = 768 (58% of original) and also logically makes sense as the severity of positions should be around the same. This requires an activation function which can do negative numbers (e.g. tanh)


## Concept 3: Evaluate Best Next Move
Using dataset 1, train it to compare two moves and then output how confident the AI is that it is a good move.

* have to reformat PGN to FEN in dataset 1
* have to create random wrong moves in dataset 1
* training does not have any inbetween moves (such as semi-good moves)

## Concept 4: Reinforcement Learning
Deep Q-Learning and stuff - looks hard!
See https://www.youtube.com/watch?v=gWNeMs1Fb8I&list=PLXO45tsB95cIplu-fLMpUEEZTwrDNh6Ba&index=4

# Development Logs
### Test 1: Commit 20
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

### Test 2

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

### Test 3
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
Params: 73,697
time per evaluation: 0.03 s/move (33 moves/s)
```
Does not seem to go for centre control at all. It does not seem to mind losing material either. It does recognize more pattern based moves such as fianchetto'ing the bishop, which is nice. It seems like there are too many parameters and it is overfitting. Time per evaluation is a bit high. It can only feasibly do around a depth 2 evaluation.

### Test 12
Major bug fix
* the representation was incorrect: everything was set to 0.5, but black pieces were -1 and white were +1. This fed into a ReLU NN, which cannot take in negative numbers. TanH is used instead now and is set to 0.
* renamed final loss to training loss and accuracy
Did not get a checkpoint
```
dataset: chessData-verysmall
time to train: ?
epochs: 100
training loss: 3.712e-04
training accuracy: 0.6321 (!)
test loss: 0.0016
test accuracy: 0.8300 (!)
dimensions:
model.add(layers.Conv2D(16, 3, activation='tanh', input_shape=(8, 8, 6),padding='same'))
model.add(layers.MaxPooling2D((2, 2), padding='same'))
model.add(layers.Conv2D(32, 3, activation='tanh', padding='same'))
model.add(layers.MaxPooling2D((2, 2), padding='same'))
model.add(layers.Conv2D(32, 3, activation='tanh', padding='same'))
model.add(layers.Flatten())
model.add(layers.Dense(16, activation='tanh'))
model.add(layers.Dense(4, activation='tanh'))
model.add(layers.Dense(1))

Params: 
time per evaluation: 0.03 s/move
```
Very high accuracy in the datasets, but could be due to the small dataset. The model goes for centre control at the start and is very good at detecting where to move which pieces. It does not go very much for material still, as a pawn will still take another centre pawn instead of a knight on the side. This is a far greater improvement than before. Time per evaluation is still a bit high.

### Test 14
Major changes
* added multiple inputs (board + attr (materials))
* batching predictions at depth 0
* min-maxing at depth 3
```
dataset: chessData-small
time to train: ?
epochs: 200 (seem to converge at 100)
training loss: 0.0071
training accuracy: 0.5900
test loss: 0.0174
test accuracy: 0.5900
time per evaluation: 0.0001 s/move (10,000 moves/s)
```

It works with fairly decent accuracy. At this moment in time, it is weaker than an average player (me) and takes longer to compute. However, it shows very significant improvements from previous methods.


**FIRST GAME(!): Chaidhat (human) - Deep Crimson (depth 3)**
```
1. e4 Nf6 2. d3 e6 3. Nc3 Bb4 4. Bd2 O-O 5. Nf3 Re8 6. Be2 g6 7. Bh6 Ng4 8. Bg5 f6 9. h3 fxg5 10. hxg4 Qf6 11. Qd2 Bxc3 12. bxc3 h6 13. Rxh6 Kg7 14. Qxg5 Qxg5 15. Nxg5 Kxh6 16. Nf7+ Kg7
```
With min-maxing depth 3, it can recognise and punish severe blunders from its opponents. It cannot recognise illegal moves (such as during check) nor castling (on move 4, the computer asked to move Rf8, so I castled it instead). This led to some pretty interesting gameplay. A blunder by me on move 14 led to it taking my rook and being up three points. However, it is easy to lead it in a lot of the positions as it cannot recongise strong positions with that much accuracy yet. The depth search is quite low and may be the cause of why it can't detect the weak positions. Sometimes it plays moves which weaken its defense: it may be a good idea to have it play against itself and self train (with the help of stockfish) to recognise these pitfalls easier. For example, on move 6. it moves g6, most likely in anticipation for a fianchetto, but there is no bishop present. I believe that with self play, it will make this mistake and get punished by itself.

**Game 2: Alex (human) - Deep Crimson (depth 3), 1-0**
```
1. b3 Nf6 2. f3 e6 3. h4 Ng8 4. d4 Nc6 5. e3 Nb4 6. h5 d6 7. Ba3 a5 8.
Nc3 Ra7 9. Bb5+ c6 10. Rh4 Qxh4+ 11. g3 Qxh5 12. Bxc6+ bxc6 13. Nce2 Qd5 14. Rb1
Nxa2 15. Bxd6 Qxd6 16. d5 Qxd5 17. Nd4 c5 18. Ra1 Rc7 19. Rxa2 cxd4
20. exd4 Bc5 21. dxc5 Qxc5 22. c4 Ra7 23. Ne2 Rd7 24. Nd4 Rxd4 25. Rxa5 Qxc4 26.
bxc4 Rxd1+ 27. Kxd1 Ne7 28. Ra8 Kd7 29. c5 Nd5 30. f4 Nxf4 31. gxf4 Bb7 32. Rxh8
Bg2 33. Rxh7 Bf1 34. Rxg7 Kc6 35. Rxf7 Kxc5 36. Rc7+ Kb5 37. Rc2 Ka5 38. Ke1 Bd3
39. Rd2 Bb5 40. Rd6 Ka4 41. Rxe6 Bf1 42. Kxf1 Kb5 43. f5
```
Game 2 showed the flaws of the neural network and some smaller details. For example, the data did not reset, resulting in subsequent calculations having to calculate the previous positions as well (fixed). In the beginning, it did not go for centre position and does a lot of repeat moves. It fails to develop its pieces. It does not seem to understand material: for example, 20. Bc5 sac'ing the bishop, 25. Qxc4 sac'ing the queen (!) instead of taking the opponent's queen, 32. sac'ing the rook for no reason and then failing to defend the pawns. It's endgame positional understanding is lacking as well as it does 36. Kb5, moving away from the centre pawns. It does not defend e6 pawn on 40. and then sac's a bishop for no reason. I'm guessing it is around 500 ELO.

The conclusion is that the problem may be due to the dataset size (chess-small) being too small. In depth 4, it is already searching 430k position (after the bugfix) which means that this is twice the size of the chess database already. The best idea maybe for it to play against itself during training and have Stockfish evaluate its position and then try fit to that data. I believe the architecture and dimensions of the NN should be sufficient.

### Test 15
Minor changes
* Changed dimensions
```
dataset: chessData-small
time to train: 7 hrs
epochs: 130
training loss: 0.0057
training accuracy: 0.5629
test loss: 0.0189
test accuracy: 0.6000
time per evaluation: 0.0004 s/move (2,500 moves/s)
```

**Game 1: Chaidhat (human) - Deep Crimson (depth 3)
```
1. e4 Nf6 2. Nc3 c6 3. d4 Qa5 4. Bd3 d6 5. Nf3 Bg4 6. O-O Bxf3 7. Qxf3 Qb4 8. e5 Qxd4 9. exf6 Qxf6 10. Qxf6 exf6 11. Re1+ 
```
Deep Crimson suggests a7->a6, an illegal move.

Not bad, although due to the illegal move situation, it might be a good idea to fix that.