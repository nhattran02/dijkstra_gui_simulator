import tkinter as tk
from tkinter import simpledialog, messagebox, ttk, filedialog
import math
import json

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
        self.Log.place(relx=0.011, rely=0.729, relheight=0.05, relwidth=0.971)
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
        self.CanvasDraw.place(relx=0.333, rely=0.017, relheight=0.7
                , relwidth=0.656)
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


        # ------------------------------------------
        # Right Click Menu
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
        self.CanvasDraw.bind("<Button-1>", self.on_click)
        self.CanvasDraw.bind("<B1-Motion>", self.on_drag)
        self.CanvasDraw.bind("<ButtonRelease-1>", self.on_release)
        self.CanvasDraw.bind("<Button-3>", self.show_context_menu)          

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
        self.CanvasDraw.create_oval(
            x - r, y - r, x + r, y + r,
            fill="skyblue", tags=f"node_{node_id}"
        )
        self.CanvasDraw.create_text(
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

        self.CanvasDraw.create_line(
            x1_edge, y1_edge, x2_edge, y2_edge, tags=f"edge_{node1_id}_{node2_id}"
        )

        offset = 10
        perp_dx = -dy / distance * offset 
        perp_dy = dx / distance * offset

        mid_x, mid_y = (x1_edge + x2_edge) / 2, (y1_edge + y2_edge) / 2
        self.CanvasDraw.create_text(
            mid_x + perp_dx, mid_y + perp_dy, text=str(weight), tags=f"edge_{node1_id}_{node2_id}_text"
        )
    
    def redraw_graph(self):
        # Redraw all nodes
        for node_id, (x, y) in self.nodes.items():
            self.draw_node(node_id, x, y)

        # Redraw all edges
        for node1, node2, weight in self.edges:
            self.draw_edge(node1, node2, weight)


    def select_node_for_move(self, x, y):
        node_id = self.get_node_at_position(x, y)
        if node_id:
            self.moving_node = node_id
    
    def move_node(self, node_id, x, y):
        self.nodes[node_id] = (x, y)
        self.CanvasDraw.delete(f"node_{node_id}")
        self.CanvasDraw.delete(f"node_{node_id}_text")
        self.draw_node(node_id, x, y)
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
