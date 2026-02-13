import tkinter as tk
from tkinter import Button, ttk

#Root window
root = tk.Tk()
root.geometry('{}x{}'.format(1280, 720))
root.title('Inventory Managment')
root.config(bg='red')

#create the frames for the widgets
mainframe = tk.Frame(root,background='#DADBD5')
mainframe.pack(fill=tk.BOTH,expand=True)

topbar = tk.Frame(mainframe,height=60,background='#1b263b')
topbar.pack(fill=tk.X,side=tk.TOP)

sidebar = tk.Frame(mainframe,width=180,background='#415a77')
sidebar.pack(fill=tk.Y,side=tk.LEFT)
sidebar.pack_propagate(False)


#Create scrollbar
scrollbar = tk.Scrollbar(mainframe)
scrollbar.pack(side=tk.RIGHT,fill=tk.Y)

#Create the inventory system
tree = ttk.Treeview(mainframe,yscrollcommand=scrollbar.set)
tree['columns'] =list(range(3)) 
tree.heading('#0',text='Product')
tree.heading('0',text='Product ID')
tree.heading('1',text='Cost')
tree.heading('2',text='Amount')
tree.pack(fill=tk.BOTH,expand=True,padx=(0,180),side=tk.BOTTOM)
scrollbar.config(command = tree.yview)
ttk.Style().configure("Treeview", background="#E0E1DD", foreground="black")

#holy i dont want to make a button everytime
class flatbutton:
    def __init__(self,master,h,fill,marginx,marginy,bg,hc,text):
        b = Button(master,height=h,background=bg,highlightcolor=hc,text=text)
        b.pack(fill=fill,padx=marginx,pady=marginy)
        b.config(borderwidth=0)

inventory_Button = flatbutton(sidebar,5,tk.X,(4,4),(4,5),'#acb7c3','#5e8ca7','Inventory System')
homepage_Button = flatbutton(sidebar,5,tk.X,(4,4),(4,5),'#acb7c3','#5e8ca7','Homepage')

#inventory system filler
for x in range(200):
    tree.insert('', 'end', text=f'{x} Example product', values=('value 1','value 2','value 3'))

root.mainloop()
