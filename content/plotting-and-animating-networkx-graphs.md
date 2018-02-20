---
layout: post
title: Plotting and Animating NetworkX graphs
date: 2013-10-11 23:04
comments: true
categories: NetworkX, Matplotlib, Animation, Plotting
---
### Modifying neworkX graph using Matplotlib
Let's start with plotting a simple graph using `nx.draw`:
```python
import networkx as nx

G = nx.Graph()
G.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9])
G.add_edges_from([(1,2), (3,4), (2,5), (4,5), (6,7), (8,9), (4,7), (1,7), (3,5), (2,7), (5,8), (2,9), (5,7)])

nx.draw(G)
```
In my case I get something like this:

{% img http://s19.postimg.org/5zl0vjk0j/figure_1.png %}

You might get something different because networkX internally uses 
`matplotlib.scatter` which randomly generates the position of the nodes.

Now let's dive deeper into how does networkX internally draws graphs. 
Taking a quick look of all the children of the plot.
```python
fig = plt.gcf()

axes = plt.gca()

axes.get_children()
Out[14]:
[<matplotlib.axis.XAxis at 0x1bed4d0>,
 <matplotlib.axis.YAxis at 0x30457d0>,
 <matplotlib.text.Text at 0x30613d0>,
 <matplotlib.text.Text at 0x3061310>,
 <matplotlib.text.Text at 0x3061550>,
 <matplotlib.text.Text at 0x30615d0>,
 <matplotlib.text.Text at 0x3061650>,
 <matplotlib.text.Text at 0x30616d0>,
 <matplotlib.text.Text at 0x3061750>,
 <matplotlib.text.Text at 0x30617d0>,
 <matplotlib.text.Text at 0x3061890>,
 <matplotlib.collections.PathCollection at 0x305d4d0>,
 <matplotlib.collections.LineCollection at 0x305dc50>,
 <matplotlib.text.Text at 0x30514d0>,
 <matplotlib.patches.Rectangle at 0x3051550>,
 <matplotlib.spines.Spine at 0x303ec90>,
 <matplotlib.spines.Spine at 0x303e990>,
 <matplotlib.spines.Spine at 0x303eb10>,
 <matplotlib.spines.Spine at 0x303e7d0>]
```
Here we see there are 9 `matplotlib.text.Text` objects which are the labels
on the nodes. Let's see some of the properties of one of the text objects.
```python
text_object = axes.get_children()[2]

text_object.get_text()
Out[13]: '1'

text_object.get_size()
Out[14]: 12.0

text_object.get_color()
Out[15]: 'k'

```
For the complete list of properties we can call the `properties` method. 
Example: `text_object.properties()`.

Next object we see is the `matplotlib.collections.PathCollection` object which
is the collection object of all the nodes. Now again we can see some properties
and modify them.
```python
nodes = axes.get_children()[11]                 # Selecting the PathCollection object
In [25]: nodes.get_pickradius()
Out[25]: 5.0

In [26]: nodes.get_label()
Out[26]: '_collection0'

In [27]: nodes.get_facecolor()
Out[27]: array([[ 1.,  0.,  0.,  1.]])

In [28]: nodes.get_edgecolors()
Out[28]: array([[ 0.,  0.,  0.,  1.]])

In [29]: nodes.get_linewidth()
Out[29]: (1.0,)
```
We can change the properties:
```python
nodes.set_linewidth(2)
nodes.set_pickradius(8)
plt.draw()
```
Now with the `offsets` property we can change the position of the nodes.
```python
In [32]: offsets = nodes.get_offsets()

In [33]: offsets
Out[33]: 
array([[ 1.        ,  0.31732594],
       [ 0.60075321,  0.28045667],
       [ 0.04382142,  0.98124087],
       [ 0.38063134,  0.99245427],
       [ 0.27586167,  0.61542286],
       [ 0.9961299 ,  0.91637658],
       [ 0.70916575,  0.66473314],
       [ 0.        ,  0.23580501],
       [ 0.28996686,  0.        ]])

In [35]: offsets[0][0] = 0.5

In [37]: offsets[0][1] = 0.5

In [38]: plt.draw()
```
Now we get this output:
{% img http://s19.postimg.org/s01dc62oj/figure_2.png %}
We see here that only the node has moved and the label and the edges are 
at their original position. We will now move the edges to the new node
position.  
NetworkX uses `matplotlib.scatter` to draw nodes which creates a
`collections.PathCollection` object and then draws the edges 
which is a `matplotlib.collections.LineCollection` object.

We can modify many properties of the lines. But for now let's just move the
two edges to the new position of their node.
```python
edges_object = axes.get_children()[12]              #selecting the LineCollection object
edges_object.get_paths()
Out[34]: 
[Path([[ 0.17693707  0.        ]
 [ 0.29792     0.44577014]], None),
 Path([[ 0.17693707  0.        ]
 [ 0.43349969  0.12392229]], None),
 Path([[ 0.29792     0.44577014]
 [ 0.30217028  0.87528811]], None),
 Path([[ 0.29792     0.44577014]
 [ 0.70125136  0.42163912]], None),
 Path([[ 0.29792     0.44577014]
 [ 0.43349969  0.12392229]], None),
 Path([[ 1.          0.3245961 ]
 [ 0.8526191   0.04511872]], None),
 Path([[ 1.          0.3245961 ]
 [ 0.70125136  0.42163912]], None),
 Path([[ 0.8526191   0.04511872]
 [ 0.70125136  0.42163912]], None),
 Path([[ 0.8526191   0.04511872]
 [ 0.43349969  0.12392229]], None),
 Path([[ 0.70125136  0.42163912]
 [ 0.65698815  0.85722426]], None),
 Path([[ 0.70125136  0.42163912]
 [ 0.43349969  0.12392229]], None),
 Path([[ 0.          0.24864231]
 [ 0.43349969  0.12392229]], None),
 Path([[ 0.65698815  0.85722426]
 [ 0.30217028  0.87528811]], None)]
```
We see the 13 edges. The initial position of the moved node was `[0.176...  0.     ]`
and we see here that the first and second paths have the starting point at
that position. So, we need to move the starting point of those two edges
to `[0.5     0.5     ]`.
```python
first_path = edges_object.get_paths()[0]
first_path.vertices
Out[41]: 
array([[ 0.17693707,  0.        ],
       [ 0.29792   ,  0.44577014]])
first_path.vertices[0][0] = 0.5
first_path.vertices[0][1] = 0.5
second_path = edges_object.get_paths()[1]
second_path.vertices
Out[48]: 
array([[ 0.17693707,  0.        ],
       [ 0.43349969,  0.12392229]])
second_path.vertices[0][0] = 0.5
second_path.vertices[0][1] = 0.5

plt.draw()
```
We can now see the graph to be something like:
{% img http://s19.postimg.org/3wfnkzqj7/figure_3.png %}

Now let's move the label to this position:
```python
label_object = axes.get_children()[2]

label_object.get_text()
Out[54]: '1'

label_object.get_position()
Out[55]: (0.17693707256025257, 0.0)

label_object.set_position((0.5, 0.5))

plt.draw()
```
We can now see the graph to be like:
{% img http://s19.postimg.org/se7r8vt3n/figure_4.png %}
So, finally we have moved the node to a new position. For having better 
control over the properties I have rewritten the `nx_pyplot` module which 
adds many functions to manipulate the graph. You can check out the 
[github repo](https://github.com/ankurankan).
### Basic Animation
Let's start with a very simple color changing animation in which we will draw 
a graph whose nodes will change color. Here in each iteration we are drawing 
a new graph over the previous ones with different node colors. This is a 
very bad approach but let's just start with this. I will write about better 
ways to do it in the next post.

I will be using `networkX` for drawing the graphs and `matplotlib` for 
animation.
```python
import networkx as nx
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import random

# Graph initialization
G = nx.Graph()
G.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9])
G.add_edges_from([(1,2), (3,4), (2,5), (4,5), (6,7), (8,9), (4,7), (1,7), (3,5), (2,7), (5,8), (2,9), (5,7)])

# Animation funciton
define animate(i):
    colors = ['r', 'b', 'g', 'y', 'w', 'm']
    nx.draw_circular(G, node_color=[random.choice(colors) for j in range(9)]

nx.draw_circular(G)
fig = plt.gcf()

# Animator call
anim = animation.FuncAnimation(fig, animate, frames=20, interval=20, blit=True)
```

Let's step through and see what's happening. In the first four lines we are 
importing `networkX`, `matplotlib.animation`, `matplotlib.pyplot` and `random` 
modules. 

In the next few lines we create a graph using networkX:
```python
G = nx.Graph()                                                             
G.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9])
G.add_edges_from([(1,2), (3,4), (2,5), (4,5), (6,7), (8,9), (4,7), (1,7), (3,5), (2,7), (5,8), (2,9), (5,7)])
```
First we initialize an empty graph `G`. Then we add 9 nodes and 13 edges to it.

This next piece is the animation function which takes a single parameter `i`
 which is the frame number of the animation.
```python
def animate(i): 
    colors = ['r', 'b', 'g', 'y', 'w', 'm']                                
    nx.draw_circular(G, node_color=[random.choice(colors) for j in range(9)]   
```
Here the `colors` list is a list of colors from which we will be randomly 
picking up colors for our nodes.
`nx.draw_circular` draws the graph keeping the nodes in a circular pattern.

```python
anim = animation.FuncAnimation(fig, animate, frames=20, interval=20, blit=True)
```
`animation.FuncAnimation` repeatedly calls the animate fucntion incrementing 
`i` in each iteration.
`frames` define the number of times animate function is called, 
`interval` is the inverval between each call.
`blit=True` defines to draw only those parts which have changed.

