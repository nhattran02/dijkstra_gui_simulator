import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import math
import ctypes

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
        self.root.title("Graph Drawer")
        
        self.root.geometry("900x700")
        # Canvas
        self.canvas = tk.Canvas(root, bg="white", width=600, height=430)
        self.canvas.pack(side=tk.RIGHT, fill=tk.X, expand=True, anchor='n')


        # Buttons
        self.control_frame = tk.Frame(root)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.log_text = tk.Text(root, bg="lightgray", width=900, height=10)
        self.log_text.pack(side=tk.BOTTOM, fill=tk.X, padx=300)
        self.log_text.insert(tk.END, "Log:\n")

        # self.add_node_button = tk.Button(self.control_frame, text="Add Node", command=self.enable_add_node, width=40)
        # self.add_node_button.pack(pady=5)
        
        # self.add_line_button = tk.Button(self.control_frame, text="Add Line", command=self.enable_add_line, width=40)
        # self.add_line_button.pack(pady=5)
        
        # self.move_button = tk.Button(self.control_frame, text="Move", command=self.enable_move, width=40)
        # self.move_button.pack(pady=5)
        
        self.save_button = tk.Button(self.control_frame, text="Save Graph", command=self.save_graph, width=40)
        self.save_button.pack(pady=5)

        self.update_button = tk.Button(self.control_frame, text="Update Matrix", command=self.update_matrix, width=40)
        self.update_button.pack(pady=5)
        
        # Matrix View
        # self.matrix_view = ttk.Treeview(self.control_frame, show="headings", height=10)
        # self.matrix_view.pack(pady=10, fill=tk.X)

        # Matrix View with Scrollbars
        self.matrix_frame = tk.Frame(self.control_frame, height=300)
        self.matrix_frame.pack(pady=10, fill=tk.X)

        # Horizontal scrollbar
        self.h_scroll = tk.Scrollbar(self.matrix_frame, orient=tk.HORIZONTAL)
        self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        # Vertical scrollbar (optional, in case rows exceed display height)
        self.v_scroll = tk.Scrollbar(self.matrix_frame, orient=tk.VERTICAL)
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.matrix_view = ttk.Treeview(
            self.matrix_frame,
            show="headings",
            height=10,
            xscrollcommand=self.h_scroll.set,
            yscrollcommand=self.v_scroll.set
        )
        self.matrix_view.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Attach scrollbars to the Treeview
        self.h_scroll.config(command=self.matrix_view.xview)
        self.v_scroll.config(command=self.matrix_view.yview)


        # Right-click menu
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Add Node", command=self.enable_add_node)
        self.context_menu.add_command(label="Add Line", command=self.enable_add_line)
        self.context_menu.add_command(label="Move", command=self.enable_move)

        # Graph Data
        self.nodes = {}  # node_id: (x, y)
        self.edges = []  # (node1_id, node2_id, weight)
        self.node_count = 0
        
        # Interaction State
        self.current_action = None
        self.selected_nodes = []
        self.moving_node = None
        
        # Bindings
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Button-3>", self.show_context_menu)
    

    def update_matrix(self):
        print(self.nodes)
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

        for row in matrix:
            print(row)
            

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
    
    def enable_add_line(self):
        self.current_action = "add_line"
        self.selected_nodes.clear()
    
    def enable_move(self):
        self.current_action = "move"
        self.selected_nodes.clear()
    
    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)
    
    def on_click(self, event):
        if self.current_action == "add_node":
            self.add_node(event.x, event.y)
        elif self.current_action == "add_line":
            self.select_node_for_line(event.x, event.y)
        elif self.current_action == "move":
            self.select_node_for_move(event.x, event.y)
    
    def on_drag(self, event):
        if self.current_action == "move" and self.moving_node:
            self.move_node(self.moving_node, event.x, event.y)
    
    def on_release(self, event):
        self.moving_node = None
    
    def add_node(self, x, y):
        self.node_count += 1
        node_id = self.node_count
        self.nodes[node_id] = (x, y)
        self.draw_node(node_id, x, y)
    
    def draw_node(self, node_id, x, y):
        r = 20
        self.canvas.create_oval(
            x - r, y - r, x + r, y + r,
            fill="skyblue", tags=f"node_{node_id}"
        )
        self.canvas.create_text(
            x, y, text=str(node_id), tags=f"node_{node_id}_text"
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
    
    def draw_edge(self, node1_id, node2_id, weight):
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

        self.canvas.create_line(
            x1_edge, y1_edge, x2_edge, y2_edge, tags=f"edge_{node1_id}_{node2_id}"
        )

        offset = 10
        perp_dx = -dy / distance * offset 
        perp_dy = dx / distance * offset

        mid_x, mid_y = (x1_edge + x2_edge) / 2, (y1_edge + y2_edge) / 2
        self.canvas.create_text(
            mid_x + perp_dx, mid_y + perp_dy, text=str(weight), tags=f"edge_{node1_id}_{node2_id}_text"
        )
    
    def select_node_for_move(self, x, y):
        node_id = self.get_node_at_position(x, y)
        if node_id:
            self.moving_node = node_id
    
    def move_node(self, node_id, x, y):
        self.nodes[node_id] = (x, y)
        self.canvas.delete(f"node_{node_id}")
        self.canvas.delete(f"node_{node_id}_text")
        self.draw_node(node_id, x, y)
        self.update_edges(node_id)
    
    def update_edges(self, node_id):
        for edge in self.edges:
            if node_id in edge[:2]:
                self.canvas.delete(f"edge_{edge[0]}_{edge[1]}")
                self.canvas.delete(f"edge_{edge[0]}_{edge[1]}_text")                
                self.draw_edge(edge[0], edge[1], edge[2])
    
    def get_node_at_position(self, x, y):
        for node_id, (nx, ny) in self.nodes.items():
            if math.sqrt((nx - x) ** 2 + (ny - y) ** 2) <= 20:
                return node_id
        return None
    
    def save_graph(self):
        graph_data = {
            "nodes": self.nodes,
            "edges": self.edges,
        }
        messagebox.showinfo("Graph Saved", f"Graph data:\n{graph_data}")


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphDrawer(root)
    root.mainloop()
