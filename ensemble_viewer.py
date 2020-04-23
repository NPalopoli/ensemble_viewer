from tkinter import *
from tkinter import ttk
from functools import partial

window = Tk()
window.title("Visualizador de ensembles")
window.geometry("800x600")
#window.resizable(False,False)


tab_parent = ttk.Notebook(window)
tabs_abiertas= []
tabs_dict = dict()
tab_selector = ttk.Frame(tab_parent)
tab_parent.add(tab_selector,text="Select protein")
tab_parent.pack(expand=1,fill="both")


# Carga un dicionario con laa info para el listbox.
protein_dict = dict()
protein_dict[0] = ["P00001","DKRGTRHTRHTRH$KCFKKKDJEJCW------xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"]
protein_dict[1] = ["P00A11","ASASASASADEDASASASASADEV$KCFKKKDJEJCW"]
protein_dict[2] = ["P20S01","aaasasSSSSSSSSSSSCW"]
#crea una lista
protein_listbox = Listbox(tab_selector)
for i in protein_dict:
    protein_listbox.insert(i,protein_dict[i][0])

protein_listbox.place(x=10,y=10)

container_dict = dict()
canvas_dict = dict()
scrollbar_dict =dict()
scrollable_frame_dict =dict()
buton_dict = dict()
residue_info_dict =dict()
res_labels_dict = dict()

def click_aa(uniprot_id,index,protein_seq):
    message = "Pos: " + str(index) + "\n "
    message += "Aminoacido: "+protein_seq[index]+ "\n "
    message += "Propiedad 1: "+str( (index+1)**5+index )
    residue_info_dict[uniprot_id].configure(text=message)
    for but_id in buton_dict[uniprot_id]:
        if str(index) == but_id:
            buton_dict[uniprot_id][but_id].configure(background="#eeee11")
        else:
            buton_dict[uniprot_id][but_id].configure(background="#ffaaaa")


def create_protein_tab(uniprot_id,protein_seq):
    if not uniprot_id in tabs_abiertas:
        tabs_dict[uniprot_id] = ttk.Frame(tab_parent)
        tab_parent.add(tabs_dict[uniprot_id],text=uniprot_id)
        tabs_abiertas.append(uniprot_id)

        container_dict[uniprot_id] = ttk.Frame(tabs_dict[uniprot_id],height=50)
        canvas_dict[uniprot_id] = Canvas(container_dict[uniprot_id],bg="#aaaaff",height=50,width=780)
        scrollbar_dict[uniprot_id] = ttk.Scrollbar(container_dict[uniprot_id], orient="horizontal", command=canvas_dict[uniprot_id].xview)
        scrollable_frame_dict[uniprot_id] = ttk.Frame(canvas_dict[uniprot_id],height=50)

        scrollable_frame_dict[uniprot_id].bind(
            "<Configure>",
            lambda e: canvas_dict[uniprot_id].configure(
                scrollregion=canvas_dict[uniprot_id].bbox("all")
            )
        )

        canvas_dict[uniprot_id].create_window((0, 0), window=scrollable_frame_dict[uniprot_id], anchor="nw")

        canvas_dict[uniprot_id].configure(xscrollcommand=scrollbar_dict[uniprot_id].set)
        container_dict[uniprot_id].place(x=10,y=10)
        scrollbar_dict[uniprot_id].pack(side="bottom", fill="x")
        canvas_dict[uniprot_id].pack(side="left", fill="y", expand=True)



        buton_dict[uniprot_id] = dict()
        res_labels_dict[uniprot_id] = dict()
        for i,aa in enumerate(protein_seq):
            buton_dict[uniprot_id][str(i)] = Button(scrollable_frame_dict[uniprot_id],activebackground="#ffffaa",background ="#ffaaaa",text=aa,width=1,height=1,padx=4,pady=0,command= partial(click_aa,uniprot_id,i,protein_seq))
            buton_dict[uniprot_id][str(i)].grid(row=0,column=i)
            res_labels_dict[uniprot_id][str(i)] = Label(scrollable_frame_dict[uniprot_id],text=str(i))
            res_labels_dict[uniprot_id][str(i)].grid(row=1,column=i)
        	#buton_dict[str(i)].place(x=5+20*i,y=4)
        residue_info_dict[uniprot_id] = Label(tabs_dict[uniprot_id],text="Click to show info",bg="#aaffaa")
        residue_info_dict[uniprot_id].place(x=400,y=150)


def seleccionar():
    a = protein_listbox.curselection()
    print (a,protein_dict[a[0]])
    uniprot_id = protein_dict[a[0]][0]
    protein_seq= protein_dict[a[0]][1]

    create_protein_tab(uniprot_id,protein_seq)

select_button = Button(tab_selector,text="Select",command=seleccionar)
select_button.place(x=500,y=100,)


window.mainloop()
