# pyxos
Paxos Implementation in Python for Distributed Algorithms Class.
It does not run for 10000 messages, there were some wrong assumptions in the beginning
which I think made the code slow. However I implemented total order and catch up rigorously and there should be no tricks with timing the processes, which came at a computational cost. I also tried to avoid for loops but it was still slow. If anyone knows why, I would welcome any feedback. Also due to my implementation of total order, it fails on the lossy test as I need all the messages for the total order.

Test with 1-3 Acceptors all behave as one would expect on my macos
