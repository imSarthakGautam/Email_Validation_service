| From / To | A  | B  | C  | D  | E  | F  |
|-----------|----|----|----|----|----|----|
| A         | 0  | 10 | 15 | 20 | 25 | 30 |
| B         | 10 | 0  | 35 | 25 | 17 | 28 |
| C         | 15 | 35 | 0  | 30 | 28 | 40 |
| D         | 20 | 25 | 30 | 0  | 22 | 16 |
| E         | 25 | 17 | 28 | 22 | 0  | 35 |
| F         | 30 | 28 | 40 | 16 | 35 | 0  |

Here starting with A and ending with A :  
there are 5!/2 = 60 routes to check

Using Greedy Approach/ Nearest Neighbour Approach:

A → B (10)  
B → E (17)  
E → D (22)  
D → F (16)  
F → C (40)  
C → A (15)  
- Total: 120