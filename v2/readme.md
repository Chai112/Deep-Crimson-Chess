# installation
For Ubuntu systems
```
sudo apt install python3
sudo apt install python3-pip
pip install tensorflow
pip install tf-nightly
```

Some tips for the next time building NNs:
* make sure the output dimension is correct as the number of neurons of the last layer corresponds to that
* make sure that the output numbers are 0-1 if you are using that type of activation function. Loss values shouldn't look crazy!
* test regularly