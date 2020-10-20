# GameOfLife
I wrote this simulation upon hearing news of professor Conway's passing (RIP prof. Conway!). Currently I randomly initialize the game that allows me to observe interesting patterns that may not have been observed (but also missing lots of other well known patterns). I am hoping to expand it to form more of his well known patterns.

To Run:
python game_of_life.py

The rules of the game are as described by Prof Conway
1) Any live cell with fewer than two live neighbours dies, as if by underpopulation.
2) Any live cell with two or three live neighbours lives on to the next generation.
3) Any live cell with more than three live neighbours dies, as if by overpopulation.
4) Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
