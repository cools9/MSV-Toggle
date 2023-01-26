import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from Toggle_interpreter import Interpreter

class IDE:
    def __init__(self):
        self.interpreter = Interpreter()
        self.root = tk.Tk()
        self.root.title("Toggle IDE")

        self.text_widget = tk.Text(self.root)
        self.text_widget.pack()

        self.run_button = tk.Button(self.root, text="Run", command=self.run_code)
        self.run_button.pack()

        self.open_button = tk.Button(self.root, text="Open", command=self.open_file)
        self.open_button.pack()

        self.save_button = tk.Button(self.root, text="Save", command=self.save_file)
        self.save_button.pack()
        
        self.output_widget = tk.Text(self.root)
        self.output_widget.pack()

    def run_code(self):
        code = self.text_widget.get("1.0", "end")
        try:
            output = self.interpreter.execute(code)
            self.output_widget.insert("end", output)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            print(str(e))

    def open_file(self):
        filepath = filedialog.askopenfilename()
        with open(filepath, "r") as file:
            code = file.read()
            self.text_widget.delete("1.0", "end")
            self.text_widget.insert("1.0", code)

    def save_file(self):
        filepath = filedialog.asksaveasfilename()
        with open(filepath, "w") as file:
            code = self.text_widget.get("1.0", "end")
            file.write(code)

    def run(self):
        self.root.mainloop()

ide = IDE()
ide.run()
