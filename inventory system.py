import tkinter as tk
from tkinter import Button, Label, ttk

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
topbar.pack_propagate(False)

sidebar = tk.Frame(mainframe,width=180,background='#415a77')
sidebar.pack(fill=tk.Y,side=tk.LEFT)
sidebar.pack_propagate(False)

logo = tk.Frame(topbar,background='red',width=40,height=40)
logo.pack(side=tk.LEFT,padx=10)

inventory_frame = tk.Frame(mainframe,background='blue')

margin_bar = tk.Frame(inventory_frame,background='gray')
margin_bar.pack(fill=tk.BOTH,side=tk.RIGHT,expand=True)

front_frame = tk.Frame(mainframe,background='orange')
front_frame.pack(side=tk.BOTTOM,expand=True,fill=tk.BOTH)

audit_log_frame = tk.Frame(mainframe,background='red')

company = Label(topbar,text='The Company',bg='#1b263b',font=('Arial',20),foreground='#ffffff')
company.pack(side=tk.LEFT,padx=(0,0))


#Create the inventory system
inventory_scrollbar = tk.Scrollbar(margin_bar)
inventory_scrollbar.pack(side=tk.RIGHT,fill=tk.Y)

inventory_tree = ttk.Treeview(inventory_frame,yscrollcommand=inventory_scrollbar.set)
inventory_tree['columns'] =list(range(4)) 
inventory_tree.heading('#0',text='Product')
inventory_tree.heading('0',text='Product ID')
inventory_tree.heading('1',text='Cost')
inventory_tree.heading('2',text='Amount')
inventory_tree.heading('3',text='Product Sum Price')
inventory_tree.column('1', width=150)
inventory_tree.column('2',width=150)
inventory_tree.pack(fill=tk.BOTH,expand=True,side=tk.LEFT)
inventory_scrollbar.config(command = inventory_tree.yview)
ttk.Style().configure("Treeview", background="#E0E1DD", foreground="black")
inventory_tree.pack_propagate(False)




def tree_delete():
    iid = inventory_tree.selection()[0]
    inventory_tree.delete(iid)
    return

def tree_edit():
    for item in inventory_tree.selection():
        item = inventory_tree.item(item)
        val = item['values']
        edit_popup(val)
    return


m = tk.Menu(inventory_frame,tearoff=0)
m.add_command(label='Edit',command= tree_edit)
m.add_command(label='Delete',command= tree_delete)


def rclick(event):
    try:
        click = inventory_tree.identify_row(event.y)
        inventory_tree.selection_set(click)
        m.tk_popup(event.x_root,event.y_root)
    finally:
        m.grab_release()

inventory_tree.bind("<Button-3>",lambda event : rclick(event))


#Create the log tree
log_scrollbar = tk.Scrollbar(audit_log_frame)
log_scrollbar.pack(side=tk.RIGHT,fill=tk.Y)

log_tree = ttk.Treeview(audit_log_frame,yscrollcommand=log_scrollbar.set)
log_tree['columns'] =list(range(2)) 
log_tree.heading('#0',text='Product')
log_tree.heading('0',text='Product ID')
log_tree.heading('1',text='Stock Change')
log_tree.pack(fill=tk.BOTH,expand=True,side=tk.BOTTOM)
log_scrollbar.config(command = log_tree.yview)
ttk.Style().configure("Treeview", background="#E0E1DD", foreground="black")


#button class
class flatbutton:
    def __init__(self,master,h,fill,marginx,marginy,bg,hc,text,cmd):
        b = Button(master,height=h,background=bg,highlightcolor=hc,text=text,command=cmd)
        b.pack(fill=fill,padx=marginx,pady=marginy)
        b.config(borderwidth=0)

def open_inventory_frame():
    inventory_frame.pack(side=tk.BOTTOM,expand=True,fill=tk.BOTH)
    front_frame.pack_forget()
    audit_log_frame.pack_forget()
    return 

def open_front_frame():
    front_frame.pack(side=tk.BOTTOM,expand=True,fill=tk.BOTH)
    inventory_frame.pack_forget()
    audit_log_frame.pack_forget()
    return

def open_log_frame():
    front_frame.pack_forget()
    inventory_frame.pack_forget()
    audit_log_frame.pack(side=tk.BOTTOM,expand=True,fill=tk.BOTH)
    return

def edit_popup(text):
    pop = tk.Toplevel(root)
    pop.geometry("400x200")
    product = tk.StringVar()
    product_id = tk.StringVar()
    cost = tk.StringVar()
    amount = tk.StringVar()
    
    class textentry:
        def __init__(self,name,strvar,text):
            xpad = 70
            framec = tk.Frame(pop)
            framec.pack(fill=tk.X,expand=True)
            label = tk.Label(framec,text=name)
            label.pack(side=tk.LEFT,padx=(xpad,0))
            enter = tk.Entry(framec,textvariable=strvar)
            enter.insert(0,text)
            enter.pack(side=tk.RIGHT,padx=(0,xpad))

    def inventory_insert():
        c = cost.get()
        a = amount.get()
        total_sum = float(a)*float(c)
        inventory_tree.insert('','end',text=f'{product.get()}',values=(f'{product_id.get()}',f'{c}',f'{a}',f'{total_sum:.2f}'))
        return 
    
    textentry('Product:',product,text[0])
    textentry('Product_ID:',product_id,text[1])
    textentry('Cost:',cost,text[2])
    textentry('Amount:',amount,text[3])
    
    bframe = tk.Frame(pop)
    bframe.pack(fill=tk.X,expand=True)
    add_button = tk.Button(bframe,text='Add',width=4,height=1,font=('Arial',13),command=inventory_insert)
    add_button.pack(fill=tk.Y)
    return


def add_popup():
    pop = tk.Toplevel(root)
    pop.geometry("400x200")
    product = tk.StringVar()
    product_id = tk.StringVar()
    cost = tk.StringVar()
    amount = tk.StringVar()

    class textentry:
        def __init__(self,name,strvar,text):
            xpad = 70
            framec = tk.Frame(pop)
            framec.pack(fill=tk.X,expand=True)
            label = tk.Label(framec,text=name)
            label.pack(side=tk.LEFT,padx=(xpad,0))
            enter = tk.Entry(framec,textvariable=strvar,show=text)
            enter.pack(side=tk.RIGHT,padx=(0,xpad))


    def inventory_insert():
        c = cost.get()
        a = amount.get()
        total_sum = float(a)*float(c)
        inventory_tree.insert('','end',text=f'{product.get()}',values=(f'{product_id.get()}',f'{c}',f'{a}',f'{total_sum:.2f}'))
        return 

    textentry('Product:',product,None)
    textentry('Product_ID:',product_id,None)
    textentry('Cost:',cost,None)
    textentry('Amount:',amount,None)
    
    bframe = tk.Frame(pop)
    bframe.pack(fill=tk.X,expand=True)
    add_button = tk.Button(bframe,text='Add',width=4,height=1,font=('Arial',13),command=inventory_insert)
    add_button.pack(fill=tk.Y)
    return

homepage_Button = flatbutton(sidebar,5,tk.X,(4,4),(4,5),'#acb7c3','#5e8ca7','Homepage', open_front_frame)
inventory_Button = flatbutton(sidebar,5,tk.X,(4,4),(4,5),'#acb7c3','#5e8ca7','Inventory System', open_inventory_frame)
log_button = flatbutton(sidebar,5,tk.X,(4,4),(4,5),'#acb7c3','#5e8ca7','Audit Log', open_log_frame)
add_item = tk.Button(margin_bar,width=3,height=1,text='+',font=('Arial',30),command=add_popup)
add_item.pack(side=tk.BOTTOM,padx=30,pady=40)



#inventory system filler
for x in range(3):
    inventory_tree.insert('', 'end', text=f'{x+1} Example product', values=('value 1','value 2','value 3','value 4'))

root.mainloop()
