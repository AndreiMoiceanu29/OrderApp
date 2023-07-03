import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pb_grpc.order_tracking_pb2 import Status
from clients import DroneManagerClient, OrderTrackingClient
from clients import create_company, get_companies, update_company, delete_company
from clients import create_product, get_products, update_product, delete_product, get_product_by_id
from pb_grpc.companies_pb2 import Company as CompanyPB
from pb_grpc.products_pb2 import Product as ProductPB
import ast
class Company:
    def __init__(self, id, name, owner):
        self.id = id
        self.name = name
        self.owner = owner
        self.num_products = 0
        self.product_ids = []


class Product:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price


class DeliveryApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.companies = []
        self.products = []
        self.create_widgets()
        self.order_status = "NOT_CREATED"
        self.create_companies_table()
        self.selected_company_id = ""
        # self.create_products_table()
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
        # Set window title
        self.master.title("Delivery App")

        # Set window to full-screen
        self.master.geometry("1920x1080")
        self.master.resizable(True, True)

        title_label = tk.Label(self, text="Drone Delivery - Order App", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)

        # Create companies table
        self.companies_table = ttk.Treeview(self, columns=("Owner", "Num Products"))
        self.companies_table.heading("#0", text="Company Name")
        self.companies_table.heading("Owner", text="Company Owner")
        self.companies_table.heading("Num Products", text="Num Products")
        self.companies_table.pack(padx=10, pady=10)
        self.companies_table.bind("<<TreeviewSelect>>", self.on_company_select)

        # Create products table
        self.products_table = ttk.Treeview(self, columns=("Price"))
        self.products_table.heading("#0", text="Product Name")
        self.products_table.heading("Price", text="Price")
        self.products_table.pack(padx=10, pady=(0, 10))

        # Create buttons for companies CRUD operations
        self.create_company_button = tk.Button(self, text="Create Company", command=self.create_company_popup)
        self.create_company_button.pack(side=tk.LEFT, padx=10)

        self.update_company_button = tk.Button(self, text="Update Company", command=self.update_company_popup)
        self.update_company_button.pack(side=tk.LEFT, padx=10)

        self.delete_company_button = tk.Button(self, text="Delete Company", command=self.delete_company)
        self.delete_company_button.pack(side=tk.LEFT, padx=10)

        # Create buttons for products CRUD operations
        self.create_product_button = tk.Button(self, text="Create Product", command=self.create_product_popup)
        self.create_product_button.pack(side=tk.LEFT, padx=10)

        self.update_product_button = tk.Button(self, text="Update Product", command=self.update_product_popup)
        self.update_product_button.pack(side=tk.LEFT, padx=10)

        self.delete_product_button = tk.Button(self, text="Delete Product", command=self.delete_product)
        self.delete_product_button.pack(side=tk.LEFT, padx=10)

        # Create Make Order button
        self.make_order_button = tk.Button(self, text="Make Order", command=self.make_order_popup)
        self.make_order_button.pack(side=tk.LEFT, padx=10)

    def on_company_select(self, event):
        selected_item = self.get_selected_item(self.companies_table)
        self.selected_company_id = selected_item["values"][-1]
        self.create_products_table()

    def create_company_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Create Company")

        label_name = tk.Label(popup, text="Company Name:")
        label_name.pack()
        entry_name = tk.Entry(popup)
        entry_name.pack()

        label_owner = tk.Label(popup, text="Company Owner:")
        label_owner.pack()
        entry_owner = tk.Entry(popup)
        entry_owner.pack()

        create_button = tk.Button(popup, text="Create", command=lambda: self.create_company(entry_name.get(), entry_owner.get()))
        create_button.pack()

    def create_company(self, name, owner):
        if name and owner:
            new_company = Company("",name, owner)
            self.companies.append(new_company)
            company_pb = CompanyPB(name=new_company.name, owner_name=new_company.owner)
            created_company = create_company(company_pb)
            new_company.id = created_company.id
            new_company.product_ids = created_company.product_ids
            self.companies_table.insert('', tk.END, text=new_company.name,
                                        values=(new_company.owner, new_company.num_products,str(new_company.product_ids),new_company.id))
            messagebox.showinfo("Success", "Company created successfully.")
        else:
            messagebox.showerror("Error", "Please provide both name and owner for the company.")

    def update_company_popup(self):
        selected_item = self.get_selected_item(self.companies_table)
        selected_item_ref = self.get_selected_item_ref(self.companies_table)
        if selected_item:
            print(selected_item)
            popup = tk.Toplevel(self)
            popup.title("Update Company")

            label_name = tk.Label(popup, text="Company Name:")
            label_name.pack()
            entry_name = tk.Entry(popup)
            entry_name.insert(0, selected_item["text"])
            entry_name.pack()

            label_owner = tk.Label(popup, text="Company Owner:")
            label_owner.pack()
            entry_owner = tk.Entry(popup)
            entry_owner.insert(0, selected_item["values"][0])
            entry_owner.pack()

            update_button = tk.Button(popup, text="Update",
                                      command=lambda: self.update_company(selected_item_ref,selected_item, entry_name.get(), entry_owner.get()))
            update_button.pack()
        else:
            messagebox.showerror("Error", "No company selected.")

    def update_company(self,ref, selected_item, name, owner):
        if name and owner:
            selected_item["text"] = name
            selected_item["values"] = (owner, selected_item["values"][1],selected_item["values"][2],selected_item["values"][3])
            self.companies_table.item(ref, text=selected_item["text"], values=selected_item["values"])
            old_company_id = selected_item["values"][-1]
            company_pb = CompanyPB(name=name, owner_name=owner)
            update_company(old_company_id=old_company_id,company=company_pb)
            messagebox.showinfo("Success", "Company updated successfully.")
        else:
            messagebox.showerror("Error", "Please provide both name and owner for the company.")

    def delete_company(self):
        selected_item_ref = self.get_selected_item_ref(self.companies_table)
        selected_item = self.get_selected_item(self.companies_table)
        if selected_item:
            self.companies_table.delete(selected_item_ref)
            company_id = selected_item["values"][-1]
            delete_company(company_id=company_id)
            messagebox.showinfo("Success", "Company deleted successfully.")
        else:
            messagebox.showerror("Error", "No company selected.")

    def create_product_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Create Product")

        label_name = tk.Label(popup, text="Product Name:")
        label_name.pack()
        entry_name = tk.Entry(popup)
        entry_name.pack()

        label_price = tk.Label(popup, text="Price:")
        label_price.pack()
        entry_price = tk.Entry(popup)
        entry_price.pack()

        create_button = tk.Button(popup, text="Create", command=lambda: self.create_product(entry_name.get(), entry_price.get()))
        create_button.pack()

    def create_product(self, name, price):
        if name and price:
            new_product = Product("",name, price)
            self.products.append(new_product)
            prod = ProductPB(name=new_product.name, price=new_product.price)
            created_product = create_product(prod)
            new_product.id = created_product.id
            selected_company = self.get_selected_item(self.companies_table)
            selected_comp = CompanyPB(name=selected_company["text"], owner_name=selected_company["values"][0])
            selected_comp.id = selected_company["values"][-1]
            selected_comp.product_ids.append(new_product.id)
            update_company(old_company_id=selected_comp.id,company=selected_comp)
            self.products_table.insert('', tk.END, text=new_product.name, values=(new_product.price,new_product.id))
            messagebox.showinfo("Success", "Product created successfully.")
        else:
            messagebox.showerror("Error", "Please provide both name and price for the product.")

    def update_product_popup(self):
        selected_item = self.get_selected_item(self.products_table)
        selected_item_ref = self.get_selected_item_ref(self.products_table)
        if selected_item:
            popup = tk.Toplevel(self)
            popup.title("Update Product")

            label_name = tk.Label(popup, text="Product Name:")
            label_name.pack()
            entry_name = tk.Entry(popup)
            entry_name.insert(0, selected_item["text"])
            entry_name.pack()

            label_price = tk.Label(popup, text="Price:")
            label_price.pack()
            entry_price = tk.Entry(popup)
            entry_price.insert(0, selected_item["values"][0])
            entry_price.pack()

            update_button = tk.Button(popup, text="Update",
                                      command=lambda: self.update_product(selected_item_ref,selected_item, entry_name.get(), entry_price.get()))
            update_button.pack()
        else:
            messagebox.showerror("Error", "No product selected.")

    def update_product(self, selected_item_ref, selected_item, name, price):
        if name and price:
            selected_item["text"] = name
            selected_item["values"] = (selected_item["values"][0],selected_item["values"][1])
            self.products_table.item(selected_item_ref, text=selected_item["text"], values=selected_item["values"])
            old_product_id = selected_item["values"][-1]
            print(old_product_id)
            prod = ProductPB(name=name, price=price)
            update_product(old_product_id=old_product_id,product=prod)
            messagebox.showinfo("Success", "Product updated successfully.")
        else:
            messagebox.showerror("Error", "Please provide both name and price for the product.")

    def delete_product(self):
        selected_item = self.get_selected_item(self.products_table)
        selected_item_ref = self.get_selected_item_ref(self.products_table)
        if selected_item:
            self.products_table.delete(selected_item_ref)
            product_id = selected_item["values"][-1]
            selected_company = self.get_selected_item(self.companies_table)
            selected_comp = CompanyPB(name=selected_company["text"], owner_name=selected_company["values"][0],product_ids=ast.literal_eval(selected_company["values"][2]))
            selected_comp.id = selected_company["values"][-1]
            selected_comp.product_ids.remove(product_id)
            update_company(old_company_id=selected_comp.id,company=selected_comp)
            delete_product(product_id=product_id)
            messagebox.showinfo("Success", "Product deleted successfully.")
        else:
            messagebox.showerror("Error", "No product selected.")

    def make_order_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Make Order")

        # Insert the code for the order popup from the provided code snippet

        popup.configure(bg="#2c2f33")

        # Create and place status label
        self.status_label = tk.Label(popup, text="Order Status: " + self.order_status.title(), font=("Arial", 16), fg="#ffffff", bg="#2c2f33", pady=20)
        self.status_label.pack()

        # Create and place order button
        button_canvas = tk.Canvas(popup, width=200, height=40, bg="#2c2f33", highlightthickness=0)
        button_canvas.pack(pady=(0, 20))

        self.order_button = tk.Button(button_canvas, text="Place Order", font=("Arial", 16), fg="#ffffff", bg="#7289da", activebackground="#99aab5", relief="flat", borderwidth=0, highlightthickness=0, command=self.command_order)
        order_button_window = button_canvas.create_window(100, 20, window=self.order_button)

        # Round the button
        self.order_button.configure(width=20, height=2)
        self.order_button.config(highlightbackground="#2c2f33", highlightcolor="#2c2f33")

        # Create rounded button shape
        button_canvas.create_oval(0, 0, 25, 40, outline="#7289da", fill="#7289da")
        button_canvas.create_oval(175, 0, 200, 40, outline="#7289da", fill="#7289da")
        button_canvas.create_rectangle(12.5, 0, 187.5, 40, outline="#7289da", fill="#7289da")

    def get_selected_item(self, treeview):
        selection = treeview.focus()
        if selection:
            return treeview.item(selection)
        return None
    
    def get_selected_item_ref(self, treeview):
        selection = treeview.selection()
        if selection:
            return selection[0]
        return None
    
    def start_timer(self):
        self.master.after(10000, self.change_order_status)

    def command_order(self):
        if self.order_status == "NOT_CREATED":
            self.order_id = self.drone_manager_client.set_goal(self.x,self.y,20)
        if self.order_status == "COMPLETED":
            # self.order_button.configure(text="Land Drone")
            self.drone_manager_client.land_drone()

    def create_companies_table(self):
        # Dummy data
        companies = get_companies()

        # Populate table with data
        for data in companies:
            self.companies_table.insert("", "end", text=data.name, values=(data.owner_name, len(data.product_ids),str(data.product_ids),data.id))

    def create_products_table(self):
        # Dummy data
        selected_company = self.get_selected_item(self.companies_table)
        product_ids = ast.literal_eval(selected_company["values"][2])
        print(product_ids)
        products = []
        # Clear table
        self.products_table.delete(*self.products_table.get_children())
        for product_id in product_ids:
            product_resp = get_product_by_id(product_id)
            if len(product_resp) > 0:
                products.append(product_resp[0])
        # Populate table with data
        for data in products:
            print(f'product_id:{data.id}')
            self.products_table.insert("", "end", text=data.name, values=(data.price,data.id))






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
