import tkinter as tk
from tkinter import ttk
from clients import OrderTrackingClient, DroneManagerClient
from pb_grpc.order_tracking_pb2 import Status
class DeliveryApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.order_status = "NOT_CREATED"
        self.create_widgets()
        self.start_timer()
        self.x = 0
        self.y = 0
        self.order_id = ""
        self.order_tracking_client = OrderTrackingClient("localhost","50051")
        self.drone_manager_client = DroneManagerClient("localhost","50052")
        with open("my_location.txt") as file:
            data = file.read().split(",")
            self.x = float(data[1])
            self.y = float(data[0])

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

        self.order_button = tk.Button(self.button_canvas, text="Place Order", font=("Arial", 16), fg="#ffffff", bg="#7289da", activebackground="#99aab5", relief="flat", borderwidth=0, highlightthickness=0, command=self.command_order)
        self.order_button_window = self.button_canvas.create_window(100, 20, window=self.order_button)

        # round the button
        self.order_button.configure(width=20, height=2)
        self.order_button.config(highlightbackground="#2c2f33", highlightcolor="#2c2f33")

        # create rounded button shape
        self.button_canvas.create_oval(0, 0, 25, 40, outline="#7289da", fill="#7289da")
        self.button_canvas.create_oval(175, 0, 200, 40, outline="#7289da", fill="#7289da")
        self.button_canvas.create_rectangle(12.5, 0, 187.5, 40, outline="#7289da", fill="#7289da")

    def start_timer(self):
        self.master.after(10000, self.change_order_status)

    def command_order(self):
        if self.order_status == "NOT_CREATED":
            self.order_id = self.drone_manager_client.set_goal(self.x,self.y,20)
        if self.order_status == "COMPLETED":
            self.drone_manager_client.land_drone()




    def change_order_status(self):
        print("in refresh")
        if self.order_id != "":
            status = self.order_tracking_client.get_order_status(self.order_id)
            print(status)
            self.order_status = Status.Name(status)
            self.status_label.configure(text="Order Status: " + self.order_status.title())
            if self.order_status == "COMPLETED":
                self.order_button.configure(text="Land Drone")
        self.start_timer()


root = tk.Tk()
app = DeliveryApp(master=root)
app.mainloop()