A simple version of Conway's Game of Life with GUI using python.

"A cell is born if it has exactly three neighbours, survives if it has two or three living neighbours, and dies otherwise."

It was completed before I started using git. 

It's not very performant, but it works for reasonably small boards, say 32x32. There are quite a few optimizations that could be done, such as not using strings to store "alive" or "dead" state, for instance. 

Just running the python file shows a GUI where the user can enter a size. Then by clicking the squares, they turn red - these are alive cells. 
Also included are some common patterns, such as pulsars and such. 
