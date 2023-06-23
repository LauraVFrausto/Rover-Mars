# -*- coding: utf-8 -*-
"""RutaMarte.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1csY0JBjVuq23y0qe9UKGzaAhSlmr0Yaj

# Planeación de rutas para la exploración en Marte

* Miguuel Emiliano Gozalez Gauna A01633816
* Francisco Javier Chávez Ochoa A01641644
* Laura Merarí Valdivia Frausto A01641790
"""

pip install simpleai

import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
import seaborn as sns
import simpleai.search as search
import math
import time

# Definir la clase MazeState
class Marte(search.SearchProblem):
    def __init__(self,start, goal, board):
        self.board = board
        self.start = start
        self.goal = goal
        super().__init__(initial_state=self.start)

    def actions(self, state):
        actions = []
        row, col = state

        if row > 0 and self.board[row][col] < self.board[row-1][col]+0.25 and self.board[row][col] > self.board[row-1][col]-0.25:
            actions.append((row-1, col))
        if col > 0 and self.board[row][col] < self.board[row][col-1]+0.25 and self.board[row][col] > self.board[row][col-1]-0.25:
            actions.append((row, col-1))
        if row < len(self.board)-1 and self.board[row][col] < self.board[row+1][col]+0.25 and self.board[row][col] > self.board[row+1][col]-0.25:
            actions.append((row+1, col))
        if col < len(self.board[row])-1 and self.board[row][col] < self.board[row][col+1]+0.25 and self.board[row][col] > self.board[row][col+1]-0.25:
            actions.append((row, col+1))
        if row > 0 and col > 0 and self.board[row][col] < self.board[row-1][col-1]+0.25 and self.board[row][col] > self.board[row-1][col-1]-0.25:
            actions.append((row-1, col-1))
        if row > 0 and col < len(self.board[row])-1 and self.board[row][col] < self.board[row-1][col+1]+0.25 and self.board[row][col] > self.board[row-1][col+1]-0.25:
            actions.append((row-1, col+1))
        if row < len(self.board)-1 and col > 0 and self.board[row][col] < self.board[row+1][col-1]+0.25 and self.board[row][col] > self.board[row+1][col-1]-0.25:
            actions.append((row+1, col-1))
        if row < len(self.board)-1 and col < len(self.board[row])-1 and self.board[row][col] < self.board[row+1][col+1]+0.25 and self.board[row][col] > self.board[row+1][col+1]-0.25:
            actions.append((row+1, col+1))
        return actions

    def result(self, state, action):
        return action

    def is_goal(self, state):
        return state == self.goal

    def heuristic(self, state):
        return math.sqrt((state[0] - self.goal[0])**2 + (state[1] - self.goal[1])**2)

    def path(self, node):
        actions = []
        total_distance = 0
        while node.parent_action is not None:
            actions.append(node.parent_action)
            total_distance += math.sqrt((node.state[0]-node.parent.state[0])**2 + (node.state[1]-node.parent.state[1])**2)
            node = node.parent
        actions.reverse()
        return actions, total_distance
    def cost(self, state, action, next_state):
        row, col = state
        next_row, next_col = next_state
        if abs(row - next_row) + abs(col - next_col) > 1:
            return math.sqrt(2)
        else:
            return 1

# importacion del mapa marciano, cuenta numero columnas y numero filas, escala

mars_map = np.load('mars_map.npy')
nr, nc = mars_map.shape
scale = 10.0174

"""# RUTAS"""

# Primera ruta
r = nr-round(6400/scale)
c =round(2850/scale)
start= (r,c)

r = nr-round(6800/scale)
c =round(3150/scale)
goal= (r,c)

# Rendimiento de los algoritmos de búsqueda para rutas cortas y largas

# coordenadas a 1000 metros
#r = nr-round(6900/scale)
#c =round(3350/scale)
#goal= (r,c)

# coordenadas a 5000 metros
#r = nr-round(7000/scale)
#c =round(5350/scale)
#goal= (r,c)

# coordenadas a 10,000 metros (El algoritmo no llega a su objetivo)
#r = nr-round(3500/scale)
#c =round(11000/scale)
#goal= (r,c)

# Primera ruta
r = nr-round(6400/scale)
c =round(2850/scale)
start= (r,c)

#r = nr-round(6800/scale)
#c =round(3150/scale)
#goal= (r,c)

# Rendimiento de los algoritmos de búsqueda para rutas cortas y largas

# coordenadas a 1000 metros
r = nr-round(6900/scale)
c =round(3350/scale)
goal= (r,c)

# coordenadas a 5000 metros
#r = nr-round(7000/scale)
#c =round(5350/scale)
#goal= (r,c)

# coordenadas a 10,000 metros (El algoritmo no llega a su objetivo)
#r = nr-round(3500/scale)
#c =round(11000/scale)
#goal= (r,c)

# Primera ruta
r = nr-round(6400/scale)
c =round(2850/scale)
start= (r,c)

#r = nr-round(6800/scale)
#c =round(3150/scale)
#goal= (r,c)

# Rendimiento de los algoritmos de búsqueda para rutas cortas y largas

# coordenadas a 1000 metros
#r = nr-round(6900/scale)
#c =round(3350/scale)
#goal= (r,c)

# coordenadas a 5000 metros
r = nr-round(7000/scale)
c =round(5350/scale)
goal= (r,c)

# coordenadas a 10,000 metros (El algoritmo no llega a su objetivo)
#r = nr-round(3500/scale)
#c =round(11000/scale)
#goal= (r,c)

"""## ALGORITMOS"""

times = []
total_distances = []
step_costs=[]

"""### A*"""

# Define the problem and run the search algorithm A*
problem = Marte(start,goal,mars_map)
start_time = time.time()
result = search.astar(problem, graph_search=True)
end_time = time.time()

actions = result.path()
total_distance = len(actions)*scale
step_cost = result.cost

times.append(end_time - start_time)
total_distances.append(total_distance)
step_costs.append(step_cost)

print("Total Distance:"+str(round(total_distance))+'m')
print("Time:", end_time - start_time)
print("Cost:"+str(round(step_cost,2)))

path1 =np.array([p[0] for p in result.path()])
path1[0]=start

# Convert the result path to a format that can be used with Scatter3d
path_x1 = np.array([p[1] for p in path1])*scale
path_y1 = (nr-np.array([p[0] for p in path1]))*scale
path_z1 = np.array([mars_map[p[0]][p[1]] for p in path1])

"""### Búsqueda de costo uniforme (UCS)"""

# Define the problem and run the search algorithm busqueda voraz
problem = Marte(start,goal,mars_map)
start_time = time.time()
result = search.greedy(problem, graph_search=True)
end_time = time.time()

actions = result.path()
total_distance = len(actions)*scale
step_cost = result.cost

times.append(end_time - start_time)
total_distances.append(total_distance)
step_costs.append(step_cost)

print("Total Distance:"+str(round(total_distance))+'m')
print("Time:", end_time - start_time)
print("Cost:"+str(round(step_cost,2)))

path3 =np.array([p[0] for p in result.path()])
path3[0]=start

# Convert the result path to a format that can be used with Scatter3d
path_x3 = np.array([p[1] for p in path3])*scale
path_y3 = (nr-np.array([p[0] for p in path3]))*scale
path_z3 = np.array([mars_map[p[0]][p[1]] for p in path3])

"""### Búsqueda en amplitud (BFS)"""

# Define the problem and run the search algorithm busqueda voraz
problem = Marte(start,goal,mars_map)
start_time = time.time()
result = search.breadth_first(problem, graph_search=True)
end_time = time.time()

actions = result.path()
total_distance = len(actions)*scale
step_cost = result.cost

times.append(end_time - start_time)
total_distances.append(total_distance)
step_costs.append(step_cost)

print("Total Distance:"+str(round(total_distance))+'m')
print("Time:", end_time - start_time)
print("Cost:"+str(round(step_cost,2)))

path4 =np.array([p[0] for p in result.path()])
path4[0]=start

# Convert the result path to a format that can be used with Scatter3d
path_x4 = np.array([p[1] for p in path4])*scale
path_y4 = (nr-np.array([p[0] for p in path4]))*scale
path_z4 = np.array([mars_map[p[0]][p[1]] for p in path4])

"""## ANALISIS de Tiempo, Distancia total y costo de mis algoritmos"""

resultados = pd.DataFrame({'Tiempo':times, 'Distancia_Total': total_distances, 'Costo': step_costs})
resultados.index=['A*','UCS', 'BFS']

# Plot of each column in DataFrame Resultadopos
import matplotlib.pyplot as plt
fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(12,4))

axs[0].bar(resultados.index, resultados['Tiempo'], color = 'red')
axs[0].set_title('Tiempo')

axs[1].bar(resultados.index, resultados['Distancia_Total'])
axs[1].set_title('Distancia_Total')

axs[2].bar(resultados.index, resultados['Costo'], color = 'green')
axs[2].set_title('Costo')

fig.tight_layout()

plt.show()

"""# PLOT del Crater"""

x = scale*np.arange(mars_map.shape[1])
y = scale*np.arange(mars_map.shape[0])
X, Y = np.meshgrid(x, y)

import matplotlib.pyplot as plt

# Create the figure and axis objects
fig, ax = plt.subplots()

# Create the heatmap using the imshow function
heatmap = ax.imshow(mars_map, cmap='coolwarm')

# Add a colorbar to the heatmap
cbar = ax.figure.colorbar(heatmap, ax=ax)

# Set the axis labels and title
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_title('Mars Map')

# Show the plot
plt.show()

fig = go.Figure(data=[
            go.Surface(
                x=X, y=Y, z=np.flipud(mars_map), colorscale='hot', cmin=0, 
                lighting=dict(ambient=0.0, diffuse=0.8, fresnel=0.02, roughness=0.4, specular=0.2),
                lightposition=dict(x=0, y=nr/2, z=2*mars_map.max())
            ),
            go.Scatter3d(
                x=path_x1, y=path_y1, z=path_z1, name='A*', mode='markers', 
                marker=dict(color=np.linspace(0, 1, len(path_x1)), colorscale="Viridis", size=4)
            ),
            
            go.Scatter3d(
                x=path_x3, y=path_y3, z=path_z3, name='UCS', mode='markers', 
                marker=dict(color=np.linspace(0, 1, len(path_x3)), colorscale="Blues", size=4)
            ),
            go.Scatter3d(
                x=path_x4, y=path_y4, z=path_z4, name='BFS', mode='markers', 
                marker=dict(color=np.linspace(0, 1, len(path_x4)), colorscale="Reds", size=4)
            )
        ], layout=go.Layout(
            scene_aspectmode='manual', 
            scene_aspectratio=dict(x=1, y=nr/nc, z=max(mars_map.max()/x.max(), 0.2)), 
            scene_zaxis_range=[0, mars_map.max()]
        ))

#fig.show()
pio.write_html(fig, file='mapa_marte.html', auto_open=True)

