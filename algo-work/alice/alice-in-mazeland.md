# Problem Description

The Red Queen has put Alice in a dungeon, in a room with a large maze drawn on the floor. In her shrill voice, the Queen tells Alice:

"If you can solve my maze, you can go free; if you can't, then it's off with your head! Since it's my maze, you have to follow my rules. You start on the square at the upper left and you have to get to the square at the lower right. The arrows show the directions you are allowed to take when you leave a square. Now here's the tricky part: When you leave a square you must travel for exactly one stride. You're only a little girl; so at the start of the maze, a stride will only take you to the next square."

Alice looked at the laze and saw that each square with a red arrow had a piece of cake with EAT ME written on top, and each square with a green arrow had a small bottle labeled DRINK ME. She remembered from her previous adventures that eating the cake would make her grow, and drinking from the bottle would make her shrink.

"Each time you land on a square with a red arrow, you must eat a piece of the cake, which will make you grow and increase the length of your stride by one. Each time you land on a square with a green arrow, you must take a sip from the bottle, which will cause you shrink and decrease the length of your stride by one. If you shrink too much, then you won't be able to move at all!"

Can you find a path that Alice can take from the starting square to the goal

# Project Description and Deliverables

Something to consider is that due to maze land magic, cakes and drinks regenerate so any cell with a cake or a bottle will always have a cake or a bottle.

Your assignment is to (1) model the logic maze problem as an explicit weighted graph (2) use an appropriate weighted graph function call (provided in NetworkX) on this graph to solve the problem (3) submit your program to Gradescope for verification and (4) take part in an interview about the project.


1 Deliverables
The deliverables are (1) submission of your program to Gradescope, where it will be verified through several test cases and (2) grading interview with a TA that will take place during Week 6 and 7.

1.1 Grading Interview [45 points]

You will meet individually with a TA for approximately 30 minutes to discuss your solution. To facilitate this discussion, you will answer a series of questions about how you model the problem and your implementation. We have included some possible questions for the grading interview below. This list is not all inclusive and you will likely be asked questions that are not included in this list. We will post more information about how to sign up for an interview and some additional questions you may be asked during Week 4.

1. Explain how you modeled the logic maze as an explicit graph.
Vertices: Describe what each vertex in your graph represents in relation to the logic maze.
Edges: Explain the edges of your graph. Are they directed or undirected? What does an edge in your graph model represent in the context of the logic maze?
Weights: What does the weight on an edge represent?
Discuss any additional properties of the graph that are crucial for the unmodified Dijkstra’s to work correctly. This might include how you handled the start/end vertices (an ideal model would have one start vertex and one end vertex) or any other pertinent special features.

2. Argue for your model’s correctness. Given any maze instance, convince us that your model represents it correctly, and when combined with Dijkstra’s Algorithm, is guaranteed to find the shortest path if a path exists. This should be a concise yet complete argument (you will have to convince the TA)

3. Analyze the space requirements of your graph (i.e., how many vertices and edges does it have) by computing these from the logic maze’s attributes. Assume that the logic maze consists of an n x m maze. If precise formulas are not possible, provide upper bounds.

Please bring your implementation to the grading interview. It should solve the problem using the model and algorithm that you have mentioned in the previous section; and should be similar to your last submission on Gradescope. If these three do not match, we may deduct verification points.

As mentioned in class, you must modify the graph and not Dijkstra’s Algorithm. Modifying Dijkstra is against instructions will result in a minimum deduction of 25 points from your overall score on this project. Using a graph traversal algorithm to create the graph model falls into the same category as modifying the algorithm. The model should not be created via a traversal, or the 25-point deduction will apply. The entire graph must be created explicitly (rather than
implicitly) before the execution of Dijkstra. We realize this may not be the most efficient solution method (discuss in your complexity analysis if desired).

1.2 Results [55 pts]
There will be two assignments on Gradescope for verification.
• The Maze Verification Testing assignment is not worth any points on Canvas, but allows
infinite submissions. Submit to this assignment first to make sure that you fix any submission-
related bugs or typos (a separate document that details how to submit to Gradescope will be
released when the autograder assignments are released). It also has some smaller test cases
with timing results that you can use to get an idea of your program’s run time on Gradescope
compared to your computer. While this may have some edge cases, it will certainly not have
all edge cases, nor will the inputs be of maximum size (hint: test your code with some edge
cases even if you pass all these tests).
• The second assignment, Maze Verification, is worth 55 points. Expect extensive testing -
edge cases, large maze sizes (up to 100 rows by 100 columns), etc. We are providing strong
incentives for you to minimize your number of attempts.
– Passing 100% of test cases on the first submission will be awarded with 5 extra credit
points for a 60/55.
– Passing 100% of test cases on the second submission will be awarded with 2.5 extra
credit points for a 57.5/55. To be clear, this extra credit is only awarded if all tests are
passed; failing (or exceeding the time limit) on even only one test = no extra credit.
– The third submission does not have any associated extra credit.
– Beyond the third submission, a 10% deduction will be applied for each additional sub-
mission attempt.
– We will not be increasing the number of penalty-free submissions to more
than three.

2 Input
The first line of the input file will have three sections separated by a pair of colons back to back.
Every piece of information will be space-separated. The first section contains two space-separated
integers. The integers are the number of rows 2 ≤ R ≤ 100 and the number of columns 1 ≤ C ≤ 100
for the size of the matrix, respectively. The matrix will represent the maze that Alice must navigate
to complete the problem. The second and third sections contain two space-separated integers each
that represent the cell of the maze that Alice will start in and the “GOAL” respectively. You can
assume that Alice will start with a step size of 1.
Each subsequent line describes the information about a particular cell. Each of these lines will
contain three sections of information separated by a pair of colons back to back. Every piece of
information will be space-separated. The first section contains the space-separated row and column
number of that cell, respectively. The second section contains the allowed directions for movement
out of that cell given by any number of these space-separated cardinal direction indicators N, E,
S, W, NE, SE, SW, NW, and X (the direction indicators can appear in any order). Where X
indicates no movements out of that cell are allowed and it will only appear by itself. The third and
final section will indicate the effect the cell has on Alice’s step size and can be one of increase (I),
decrease (D), or no effect (N). Additionally, each of these lines can appear in any order.
The entire input file for Abbot’s maze is included at the end in the appendix.
3 Weights
Although, in Abbott’s maze, Alice is able to navigate the maze from start to end any way she wants
as long as she makes it to the end (if possible), she could expend more energy than necessary to get
there. Alice is very tired from having to deal with the Red Queen’s antics, so we want to help her
try to make it to the end with the least amount of energy used possible with the help of Dijkstra’s
Algorithm (which had not been invented in Mazeland). We will thus consider the step size that
Alice makes from cell to cell to be the weight of the edges.
4 Output Format
The first line of the output must contain the length of the shortest path found by your algorithm,
followed by the number of cells Alice visits on this shortest path. The second line gives the
coordinates for the cell where Alice starts separated by a space. The third line gives the coordinates
of the next cell Alice visits on the shortest path. This continues line-by-line concluding with the
coordinates of the “GOAL” cell. For example, one possible partial output for a maze that starts
at cell (1, 1) and has a “GOAL” of cell (8, 8) is
128 53
1 1
2 1
...
8 8
If there is no path for Alice to escape, then output “NO PATH”
8 8 :: 1 1 :: 8 8
1 1 :: E S :: N
1 2 :: E :: N
1 3 :: S :: I
1 4 :: E W :: N
1 5 :: SE SW :: N
1 6 :: SE :: D
1 7 :: E S W :: N
1 8 :: S :: I
2 1 :: SE :: I
2 2 :: E :: N
2 3 :: E W :: N
2 4 :: N S :: N
2 5 :: E :: N
2 6 :: N S :: N
2 7 :: N S :: N
2 8 :: SW :: N
3 1 :: NE SE :: N
3 2 :: N :: N
3 3 :: E S :: N
3 4 :: E :: N
3 5 :: E W :: N
3 6 :: SE NW :: N
3 7 :: NE SW :: N
3 8 :: SW :: N
4 1 :: NE SE :: N
4 2 :: SE :: D
4 3 :: E :: N
4 4 :: E W :: N
4 5 :: N S :: N
4 6 :: N S :: N
4 7 :: SE NW :: D
4 8 :: S :: N
5 1 :: N :: N
5 2 :: N :: N
5 3 :: NE SW :: N
5 4 :: NE SW :: N
5 5 :: SE SW NW :: N
5 6 :: NE SW :: N
5 7 :: S :: N
5 8 :: S :: N
6 1 :: N S :: N
6 2 :: NE SW :: N
6 3 :: NE SW NW :: N
6 4 :: S :: N
6 5 :: E W :: N
6 6 :: S :: N
6 7 :: N S :: N
6 8 :: SW NW :: N
7 1 :: N :: D
7 2 :: N E :: N
7 3 :: N E S :: N
7 4 :: E W :: N
7 5 :: N S :: N
7 6 :: W :: N
7 7 :: SW :: N
7 8 :: NW :: I
8 1 :: N E :: N
8 2 :: N :: I
8 3 :: N W :: N
8 4 :: W :: N
8 5 :: NE :: N
8 6 :: E :: N
8 7 :: W :: I
8 8 :: X :: N

Language Agnostic Autograder Submission
The verification assignment(s) are on Gradescope. Details are provided in the project instructions. Don’t
worry about submitting to Gradescope until you are certain your implementation is correct. The
instructions below are specifically about submitting your completed code to Gradescope.
When you submit to Gradescope, several test causes will be automatically run on your code, and you
will receive a score for the verification depending on the number of tests passed. Please note that you
have limited submission attempts and should only submit to Gradescope after performing extensive
testing to ensure your program is correct.
This Gradescope autograder is designed to be able to accept any language. However, if you choose a
language outside of Python 3, C/C++, or Java, please email or speak with TA John Henke.
(jhenke@mines.edu)
Only the standard library of your chosen language is available by default for each project except for
Project 4 Maze, where networkx in Python 3 will be preinstalled. Note the Python version that
Gradescope currently supports is Python 3.6 (features in python versions beyond 3.6 will not work
properly). If you would like to use other libraries outside of the standard library, then you must use the
Build.sh or Makefile submission type to install your dependencies (see below).
All submissions should be tested on Isengard/Alamode before submitting to Gradescope to ensure
they run properly on a Linux system. If a submission to Gradescope is improperly formatted or errors,
it will use up one of your submission attempts (if the infinite submission assignment exists, use it for
this purpose).
Input file contents will be provided over stdin, and a path to the input file will be provided as a
command line argument. The contents of this file are specified in the project instructions. It is your
choice how you would like to accept the input. All output requested in the project instructions must be
provided to stdout. Make sure to comment out any print statements except the ones providing the
requested output, or all tests will fail. The output must be provided exactly as specified in the project
instructions (decimal places, rounding, number of output lines, etc.) or it will be marked incorrect.
Your submission must contain exactly one of the following files (case-sensitive) in the top-level directory
that will be used for compilation. Note that all files to be compiled and run must also be in the top-level
directory.
• language.txt - this is the simplest/easiest method of submission.
• Build.sh
• Makefile
language.txt can only be used for submissions in Python 3, C/C++, and Java. language.txt must have
exactly two lines. The first line is the language: one of “python”, “c”, “c++”, or “java” without the
quotes.
The second line of language.txt must contain one of the following depending on the language selected:
Python - The name of the python file to execute (case sensitive, including the extension .py).
C/C++ - The name of the file containing main(). Only one provided file may contain a main() method.
Java - The name of the class containing main() (case sensitive, without .java).
Submit language.txt and your source code files (.cpp, .java, .py) to Gradescope under the correct
assignment.
How the autograder compiles and runs your code (for testing purposes)
Note these commands do not include passing the input file contents over stdin, but rather only the path
to the input file as a command line argument (arg1).
Python - The autograder runs the command “python3 file.py arg1” to execute your submission, where
file.py is the file name provided on the second line of language.txt.
C/C++ - The autograder compiles by determining all files with the extensions “.c” and “.cpp”, compiles
using “g++ file1.cpp file2.cpp ... -o PROJECT” and then runs “./PROJECT arg1”
Java - The autograder identifies all classes by identifying files that end in .java, compiles by running
“javac class1 class2 ....” and then runs “java main_class arg1” where main_class is the class name
provided on the second line of language.txt.
All submissions should be tested on Isengard/Alamode using the instructions given in the
previous paragraph for compilation and execution before submitting to Gradescope to ensure
they run properly. If a submission to Gradescope is improperly formatted or errors, it will use
up one of your submission attempts (and it’s on you).
Build.sh/Makefile Option
These options should only be used for languages outside of Python, C/C++, and Java.
Your submission must contain in the top-level directory either Build.sh or a Makefile (but not both). The
file provided must correctly compile your code on a Linux system. If Build.sh is present, then the bash
script will be invoked (i.e., “bash Build.sh” in the terminal). If a Makefile is present, then the command
“make” will be executed.
In either case, after compilation, there must be an executable script, in any language (with an
appropriate shebang #! line) named “PROJECT” (case sensitive, no extension). PROJECT will be invoked
with the proper command line arguments (./PROJECT arg1 arg2 ...), must execute without errors, and
provide the correct output to stdout.
The Build.sh/Makefile can be used to install the language that you are using in the docker container.
PROJECT does not have to be a compiled executable of your code; PROJECT can instead be a bash script
that executes your code however you would like and passes along the command line arguments it
receives to your code (nodejs my_javascript_program $1 $2). This helps avoid trying to compile certain
languages to executables (e.g. JavaScript) that are not meant to be compiled languages.

You have to write this in Python.
