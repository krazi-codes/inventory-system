import tkinter as tk
import backend

def create(parent_frame, tree_widget):
    frame = tk.Frame(parent_frame, bg='#1b263b')
    frame.pack(side=tk.RIGHT, padx=10, pady=10)

    entry = tk.Entry(frame)
    entry.pack(side=tk.LEFT, padx=5)

    btn = tk.Button(frame, text="Search", command=lambda: run_search(entry, tree_widget))
    btn.pack(side=tk.LEFT)

def run_search(entry_box, tree):
    search_text = entry_box.get()

    for item in tree.get_children():
        tree.delete(item)

    results = backend.search_database(search_text)

    for row in results:
        tree.insert('', 'end', text=row[1], values=(row[0], row[3], row[2]))
