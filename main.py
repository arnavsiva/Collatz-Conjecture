import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

memo = {}

def collatz_sequence(n):
    if n in memo:
        return memo[n]
    original_n = n
    sequence = [n]
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        sequence.append(n)
    memo[original_n] = sequence
    return sequence

def update_plot():
    try:
        start = int(start_var.get())
        end = int(end_var.get())
        update_iterations_list(start, end)
    except ValueError:
        listbox.delete(0, tk.END)
        listbox.insert(tk.END, "Start or End is not a number")

def update_iterations_list(start, end):
    listbox.delete(0, tk.END)
    for number in range(start, end + 1):
        sequence = collatz_sequence(number)
        listbox.insert(tk.END, f"Number: {number}, Iterations: {len(sequence) - 1}")

def update_sequence_display():
    try:
        number = int(number_var.get())
        sequence = collatz_sequence(number)
        update_graph(sequence)
    except ValueError:
        listbox.delete(0, tk.END)
        listbox.insert(tk.END, "Number is not a number")

def update_graph(sequence):
    ax.clear()
    ax.plot(sequence, marker='o')
    for i, value in enumerate(sequence):
        ax.annotate(str(value), (i, value), textcoords="offset points", xytext=(0,10), ha='center')
    ax.set_xlabel('Step')
    ax.set_ylabel('Value')
    ax.set_title('Collatz Conjecture Path')
    ax.grid(True)
    canvas.draw()

def on_closing():
    root.quit()
    root.destroy()

root = tk.Tk()
root.title("Collatz Conjecture Visualization")
root.protocol("WM_DELETE_WINDOW", on_closing)
root.state('zoomed')

fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)

overlay_frame = tk.Frame(root, bg='white', bd=2, relief=tk.RAISED)
overlay_frame.place(relx=0, rely=0, relwidth=0.25, relheight=1, anchor='nw')

overlay_frame.grid_rowconfigure(4, weight=1)

start_label = ttk.Label(overlay_frame, text="Start:")
start_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
start_var = tk.StringVar(value="1")
start_entry = ttk.Entry(overlay_frame, textvariable=start_var, width=10)
start_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

end_label = ttk.Label(overlay_frame, text="End:")
end_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
end_var = tk.StringVar(value="10")
end_entry = ttk.Entry(overlay_frame, textvariable=end_var, width=10)
end_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

update_button = ttk.Button(overlay_frame, text="Update", command=update_plot)
update_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

listbox_heading = ttk.Label(overlay_frame, text="Iterations List", font=("Helvetica", 16))
listbox_heading.grid(row=3, column=0, columnspan=2, pady=10, padx=5, sticky=tk.W)

listbox_frame = tk.Frame(overlay_frame)
listbox_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.N, tk.S, tk.E, tk.W), padx=5, pady=5)
listbox_frame.grid_rowconfigure(0, weight=1)
listbox_frame.grid_columnconfigure(0, weight=1)

scrollbar = tk.Scrollbar(listbox_frame)
scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set)
listbox.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
scrollbar.config(command=listbox.yview)

right_frame = ttk.Frame(overlay_frame)
right_frame.grid(row=0, column=2, rowspan=5, sticky=(tk.N, tk.S), padx=5, pady=5)

number_label = ttk.Label(right_frame, text="Number:")
number_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
number_var = tk.StringVar(value="1")
number_entry = ttk.Entry(right_frame, textvariable=number_var, width=10)
number_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

show_sequence_button = ttk.Button(right_frame, text="Show Sequence", command=update_sequence_display)
show_sequence_button.grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)

update_plot()

root.mainloop()
