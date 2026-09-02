import tkinter as tk
from tkinter import Text, END, messagebox, filedialog
import datetime
import pdf_create as pc
import os



#Window conf
width = 750
height = 350

root = tk.Tk()
root.minsize(width, height)
root.resizable(False, False)
root.title("VAGNLSYS")
menu = tk.Menu(root)
root.config(menu=menu)

save_path = str(os.getcwd())
print(f"Settings: save location{save_path}")

def button_create_clicked():
    id = order_id_entry.get().strip()
    date = date_entry.get().strip()
    description = description_text.get("1.0", "end-1c").strip()

    

    #Checks if id box is empty, and if date box is empty prompts user with ask box.
    if not id:
        print("Skriv in ett order nummer!")
        messagebox.showwarning("Varning", "Du måste fylla i ett ordernummer!")
        return 

    if not date:
        if not messagebox.askokcancel("Varning", "Datum ej angiven"):
            return

    #print(f"{id}, {date}, {description}")

    data = {
        "id": id,
        "date": date,
        "description": description,
        "save_path": save_path
    }

    try:
        pc.create_pdf(data)
    except PermissionError:
        messagebox.showerror("Åtkomst nekad", "Kunde inte spara PDF-filen.")
        return
    except OSError as e:
        messagebox.showerror("Filfel", f"Ett systemfel uppstod vid sparandet:\n{e}")
        return
    except Exception as e:
        messagebox.showerror("Oväntat fel", f"Ett oväntat fel uppstod:\n{e}")
        return

    #Resets the input boxes for next session
    if messagebox.askyesno("Klart", f"PDF sparad till:\n{save_path}\n\nTa bort föregående detaljer?"):
        order_id_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)
        date_entry.insert(tk.END, todays_date)

        description_text.delete("1.0", tk.END)
    

def button_save_to_clicked():
    global save_path
    new_path = filedialog.askdirectory()
    if new_path:
        save_path = new_path
        print(f"Ny sparplats {save_path}")
    

#Todays date
tz = datetime.timezone.utc
ft = "%Y-%m-%d"
todays_date = datetime.datetime.now(tz=tz).strftime(ft)

#Menu
filemenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Filer", menu=filemenu)
#filemenu.add_command(label="New")
#filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

settings = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Inställningar", menu=settings)
settings.add_command(label="Spara till", command= button_save_to_clicked)


#helpmenu = tk.Menu(menu, tearoff=0)
#menu.add_cascade(label="Hjälp", menu=helpmenu)
#helpmenu.add_command(label="Om")



# En övergripande behållare för raden högst upp
top_frame = tk.Frame(root)
top_frame.pack(fill="x", padx=10, pady=10)

# Vänster sida (Order Unit4)
left_frame = tk.Frame(top_frame)
left_frame.pack(side="left")

#Order id box 
tk.Label(left_frame, text="Order Unit4:").pack(side="left", padx=(0, 10))
order_id_entry = tk.Entry(left_frame)
order_id_entry.pack(side="left")
order_id_entry.focus()

# Höger sida (Datum) - packas med side="right" för att tryckas ut till kanten
right_frame = tk.Frame(top_frame)
right_frame.pack(side="right")

tk.Label(right_frame, text="Datum:").pack(side="left", padx=(0, 10))
date_entry = tk.Entry(right_frame)
date_entry.pack(side="left")
date_entry.insert(END, todays_date)

# Beskrivning under
desc_frame = tk.Frame(root)
desc_frame.pack(fill="x", padx=10, pady=10)

tk.Label(desc_frame, text="Beskrivning:").pack(anchor="w", pady=(0, 5))
description_text = Text(desc_frame, height=10, width=50)
description_text.pack(anchor="w")
#description_text.insert("1.0", "GeeksforGeeks\nBEST WEBSITE\n")


button_create_pdf = tk.Button(root, text="Skapa etikett", width=25, command=button_create_clicked)
button_create_pdf.pack(side="left", pady=(0, 5))

root.mainloop()