Solver for the puzzle game Lunar Shift <br>
App Store: https://apps.apple.com/us/app/lunar-shift/id6736531952 <br>
Google Play: https://play.google.com/store/apps/details?id=com.jakobkempe.lunarshift&hl=en-US <br>

Installation:
```
pip install -r requirements.txt
```

How to run:
```python app.py```

Flask version:
![img.png](img.png)
![solution.png](solution.png)
Console version:

```python main.py```

Sample Output:
```
=== Grid Solver Console Program ===

Enter grid rows (numbers separated by spaces).
Press Enter on an empty line to finish.

0 1 1 1
1 0 1 0
1 0 0 0
1 1 0 0

Enter the starting position (row and column separated by a space) [default: 0 0]:

Enter the number of moves allowed [default: 15]:
14
Enter the target value (0 or 1) for the grid to be solved [default: 0]:


Searching for a solution...

Solution found!
Sequence of moves: ['down', 'down', 'down', 'right', 'up', 'up', 'down', 'up', 'up', 'right', 'down', 'up', 'right', 'left']

Simulating moves:

Initial board state:
0 1 1 1
1 0 1 0
1 0 0 0
1 1 0 0

After move 1 ('down'):
0 1 1 1
0 0 1 0
1 0 0 0
1 1 0 0

After move 2 ('down'):
0 1 1 1
0 0 1 0
0 0 0 0
1 1 0 0

After move 3 ('down'):
0 1 1 1
0 0 1 0
0 0 0 0
0 1 0 0

After move 4 ('right'):
0 1 1 1
0 0 1 0
0 0 0 0
0 0 0 0

After move 5 ('up'):
0 1 1 1
0 0 1 0
0 1 0 0
0 0 0 0

After move 6 ('up'):
0 1 1 1
0 1 1 0
0 1 0 0
0 0 0 0

After move 7 ('down'):
0 1 1 1
0 1 1 0
0 0 0 0
0 0 0 0

After move 8 ('up'):
0 1 1 1
0 0 1 0
0 0 0 0
0 0 0 0

After move 9 ('up'):
0 0 1 1
0 0 1 0
0 0 0 0
0 0 0 0

After move 10 ('right'):
0 0 0 1
0 0 1 0
0 0 0 0
0 0 0 0

After move 11 ('down'):
0 0 0 1
0 0 0 0
0 0 0 0
0 0 0 0

After move 12 ('up'):
0 0 1 1
0 0 0 0
0 0 0 0
0 0 0 0

After move 13 ('right'):
0 0 1 0
0 0 0 0
0 0 0 0
0 0 0 0

After move 14 ('left'):
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
```
