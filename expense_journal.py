import customtkinter as ctk
from tkinter import messagebox

class ExpenseTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title("Expense Tracker")
        self.geometry("600x700") # Taller and narrower for a vertical layout
        ctk.set_appearance_mode("dark")
        
        # --- Custom Theme: Midnight & Coral ---
        self.BG_COLOR = "#0f0c29"          # Very deep purple/black
        self.CARD_COLOR = "#1e1b4b"        # Midnight purple panel
        self.ITEM_CARD = "#312e81"         # Lighter purple for list items
        self.ACCENT_COLOR = "#f43f5e"      # Neon Coral/Pink
        self.ACCENT_HOVER = "#e11d48"      # Darker Coral
        self.TEXT_MAIN = "white"
        self.TEXT_MUTED = "#a5b4fc"        # Soft indigo for subtitles
        
        self.configure(fg_color=self.BG_COLOR)

        # --- Data Storage ---
        self.expenses = []

        # --- Top Section: Total Display ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(pady=(40, 20), fill="x")

        ctk.CTkLabel(self.header_frame, text="TOTAL SPENT", font=ctk.CTkFont(size=14, weight="bold"), text_color=self.TEXT_MUTED).pack()
        self.total_label = ctk.CTkLabel(self.header_frame, text="₹0.00", font=ctk.CTkFont(size=48, weight="bold"), text_color=self.ACCENT_COLOR)
        self.total_label.pack(pady=(5, 0))

        # --- Middle Section: Inputs (Horizontal Row) ---
        self.input_card = ctk.CTkFrame(self, fg_color=self.CARD_COLOR, corner_radius=15)
        self.input_card.pack(pady=10, padx=30, fill="x")

        # Container to hold inputs side-by-side
        input_container = ctk.CTkFrame(self.input_card, fg_color="transparent")
        input_container.pack(pady=20, padx=20, fill="x")

        self.cat_entry = ctk.CTkEntry(input_container, placeholder_text="Category (e.g., Food)", 
                                      height=40, corner_radius=8, font=ctk.CTkFont(size=14),
                                      fg_color="#0f0c29", border_color="#4338ca", border_width=1)
        self.cat_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.amt_entry = ctk.CTkEntry(input_container, placeholder_text="Amount", width=100,
                                      height=40, corner_radius=8, font=ctk.CTkFont(size=14),
                                      fg_color="#0f0c29", border_color="#4338ca", border_width=1)
        self.amt_entry.pack(side="left", padx=(0, 10))
        
        self.amt_entry.bind("<Return>", lambda event: self.log_expense())

        self.action_btn = ctk.CTkButton(input_container, text="Add", width=80, height=40, corner_radius=8,
                                        font=ctk.CTkFont(size=14, weight="bold"),
                                        fg_color=self.ACCENT_COLOR, hover_color=self.ACCENT_HOVER, text_color="white",
                                        command=self.log_expense)
        self.action_btn.pack(side="left")

        # --- Bottom Section: Scrollable List ---
        list_title_frame = ctk.CTkFrame(self, fg_color="transparent")
        list_title_frame.pack(fill="x", padx=40, pady=(20, 5))
        ctk.CTkLabel(list_title_frame, text="Recent Transactions", font=ctk.CTkFont(size=16, weight="bold"), text_color=self.TEXT_MAIN).pack(side="left")

        self.summary_list = ctk.CTkScrollableFrame(self, fg_color="transparent", scrollbar_button_color=self.CARD_COLOR)
        self.summary_list.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.update_summary()

    # --- CRUD LOGIC ---

    def log_expense(self):
        category = self.cat_entry.get().strip().title()
        amount_str = self.amt_entry.get().strip()

        if not category or not amount_str:
            messagebox.showerror("Error", "Please fill in both fields.")
            return

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Error", "That doesn't look like a valid number.")
            return

        self.expenses.insert(0, {"category": category, "amount": amount}) # Insert at 0 so newest is on top
        
        self.clear_inputs()
        self.update_summary()
        self.cat_entry.focus()

    def edit_expense(self, index):
        expense = self.expenses[index]
        
        self.clear_inputs()
        self.cat_entry.insert(0, expense["category"])
        self.amt_entry.insert(0, str(expense["amount"]))
        
        self.action_btn.configure(text="Update", fg_color="#6366f1", hover_color="#4f46e5", 
                                  command=lambda: self.update_expense(index))

    def update_expense(self, index):
        category = self.cat_entry.get().strip().title()
        amount_str = self.amt_entry.get().strip()

        if not category or not amount_str:
            return

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Error", "Invalid number format.")
            return

        self.expenses[index] = {"category": category, "amount": amount}
        
        self.clear_inputs()
        self.update_summary()
        
        self.action_btn.configure(text="Add", fg_color=self.ACCENT_COLOR, hover_color=self.ACCENT_HOVER, 
                                  command=self.log_expense)

    def remove_expense(self, index):
        del self.expenses[index]
        
        if self.action_btn.cget("text") == "Update":
            self.clear_inputs()
            self.action_btn.configure(text="Add", fg_color=self.ACCENT_COLOR, hover_color=self.ACCENT_HOVER, command=self.log_expense)

        self.update_summary()

    def clear_inputs(self):
        self.cat_entry.delete(0, 'end')
        self.amt_entry.delete(0, 'end')

    def update_summary(self):
        for widget in self.summary_list.winfo_children():
            widget.destroy()

        if not self.expenses:
            ctk.CTkLabel(self.summary_list, text="No records yet.", font=ctk.CTkFont(size=14, slant="italic"), text_color=self.TEXT_MUTED).pack(pady=40)
            self.total_label.configure(text="₹0.00")
            return

        total_spent = 0.0

        for index, item in enumerate(self.expenses):
            total_spent += item['amount']
            
            # Individual Item Card
            row = ctk.CTkFrame(self.summary_list, fg_color=self.ITEM_CARD, corner_radius=10)
            row.pack(fill="x", pady=6, padx=10)
            
            # Category label (Left)
            ctk.CTkLabel(row, text=item['category'], font=ctk.CTkFont(size=16, weight="bold"), text_color=self.TEXT_MAIN).pack(side="left", padx=15, pady=15)
            
            # Action Buttons (Right)
            remove_btn = ctk.CTkButton(row, text="✕", width=30, height=30, corner_radius=6, font=ctk.CTkFont(weight="bold"),
                                       fg_color="transparent", text_color=self.TEXT_MUTED, hover_color="#881337", 
                                       command=lambda i=index: self.remove_expense(i))
            remove_btn.pack(side="right", padx=(5, 10))

            edit_btn = ctk.CTkButton(row, text="✎", width=30, height=30, corner_radius=6, font=ctk.CTkFont(size=16),
                                     fg_color="transparent", text_color=self.TEXT_MUTED, hover_color="#3730a3", 
                                     command=lambda i=index: self.edit_expense(i))
            edit_btn.pack(side="right", padx=(10, 0))

            # Amount Label (Right)
            ctk.CTkLabel(row, text=f"₹{item['amount']:.2f}", font=ctk.CTkFont(size=16), text_color=self.ACCENT_COLOR).pack(side="right", padx=10)

        self.total_label.configure(text=f"₹{total_spent:.2f}")

if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.mainloop()
