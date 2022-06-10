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