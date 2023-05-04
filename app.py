import tkinter as tk
from tkinter import ttk

class DeliveryApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.order_status = "placed"
        self.create_widgets()

    def create_widgets(self):
        # set window title
        self.master.title("Delivery App")

        # set window size and position
        self.master.geometry("400x200+300+200")
        self.master.resizable(False, False)

        # set background color
        self.master.configure(bg="#2c2f33")

        # create and place status label
        self.status_label = tk.Label(self, text="Order Status: " + self.order_status.title(), font=("Arial", 16), fg="#ffffff", bg="#2c2f33", pady=20)
        self.status_label.pack()

        # create and place order button
        self.button_canvas = tk.Canvas(self, width=200, height=40, bg="#2c2f33", highlightthickness=0)
        self.button_canvas.pack(pady=(0, 20))

        self.order_button = tk.Button(self.button_canvas, text="Place Order", font=("Arial", 16), fg="#ffffff", bg="#7289da", activebackground="#99aab5", relief="flat", borderwidth=0, highlightthickness=0, command=self.change_order_status)
        self.order_button_window = self.button_canvas.create_window(100, 20, window=self.order_button)

        # round the button
        self.order_button.configure(width=20, height=2)
        self.order_button.config(highlightbackground="#2c2f33", highlightcolor="#2c2f33")

        # create rounded button shape
        self.button_canvas.create_oval(0, 0, 25, 40, outline="#7289da", fill="#7289da")
        self.button_canvas.create_oval(175, 0, 200, 40, outline="#7289da", fill="#7289da")
        self.button_canvas.create_rectangle(12.5, 0, 187.5, 40, outline="#7289da", fill="#7289da")

    def change_order_status(self):
        if self.order_status == "placed":
            self.order_status = "received"
            self.order_button.configure(text="Take Order")
            self.status_label.configure(text="O rder Status: " + self.order_status.title())
        elif self.order_status == "received":
            self.order_status = "completed"
            self.order_button.configure(text="Complete Order")
            self.status_label.configure(text="Order Status: " + self.order_status.title())
        else:
            self.order_status = "placed"
            self.order_button.configure(text="Place Order")
            self.status_label.configure(text="Order Status: " + self.order_status.title())

root = tk.Tk()
app = DeliveryApp(master=root)
app.mainloop()