# gui.py
# Simple GUI for the production management system using Tkinter

import tkinter as tk
from tkinter import messagebox
from inventory import Inventory
from customers import CustomerDB
from costs import CostManager
from quotes import Quoter

class App:
    def add_material(self):
        try:
            amt = int(self.material_amt.get())
            self.inventory.add_material(self.material_var.get(), amt)
            messagebox.showinfo("Success", f"Added {amt} {self.material_var.get()} to inventory.")
        except ValueError:
            messagebox.showerror("Error", "Invalid amount.")

    def add_ink(self):
        try:
            amt = int(self.ink_amt.get())
            self.inventory.add_ink(self.ink_var.get(), amt)
            messagebox.showinfo("Success", f"Added {amt} {self.ink_var.get()} ink to inventory.")
        except ValueError:
            messagebox.showerror("Error", "Invalid amount.")

    def show_inventory(self):
        inv = self.inventory.get_inventory()
        msg = f"Materials: {inv['materials']}\nInks: {inv['inks']}"
        messagebox.showinfo("Inventory", msg)

    def add_customer(self):
        name = self.cust_name.get()
        contact = self.cust_contact.get()
        if name:
            self.customers.add_customer(name, contact)
            messagebox.showinfo("Success", f"Added customer {name}.")
        else:
            messagebox.showerror("Error", "Customer name required.")

    def set_material_cost(self):
        try:
            cost = float(self.cost_material_amt.get())
            self.costs.set_material_cost(self.cost_material_var.get(), cost)
            messagebox.showinfo("Success", f"Set {self.cost_material_var.get()} cost to {cost}.")
        except ValueError:
            messagebox.showerror("Error", "Invalid cost.")

    def set_ink_cost(self):
        try:
            cost = float(self.cost_ink_amt.get())
            self.costs.set_ink_cost(self.cost_ink_var.get(), cost)
            messagebox.showinfo("Success", f"Set {self.cost_ink_var.get()} ink cost to {cost}.")
        except ValueError:
            messagebox.showerror("Error", "Invalid cost.")

    def set_markup(self):
        try:
            markup = float(self.markup_amt.get())
            self.costs.set_markup(markup)
            messagebox.showinfo("Success", f"Set markup to {markup*100}%.")
        except ValueError:
            messagebox.showerror("Error", "Invalid markup.")

    def generate_quote(self):
        try:
            material = self.quote_material.get()
            material_qty = int(self.quote_material_qty.get())
            ink = self.quote_ink.get()
            ink_qty = int(self.quote_ink_qty.get())
            quote = self.quoter.generate_quote(material, material_qty, ink, ink_qty)
            cust = self.quote_cust.get()
            if cust:
                self.customers.add_order(cust, {'material': material, 'material_qty': material_qty, 'ink': ink, 'ink_qty': ink_qty, 'quote': quote})
            messagebox.showinfo("Quote", f"Quote: ${quote}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input for quote.")
    def __init__(self, root):
        self.root = root
        self.root.title("Production Manager")
        self.inventory = Inventory()
        self.customers = CustomerDB()
        self.costs = CostManager()
        self.quoter = Quoter(self.costs)
        self.create_widgets()

    def create_widgets(self):
        self.root.minsize(600, 600)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        container = tk.Frame(self.root)
        container.grid(row=0, column=0, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        canvas = tk.Canvas(container)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        scrollable_frame.bind_all("<MouseWheel>", _on_mousewheel)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Inventory Frame
        inv_frame = tk.LabelFrame(scrollable_frame, text="Inventory")
        inv_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        tk.Label(inv_frame, text="Material:").grid(row=0, column=0)
        self.material_var = tk.StringVar(value="paper")
        tk.OptionMenu(inv_frame, self.material_var, "paper", "vinyl").grid(row=0, column=1)
        tk.Label(inv_frame, text="Amount:").grid(row=0, column=2)
        self.material_amt = tk.Entry(inv_frame, width=5)
        self.material_amt.grid(row=0, column=3)
        tk.Button(inv_frame, text="Add", command=self.add_material).grid(row=0, column=4)
        tk.Button(inv_frame, text="Show Inventory", command=self.show_inventory).grid(row=0, column=5)

        # Ink Inventory
        tk.Label(inv_frame, text="Ink:").grid(row=1, column=0)
        self.ink_var = tk.StringVar(value="black")
        tk.OptionMenu(inv_frame, self.ink_var, "black", "white").grid(row=1, column=1)
        tk.Label(inv_frame, text="Amount:").grid(row=1, column=2)
        self.ink_amt = tk.Entry(inv_frame, width=5)
        self.ink_amt.grid(row=1, column=3)
        tk.Button(inv_frame, text="Add Ink", command=self.add_ink).grid(row=1, column=4)

        # Customer Frame
        cust_frame = tk.LabelFrame(scrollable_frame, text="Customers")
        cust_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        tk.Label(cust_frame, text="Name:").grid(row=0, column=0)
        self.cust_name = tk.Entry(cust_frame)
        self.cust_name.grid(row=0, column=1)
        tk.Label(cust_frame, text="Contact:").grid(row=0, column=2)
        self.cust_contact = tk.Entry(cust_frame)
        self.cust_contact.grid(row=0, column=3)
        tk.Button(cust_frame, text="Add Customer", command=self.add_customer).grid(row=0, column=4)

        # Cost Frame
        cost_frame = tk.LabelFrame(scrollable_frame, text="Costs & Markup")
        cost_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        # Material cost
        tk.Label(cost_frame, text="Material:").grid(row=0, column=0)
        self.cost_material_var = tk.StringVar(value="paper")
        tk.OptionMenu(cost_frame, self.cost_material_var, "paper", "vinyl").grid(row=0, column=1)
        tk.Label(cost_frame, text="Cost:").grid(row=0, column=2)
        self.cost_material_amt = tk.Entry(cost_frame, width=7)
        self.cost_material_amt.grid(row=0, column=3)
        tk.Button(cost_frame, text="Set Material Cost", command=self.set_material_cost).grid(row=0, column=4)
        # Ink cost
        tk.Label(cost_frame, text="Ink:").grid(row=1, column=0)
        self.cost_ink_var = tk.StringVar(value="black")
        tk.OptionMenu(cost_frame, self.cost_ink_var, "black", "white").grid(row=1, column=1)
        tk.Label(cost_frame, text="Cost:").grid(row=1, column=2)
        self.cost_ink_amt = tk.Entry(cost_frame, width=7)
        self.cost_ink_amt.grid(row=1, column=3)
        tk.Button(cost_frame, text="Set Ink Cost", command=self.set_ink_cost).grid(row=1, column=4)
        # Markup
        tk.Label(cost_frame, text="Markup (e.g. 0.2 for 20%):").grid(row=2, column=0)
        self.markup_amt = tk.Entry(cost_frame, width=7)
        self.markup_amt.grid(row=2, column=1)
        tk.Button(cost_frame, text="Set Markup", command=self.set_markup).grid(row=2, column=2)

        # Quote Frame
        quote_frame = tk.LabelFrame(scrollable_frame, text="Quote")
        quote_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        tk.Label(quote_frame, text="Customer:").grid(row=0, column=0)
        self.quote_cust = tk.Entry(quote_frame)
        self.quote_cust.grid(row=0, column=1)
        tk.Label(quote_frame, text="Material:").grid(row=1, column=0)
        self.quote_material = tk.StringVar(value="paper")
        tk.OptionMenu(quote_frame, self.quote_material, "paper", "vinyl").grid(row=1, column=1)
        tk.Label(quote_frame, text="Material Qty:").grid(row=1, column=2)
        self.quote_material_qty = tk.Entry(quote_frame, width=5)
        self.quote_material_qty.grid(row=1, column=3)
        tk.Label(quote_frame, text="Ink:").grid(row=2, column=0)
        self.quote_ink = tk.StringVar(value="black")
        tk.OptionMenu(quote_frame, self.quote_ink, "black", "white").grid(row=2, column=1)
        tk.Label(quote_frame, text="Ink Qty:").grid(row=2, column=2)
        self.quote_ink_qty = tk.Entry(quote_frame, width=5)
        self.quote_ink_qty.grid(row=2, column=3)
        tk.Button(quote_frame, text="Generate Quote", command=self.generate_quote).grid(row=3, column=0, columnspan=2)
        try:
            cost = float(self.cost_material_amt.get())
            self.costs.set_material_cost(self.cost_material_var.get(), cost)
            messagebox.showinfo("Success", f"Set {self.cost_material_var.get()} cost to {cost}.")
        except ValueError:
            messagebox.showerror("Error", "Invalid cost.")

    def set_markup(self):
        try:
            markup = float(self.markup_amt.get())
            self.costs.set_markup(markup)
            messagebox.showinfo("Success", f"Set markup to {markup*100}%.")
        except ValueError:
            messagebox.showerror("Error", "Invalid markup.")

    def generate_quote(self):
        try:
            material = self.quote_material.get()
            material_qty = int(self.quote_material_qty.get())
            ink = self.quote_ink.get()
            ink_qty = int(self.quote_ink_qty.get())
            quote = self.quoter.generate_quote(material, material_qty, ink, ink_qty)
            cust = self.quote_cust.get()
            if cust:
                self.customers.add_order(cust, {'material': material, 'material_qty': material_qty, 'ink': ink, 'ink_qty': ink_qty, 'quote': quote})
            messagebox.showinfo("Quote", f"Quote: ${quote}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input for quote.")

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
