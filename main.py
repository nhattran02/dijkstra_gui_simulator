import tkinter as tk
from tkinter import simpledialog, messagebox, ttk, filedialog
import math
import json
import heapq

INF = int(1e9)

class GraphDrawer:
    def __init__(self, root):    
        root.geometry("900x700+325+37")
        root.minsize(120, 1)
        root.maxsize(1540, 845)
        root.resizable(1,  1)
        root.title("Dijkstra")
        root.configure(background="#d9d9d9")
        root.configure(highlightbackground="#d9d9d9")
        root.configure(highlightcolor="black")

        self.root = root

        # Weight Matrix Frame
        self.weightMatrixFrame = tk.Frame(self.root)
        self.weightMatrixFrame.place(relx=0.011, rely=0.369, relheight=0.343, relwidth=0.314)
        self.weightMatrixFrame.configure(relief='groove')
        self.weightMatrixFrame.configure(borderwidth="2")
        self.weightMatrixFrame.configure(relief="groove")
        self.weightMatrixFrame.configure(background="#ffffff")
        self.weightMatrixFrame.configure(highlightbackground="#ffffff")
        self.weightMatrixFrame.configure(highlightcolor="black")

        self.h_scroll = tk.Scrollbar(self.weightMatrixFrame, orient=tk.HORIZONTAL)
        self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        self.v_scroll = tk.Scrollbar(self.weightMatrixFrame, orient=tk.VERTICAL)
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)    

        self.matrix_view = ttk.Treeview(
            self.weightMatrixFrame,
            show="headings",
            height=10,
            xscrollcommand=self.h_scroll.set,
            yscrollcommand=self.v_scroll.set
        )
        self.matrix_view.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Attach scrollbars to the Treeview
        self.h_scroll.config(command=self.matrix_view.xview)
        self.v_scroll.config(command=self.matrix_view.yview)            

        # Weight Matrix Label
        self.weightMatrixLabel = tk.Label(self.root)
        self.weightMatrixLabel.place(relx=0.022, rely=0.316, height=25, width=93)

        self.weightMatrixLabel.configure(activebackground="#d9d9d9")
        self.weightMatrixLabel.configure(activeforeground="black")
        self.weightMatrixLabel.configure(anchor='w')
        self.weightMatrixLabel.configure(background="#d9d9d9")
        self.weightMatrixLabel.configure(compound='left')
        self.weightMatrixLabel.configure(disabledforeground="#a3a3a3")
        self.weightMatrixLabel.configure(font="-family {Segoe UI} -size 9")
        self.weightMatrixLabel.configure(foreground="black")
        self.weightMatrixLabel.configure(highlightbackground="#d9d9d9")
        self.weightMatrixLabel.configure(highlightcolor="black")
        self.weightMatrixLabel.configure(text='''Weight Matrix''')

        # Log 
        self.Log = tk.Text(self.root)
        self.Log.place(relx=0.011, rely=0.729, relheight=0.25, relwidth=1)
        self.Log.configure(background="white")
        self.Log.configure(font="TkTextFont")
        self.Log.configure(foreground="black")
        self.Log.configure(highlightbackground="#d9d9d9")
        self.Log.configure(highlightcolor="black")
        self.Log.configure(insertbackground="black")
        self.Log.configure(selectbackground="#d9d9d9")
        self.Log.configure(selectforeground="black")
        self.Log.configure(wrap="word")

        # Open Graph Button
        self.openGraphBtn = tk.Button(self.root)
        self.openGraphBtn.place(relx=0.022, rely=0.029, height=26, width=120)
        self.openGraphBtn.configure(activebackground="#d9d9d9")
        self.openGraphBtn.configure(activeforeground="black")
        self.openGraphBtn.configure(background="#d9d9d9")
        self.openGraphBtn.configure(disabledforeground="#a3a3a3")
        self.openGraphBtn.configure(font="-family {Segoe UI} -size 9")
        self.openGraphBtn.configure(foreground="black")
        self.openGraphBtn.configure(highlightbackground="#d9d9d9")
        self.openGraphBtn.configure(highlightcolor="black")
        self.openGraphBtn.configure(text='''Open Graph''')    
        self.openGraphBtn.configure(command=self.open_graph)


        # Save Graph Button
        self.savegraphBtn = tk.Button(self.root)
        self.savegraphBtn.place(relx=0.022, rely=0.086, height=26, width=120)
        self.savegraphBtn.configure(activebackground="#d9d9d9")
        self.savegraphBtn.configure(activeforeground="black")
        self.savegraphBtn.configure(background="#d9d9d9")
        self.savegraphBtn.configure(disabledforeground="#a3a3a3")
        self.savegraphBtn.configure(font="-family {Segoe UI} -size 9")
        self.savegraphBtn.configure(foreground="black")
        self.savegraphBtn.configure(highlightbackground="#d9d9d9")
        self.savegraphBtn.configure(highlightcolor="black")
        self.savegraphBtn.configure(text='''Save Graph''')
        self.savegraphBtn.configure(command=self.save_graph)

        # New Graph Button
        self.newGraphBtn = tk.Button(self.root)
        self.newGraphBtn.place(relx=0.178, rely=0.029, height=26, width=120)
        self.newGraphBtn.configure(activebackground="#d9d9d9")
        self.newGraphBtn.configure(activeforeground="black")
        self.newGraphBtn.configure(background="#d9d9d9")
        self.newGraphBtn.configure(disabledforeground="#a3a3a3")
        self.newGraphBtn.configure(font="-family {Segoe UI} -size 9")
        self.newGraphBtn.configure(foreground="black")
        self.newGraphBtn.configure(highlightbackground="#d9d9d9")
        self.newGraphBtn.configure(highlightcolor="black")
        self.newGraphBtn.configure(text='''New Graph''')    
        self.newGraphBtn.configure(command=self.new_graph)


        # Update Button
        self.updateBtn = tk.Button(self.root)
        self.updateBtn.place(relx=0.178, rely=0.086, height=26, width=120)
        self.updateBtn.configure(activebackground="#d9d9d9")
        self.updateBtn.configure(activeforeground="black")
        self.updateBtn.configure(background="#d9d9d9")
        self.updateBtn.configure(disabledforeground="#a3a3a3")
        self.updateBtn.configure(font="-family {Segoe UI} -size 9")
        self.updateBtn.configure(foreground="black")
        self.updateBtn.configure(highlightbackground="#d9d9d9")
        self.updateBtn.configure(highlightcolor="black")
        self.updateBtn.configure(text='''Update Matrix''')        
        self.updateBtn.configure(command=self.update_matrix)

        # Canvas Draw
        self.CanvasDraw = tk.Canvas(self.root)
        self.CanvasDraw.place(relx=0.333, rely=0.017, relheight=0.7, relwidth=0.656)
        self.CanvasDraw.configure(background="#ffffff")
        self.CanvasDraw.configure(borderwidth="2")
        self.CanvasDraw.configure(highlightbackground="#d9d9d9")
        self.CanvasDraw.configure(highlightcolor="black")
        self.CanvasDraw.configure(insertbackground="black")
        self.CanvasDraw.configure(relief="ridge")
        self.CanvasDraw.configure(selectbackground="#d9d9d9")
        self.CanvasDraw.configure(selectforeground="black")        

        # Run Step Button
        self.runStepBtn = tk.Button(self.root)
        self.runStepBtn.place(relx=0.178, rely=0.243, height=26, width=120)
        self.runStepBtn.configure(activebackground="#d9d9d9")
        self.runStepBtn.configure(activeforeground="black")
        self.runStepBtn.configure(background="#d9d9d9")
        self.runStepBtn.configure(disabledforeground="#a3a3a3")
        self.runStepBtn.configure(font="-family {Segoe UI} -size 9")
        self.runStepBtn.configure(foreground="black")
        self.runStepBtn.configure(highlightbackground="#d9d9d9")
        self.runStepBtn.configure(highlightcolor="black")
        self.runStepBtn.configure(text='''Run Step''')
        self.runStepBtn.configure(command=self.run_step)

        # Run All Button
        self.runAllBtn = tk.Button(self.root)
        self.runAllBtn.place(relx=0.022, rely=0.243, height=26, width=120)
        self.runAllBtn.configure(activebackground="#d9d9d9")
        self.runAllBtn.configure(activeforeground="black")
        self.runAllBtn.configure(background="#d9d9d9")
        self.runAllBtn.configure(disabledforeground="#a3a3a3")
        self.runAllBtn.configure(font="-family {Segoe UI} -size 9")
        self.runAllBtn.configure(foreground="black")
        self.runAllBtn.configure(highlightbackground="#d9d9d9")
        self.runAllBtn.configure(highlightcolor="black")
        self.runAllBtn.configure(text='''Run All''')
        self.runAllBtn.configure(command=self.run_all)


        # -----------------------------------------    
        # Graph Data
        self.nodes = {}  # node_id: (x, y)
        self.edges = []  # (node1_id, node2_id, weight)
        self.node_count = 0
        self.start_node = None
        self.end_node = None
        self.dijkstra_queue = None
        self.visited_nodes = set()
        self.node_distances = {}
        self.previous_nodes = {}


        # Interaction State
        self.current_action = None
        self.selected_nodes = []
        self.moving_node = None

        # Right Click Menu
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Add Node", command=self.enable_add_node)
        self.context_menu.add_command(label="Add Line", command=self.enable_add_line)
        self.context_menu.add_command(label="Move", command=self.enable_move)  
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Set Start Node", command=self.enable_set_start_node)
        self.context_menu.add_command(label="Set End Node", command=self.enable_set_end_node)        

        # Bindings
        self.CanvasDraw.bind("<Button-1>", self.on_click)
        self.CanvasDraw.bind("<B1-Motion>", self.on_drag)
        self.CanvasDraw.bind("<ButtonRelease-1>", self.on_release)
        self.CanvasDraw.bind("<Button-3>", self.show_context_menu)
        
    def highlight_path(self, path):
        self.CanvasDraw.delete("all")
        self.redraw_graph()          
        for i in range(len(path)):
            self.draw_node(path[i], *self.nodes[path[i]], text_color="white", bg_color="green")
            if i > 0:
                self._draw_edge(path[i - 1], path[i], 0, bg_color="green")

    def dijkstra_find_path(self, n, adj, s, e):
        dist = [INF] * (n + 1)
        visited = [False] * (n + 1)
        parent = [-1] * (n + 1)  # To track the path
        dist[s] = 0

        for _ in range(n):
            # Find the vertex with the smallest distance that has not been visited
            u = -1
            for i in range(1, n + 1):
                if not visited[i] and (u == -1 or dist[i] < dist[u]):
                    u = i

            if dist[u] == INF:
                break

            visited[u] = True

            for v, w in adj[u]:
                if dist[v] > dist[u] + w:
                    dist[v] = dist[u] + w
                    parent[v] = u
        path = []
        if dist[e] != INF:  # If there's a valid path to e
            current = e
            while current != -1:
                path.append(current)
                current = parent[current]
            path.reverse()

        return dist[e], path

    def convert_edges_to_adj(self, edges, n):
        # Initialize adjacency list for a graph with n nodes
        adj = [[] for _ in range(n + 1)]
        for edge in edges:
            u, v, w = edge
            adj[u].append((v, w))
            adj[v].append((u, w))  # Comment this line if the graph is directed
        return adj

    def run_step(self):
        if not hasattr(self, 'step_state'):  # Initialize step state if not present
            # Initialize the step-by-step state
            self.num_nodes = len(self.nodes)
            if self.num_nodes == 0:
                messagebox.showinfo("Run Step", "No nodes to run.")
                return        
            if self.start_node is None or self.end_node is None:
                messagebox.showinfo("Run Step", "Please set the start and end nodes.")
                return

            # Initialize the Dijkstra algorithm variables
            self.step_state = {
                "dist": [INF] * (self.num_nodes + 1),
                "visited": [False] * (self.num_nodes + 1),
                "parent": [-1] * (self.num_nodes + 1),
                "current_node": -1,
                "steps": 0,
                "adj": self.convert_edges_to_adj(self.edges, self.num_nodes),
            }
            self.step_state["dist"][self.start_node] = 0
            # self.Log.delete('1.0', tk.END)
            self.Log.insert(tk.END, f"Starting Dijkstra from Node {self.start_node}\n")
            self.Log.see(tk.END)

        state = self.step_state
        adj = state["adj"]

        # Find the next unvisited node with the smallest distance
        u = -1
        for i in range(1, self.num_nodes + 1):
            if not state["visited"][i] and (u == -1 or state["dist"][i] < state["dist"][u]):
                u = i

        if u == -1 or state["dist"][u] == INF:
            self.Log.insert(tk.END, "No further steps possible or no path exists.\n")
            self.Log.see(tk.END)
            del self.step_state
            return

        # Mark the current node as visited
        state["visited"][u] = True
        state["current_node"] = u
        self.Log.insert(tk.END, f"Visiting Node {u}, Distance: {state['dist'][u]}\n")
        self.Log.see(tk.END)

        # Update distances for adjacent nodes
        for v, w in adj[u]:
            if state["dist"][v] > state["dist"][u] + w:
                state["dist"][v] = state["dist"][u] + w
                state["parent"][v] = u
                self.Log.insert(tk.END, f"Updated Distance to Node {v}: {state['dist'][v]} (via Node {u})\n")
                self.Log.see(tk.END)

        # Highlight the current node and edges in the graph
        self.CanvasDraw.delete("all")
        self.redraw_graph()

        # Highlight all visited nodes in blue
        for node in range(1, self.num_nodes + 1):
            if state["visited"][node]:
                self.draw_node(node, *self.nodes[node], text_color="white", bg_color="blue")        

        self.draw_node(u, *self.nodes[u], text_color="white", bg_color="blue")  # Highlight current node
        for v, w in adj[u]:
            if state["visited"][v]:
                self._draw_edge(u, v, 0, bg_color="green")  # Highlight visited edges
            else:
                self._draw_edge(u, v, 0, bg_color="orange")  # Highlight potential edges

        state["steps"] += 1

        # Check if we reached the end node
        if u == self.end_node:
            # Reconstruct the path
            path = []
            current = self.end_node
            while current != -1:
                path.append(current)
                current = state["parent"][current]
            path.reverse()
            self.Log.insert(tk.END, f"Reached Node {self.end_node}. Shortest path: {' -> '.join(map(str, path))}\n")
            self.Log.see(tk.END)
            self.highlight_path(path)
            del self.step_state  # Reset step state after completion


    def run_all(self):
        num_nodes = len(self.nodes)
        if num_nodes == 0:
            messagebox.showinfo("Run All", "No nodes to run.")
            return        
        if self.start_node is None or self.end_node is None:
            messagebox.showinfo("Run All", "Please set the start and end nodes.")
            return

        adj = self.convert_edges_to_adj(self.edges, len(self.nodes))
        print(adj)
        distance, path = self.dijkstra_find_path(num_nodes, adj, self.start_node, self.end_node)
        print(path)
        if distance == INF:
            # self.Log.delete('1.0', tk.END)
            self.Log.insert(tk.END, f"No path exists from Node {self.start_node} to Node {self.end_node}\n")
            self.Log.see(tk.END)
        else:
            # self.Log.delete('1.0', tk.END)
            self.Log.insert(tk.END, f"Shortest distance from Node {self.start_node} to Node {self.end_node}: {distance}\n") 
            self.Log.insert(tk.END, f"Path: {' -> '.join(map(str, path))}")
            self.Log.see(tk.END)
            self.highlight_path(path)

    def enable_set_start_node(self):
        self.current_action = "set_start_node"
        # self.Log.delete('1.0', tk.END)
        self.Log.insert(tk.END, "Current Action: Set Start Node\n")           
        self.Log.see(tk.END)

    def enable_set_end_node(self):
        self.current_action = "set_end_node"
        # self.Log.delete('1.0', tk.END)
        self.Log.insert(tk.END, "Current Action: Set End Node\n")     
        self.Log.see(tk.END)      
              

    def update_matrix(self):
        num_nodes = len(self.nodes)
        if num_nodes == 0:
            messagebox.showinfo("Update Matrix", "No nodes to update the matrix.")
            return
        
        # Create adjacency matrix
        matrix = [[float('inf')] * num_nodes for _ in range(num_nodes)]
        for i in range(num_nodes):
            matrix[i][i] = 0

        for node1, node2, weight in self.edges:
            matrix[node1 - 1][node2 - 1] = weight
            matrix[node2 - 1][node1 - 1] = weight

        # for row in matrix:
        #     print(row)
            

        self.matrix_view["columns"] = [str(i + 1) for i in range(num_nodes)]

        # Set column headers and fixed widths
        for i in range(num_nodes):
            self.matrix_view.heading(str(i + 1), text=f"{i + 1}")
            self.matrix_view.column(str(i + 1), width=40, anchor="center", stretch=False)

        self.matrix_view.delete(*self.matrix_view.get_children())

        for i, row in enumerate(matrix):
            row_data = ["∞" if value == float('inf') else value for value in row]
            self.matrix_view.insert("", "end", values=row_data)

    def enable_add_node(self):
        self.current_action = "add_node"
        self.selected_nodes.clear()
        # self.Log.delete('1.0', tk.END)
        self.Log.insert(tk.END, "Current Action: Add Node\n")       
        self.Log.see(tk.END) 

    
    def enable_add_line(self):
        self.current_action = "add_line"
        self.selected_nodes.clear()
        # self.Log.delete('1.0', tk.END)
        self.Log.insert(tk.END, "Current Action: Add Line\n")     
        self.Log.see(tk.END)     

    
    def enable_move(self):
        self.current_action = "move"
        self.selected_nodes.clear()
        # self.Log.delete('1.0', tk.END)
        self.Log.insert(tk.END, "Current Action: Move Node\n")  
        self.Log.see(tk.END)         
    
    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)
    
    def on_click(self, event):
        if self.current_action == "add_node":
            self.add_node(event.x, event.y)
        elif self.current_action == "add_line":
            self.select_node_for_line(event.x, event.y)
        elif self.current_action == "move":
            self.select_node_for_move(event.x, event.y)
        elif self.current_action == "set_start_node":
            self.select_start_node(event.x, event.y)
        elif self.current_action == "set_end_node":
            self.select_end_node(event.x, event.y)
    
    def on_drag(self, event):
        if self.current_action == "move" and self.moving_node:
            self.move_node(self.moving_node, event.x, event.y)
    
    def on_release(self, event):
        self.moving_node = None
    
    def add_node(self, x, y):
        self.node_count += 1
        node_id = self.node_count
        self.nodes[node_id] = (x, y)
        self.draw_node(node_id, x, y, text_color="black", bg_color="skyblue")
    
    def draw_node(self, node_id, x, y, text_color="black", bg_color="skyblue"):
        r = 20
        self.CanvasDraw.create_oval(
            x - r, y - r, x + r, y + r, fill=bg_color, tags=f"node_{node_id}"
        )
        self.CanvasDraw.create_text(
            x, y, text=str(node_id), tags=f"node_{node_id}_text", fill=text_color
        )
    
    def select_node_for_line(self, x, y):
        node_id = self.get_node_at_position(x, y)
        if node_id:
            self.selected_nodes.append(node_id)
            if len(self.selected_nodes) == 2:
                self.add_edge(*self.selected_nodes)
                self.selected_nodes.clear()
    
    def add_edge(self, node1_id, node2_id):
        weight = simpledialog.askstring("Input Weight", f"Enter weight for edge {node1_id}-{node2_id}:")
        if weight is None or not weight.isdigit():
            messagebox.showwarning("Invalid Input", "Weight must be a positive integer.")
            return
        weight = int(weight)
        self.edges.append((node1_id, node2_id, weight))
        self.draw_edge(node1_id, node2_id, weight)
    
    def draw_edge(self, node1_id, node2_id, weight, bg_color="black"):
        x1, y1 = self.nodes[node1_id]
        x2, y2 = self.nodes[node2_id]
        r = 20 
        
        dx, dy = x2 - x1, y2 - y1
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance == 0: 
            return

        x1_edge = x1 + r * dx / distance
        y1_edge = y1 + r * dy / distance
        x2_edge = x2 - r * dx / distance
        y2_edge = y2 - r * dy / distance

        self.CanvasDraw.create_line(
            x1_edge, y1_edge, x2_edge, y2_edge, tags=f"edge_{node1_id}_{node2_id}", fill=bg_color
        )

        offset = 10
        perp_dx = -dy / distance * offset 
        perp_dy = dx / distance * offset

        mid_x, mid_y = (x1_edge + x2_edge) / 2, (y1_edge + y2_edge) / 2
        self.CanvasDraw.create_text(
            mid_x + perp_dx, mid_y + perp_dy, text=str(weight), tags=f"edge_{node1_id}_{node2_id}_text"
        )

    def _draw_edge(self, node1_id, node2_id, weight, bg_color="black"):
        x1, y1 = self.nodes[node1_id]
        x2, y2 = self.nodes[node2_id]
        r = 20 
        
        dx, dy = x2 - x1, y2 - y1
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance == 0: 
            return

        x1_edge = x1 + r * dx / distance
        y1_edge = y1 + r * dy / distance
        x2_edge = x2 - r * dx / distance
        y2_edge = y2 - r * dy / distance

        self.CanvasDraw.create_line(
            x1_edge, y1_edge, x2_edge, y2_edge, tags=f"edge_{node1_id}_{node2_id}", fill=bg_color
        )      
    
    def redraw_graph(self):
        # Redraw all nodes
        for node_id, (x, y) in self.nodes.items():
            self.draw_node(node_id, x, y, text_color="black", bg_color="skyblue")

        # Redraw all edges
        for node1, node2, weight in self.edges:
            self.draw_edge(node1, node2, weight)

    def select_start_node(self, x, y):
        node_id = self.get_node_at_position(x, y)
        if node_id:
            self.start_node = node_id
            self.CanvasDraw.delete("all")
            self.redraw_graph()
            if self.start_node:
                self.draw_node(node_id, *self.nodes[self.start_node], text_color="white", bg_color="green")
            if self.end_node:
                self.draw_node(self.end_node, *self.nodes[self.end_node], text_color="white", bg_color="red")

    def select_end_node(self, x, y):
        node_id = self.get_node_at_position(x, y)
        if node_id:
            self.end_node = node_id
            self.CanvasDraw.delete("all")
            self.redraw_graph()
            if self.end_node:
                self.draw_node(node_id, *self.nodes[self.end_node], text_color="white", bg_color="red")
            if self.start_node:
                self.draw_node(self.start_node, *self.nodes[self.start_node], text_color="white", bg_color="green")

    def select_node_for_move(self, x, y):
        node_id = self.get_node_at_position(x, y)
        if node_id:
            self.moving_node = node_id
    
    def move_node(self, node_id, x, y):
        self.nodes[node_id] = (x, y)
        self.CanvasDraw.delete(f"node_{node_id}")
        self.CanvasDraw.delete(f"node_{node_id}_text")
        self.draw_node(node_id, x, y, text_color="black", bg_color="skyblue")
        if self.start_node and self.start_node == node_id:
            self.draw_node(node_id, *self.nodes[self.start_node], text_color="white", bg_color="green")
        if self.end_node and self.end_node == node_id:
            self.draw_node(self.end_node, *self.nodes[self.end_node], text_color="white", bg_color="red")        
        self.update_edges(node_id)
    
    def update_edges(self, node_id):
        for edge in self.edges:
            if node_id in edge[:2]:
                self.CanvasDraw.delete(f"edge_{edge[0]}_{edge[1]}")
                self.CanvasDraw.delete(f"edge_{edge[0]}_{edge[1]}_text")                
                self.draw_edge(edge[0], edge[1], edge[2])
    
    def get_node_at_position(self, x, y):
        for node_id, (nx, ny) in self.nodes.items():
            if math.sqrt((nx - x) ** 2 + (ny - y) ** 2) <= 20:
                return node_id
        return None
    
    def new_graph(self):
        if self.nodes or self.edges:
            # Prompt to save the current graph
            answer = messagebox.askyesnocancel(
                "New Graph", 
                "Do you want to save the current graph before starting a new one?"
            )
            
            if answer is None:  # Cancel
                return
            elif answer:  # Yes, save the graph
                self.save_graph()
        
        # Clear the graph data and canvas
        self.nodes.clear()
        self.edges.clear()
        self.start_node = None
        self.end_node = None
        self.node_count = 0
        self.selected_nodes = []
        self.moving_node = None
        self.CanvasDraw.delete("all")
        self.matrix_view.delete(*self.matrix_view.get_children())

    def save_graph(self):
        if not self.nodes:
            messagebox.showinfo("Save Graph", "No nodes to save.")
            return

        file_path = filedialog.asksaveasfilename(
            title="Save Graph",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if not file_path:
            return

        # Save the graph data
        nodes_to_save = {int(k): list(v) for k, v in self.nodes.items()}
        graph_data = {
            "nodes": nodes_to_save,
            "edges": self.edges
        }

        try:
            with open(file_path, 'w') as file:
                json.dump(graph_data, file)
            # messagebox.showinfo("Save Graph", "Graph saved successfully!")
        except Exception as e:
            messagebox.showerror("Save Graph", f"Failed to save graph: {e}")

    def open_graph(self):

        file_path = filedialog.askopenfilename(
            title="Open Graph",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if not file_path:
            return
        self.start_node = None 
        self.end_node = None
        try:
            with open(file_path, 'r') as file:
                graph_data = json.load(file)

            # Load the graph data
            self.nodes = {int(k): tuple(v) for k, v in graph_data["nodes"].items()}
            self.edges = graph_data["edges"]
            self.node_count = len(self.nodes)

            # Clear canvas and redraw
            self.CanvasDraw.delete("all")
            self.redraw_graph()
            self.update_matrix()

        except Exception as e:
            messagebox.showerror("Open Graph", f"Failed to open graph: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphDrawer(root)
    root.mainloop()
