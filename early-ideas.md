# Early Ideas

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

# Commit Logs
### Commit 20: 
using concept 2, training for 50 epochs using a rather larger NN, it can start to tell the difference between who is winning. If a white pawn is very far up the rank, it gives a favourable chance to white of winning (around 0.74, equivalent to 48 pawns up). However sometimes it does not give equal piece advantages. For example, if black a lot of pawns and knights whereas white does not, it only gives a advantage to black (like around 0.43 (-14 pawns)). Obviously, it is exagerrating the numbers of pawns, but it may be the result of stockfish giving very exagerrated evaluations during endgames (bad data) and also when it is "mate in", it awards 1.0 (100 pawns up). It may be a better idea to use sigmoid instead