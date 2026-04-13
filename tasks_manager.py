import customtkinter as ctk
import json
import os

class TaskManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("TO-DO List")
        self.geometry("420x600")
        
        # Custom Color Palette
        self.NAVY_BG = "#081b29"
        self.CYAN = "#00e5ff"
        self.CYAN_HOVER = "#00b3cc"
        self.TEXT_ON_CYAN = "black"
        
        # Set overall app background
        self.configure(fg_color=self.NAVY_BG)

        self.data_file = "tasks.json"
        self.categories = ["Work", "Personal", "Home", "Other"]
        self.tasks = self.load_tasks()

        # Title
        ctk.CTkLabel(self, text="TO-DO List", font=ctk.CTkFont(size=24, weight="bold"), text_color="white").pack(pady=(20, 15))

        # --- Row 1: Task Entry & Add Button ---
        row1 = ctk.CTkFrame(self, fg_color="transparent")
        row1.pack(pady=5, padx=30, fill="x")

        # Default styling for Entry
        self.task_entry = ctk.CTkEntry(row1, placeholder_text="Enter the task", height=35)
        self.task_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.add_btn = ctk.CTkButton(row1, text="Add", width=60, height=35, 
                                     fg_color=self.CYAN, text_color=self.TEXT_ON_CYAN, 
                                     hover_color=self.CYAN_HOVER, corner_radius=0, 
                                     font=ctk.CTkFont(size=14), command=self.add_task)
        self.add_btn.pack(side="right")

        # --- Row 2: Category & Time Inputs ---
        row2 = ctk.CTkFrame(self, fg_color="transparent")
        row2.pack(pady=5, padx=30, fill="x")

        self.category_var = ctk.StringVar(value="Work")
        # Default styling for OptionMenu
        self.category_menu = ctk.CTkOptionMenu(row2, values=self.categories, variable=self.category_var, width=100, height=30)
        self.category_menu.pack(side="left", padx=(0, 10))

        # Default styling for Entry
        self.time_entry = ctk.CTkEntry(row2, placeholder_text="Time (e.g: 2.00 PM)", height=30)
        self.time_entry.pack(side="left", fill="x", expand=True)


        # --- Main List Box (Large Cyan Rectangle) ---
        self.list_frame = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color=self.CYAN, 
                                                 scrollbar_button_color=self.NAVY_BG)
        self.list_frame.pack(pady=15, padx=30, fill="both", expand=True)

        self.checks = []
        self.populate()


        # --- Bottom Buttons Frame ---
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(pady=(0, 20), padx=30, fill="x")
        
        bottom_frame.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkButton(bottom_frame, text="Check All", height=30, 
                      fg_color=self.CYAN, text_color=self.TEXT_ON_CYAN, 
                      hover_color=self.CYAN_HOVER, corner_radius=0, font=ctk.CTkFont(size=12),
                      command=self.check_all).grid(row=0, column=0, padx=(0, 5), sticky="ew")

        ctk.CTkButton(bottom_frame, text="Clear All", height=30, 
                      fg_color=self.CYAN, text_color=self.TEXT_ON_CYAN, 
                      hover_color=self.CYAN_HOVER, corner_radius=0, font=ctk.CTkFont(size=12),
                      command=self.clear_all).grid(row=0, column=1, padx=5, sticky="ew")

        ctk.CTkButton(bottom_frame, text="Remove (Checked)", height=30, 
                      fg_color=self.CYAN, text_color=self.TEXT_ON_CYAN, 
                      hover_color=self.CYAN_HOVER, corner_radius=0, font=ctk.CTkFont(size=12),
                      command=self.remove_done).grid(row=0, column=2, padx=(5, 0), sticky="ew")


    # ==================== LOGIC ====================

    def load_tasks(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    # Automatically upgrade older simple-string lists to dictionaries
                    if data and isinstance(data[0], str):
                        return [{"text": t, "category": "Work", "time": ""} for t in data]
                    return data
            except json.JSONDecodeError:
                return []
        return []

    def save_tasks(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.tasks, f)

    def get_category_color(self, category):
        colors = {"Work": "#ff8c00", "Personal": "#0055ff", "Home": "#2db83d", "Other": "#555555"}
        return colors.get(category, "#555555")

    def populate(self):
        for w in self.list_frame.winfo_children():
            w.destroy()
        self.checks.clear()
        
        for index, task in enumerate(self.tasks):
            # Create a row container for each task
            row_frame = ctk.CTkFrame(self.list_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=8, padx=5)

            # Checkbox
            cb = ctk.CTkCheckBox(row_frame, text=task["text"], text_color=self.TEXT_ON_CYAN, font=ctk.CTkFont(size=16))
            cb.pack(side="left")
            self.checks.append((cb, task))

            # Edit Button
            edit_btn = ctk.CTkButton(row_frame, text="Edit", width=40, height=24, corner_radius=0,
                                     fg_color=self.NAVY_BG, text_color="white", hover_color="#123a59",
                                     command=lambda i=index: self.edit_task(i))
            edit_btn.pack(side="right", padx=(5, 0))

            # Time Label
            if task.get("time"):
                time_lbl = ctk.CTkLabel(row_frame, text=task["time"], text_color="black", font=ctk.CTkFont(size=12, weight="bold"))
                time_lbl.pack(side="right", padx=(10, 5))

            # Category Badge
            cat_color = self.get_category_color(task.get("category", "Work"))
            cat_badge = ctk.CTkLabel(row_frame, text=task.get("category", "Work"), fg_color=cat_color, text_color="white", 
                                     corner_radius=0, width=50, height=20, font=ctk.CTkFont(size=11, weight="bold"))
            cat_badge.pack(side="right", padx=(10, 0))

    def add_task(self):
        new_text = self.task_entry.get().strip()
        new_category = self.category_var.get()
        new_time = self.time_entry.get().strip()

        if new_text and not any(t["text"] == new_text for t in self.tasks):
            new_task = {"text": new_text, "category": new_category, "time": new_time}
            self.tasks.append(new_task)
            self.save_tasks()
            self.populate() 
            
            self.clear_inputs()

    def edit_task(self, index):
        task = self.tasks[index]
        
        self.clear_inputs()
        self.task_entry.insert(0, task["text"])
        self.category_var.set(task.get("category", "Work"))
        if task.get("time"):
            self.time_entry.insert(0, task["time"])
        
        self.add_btn.configure(text="Update", command=lambda: self.update_task(index))

    def update_task(self, index):
        updated_text = self.task_entry.get().strip()
        if updated_text:
            self.tasks[index]["text"] = updated_text
            self.tasks[index]["category"] = self.category_var.get()
            self.tasks[index]["time"] = self.time_entry.get().strip()
            
            self.save_tasks()
            self.populate()
            
            self.clear_inputs()
            self.add_btn.configure(text="Add", command=self.add_task)

    def clear_inputs(self):
        self.task_entry.delete(0, 'end')
        self.time_entry.delete(0, 'end')
        self.category_var.set("Work")

    def check_all(self):
        for cb, _ in self.checks:
            cb.select()

    def clear_all(self):
        for cb, _ in self.checks:
            cb.deselect()

    def remove_done(self):
        # Keep only the tasks where the checkbox is not selected
        self.tasks = [task for cb, task in self.checks if not cb.get()]
        self.save_tasks()
        self.populate() 

if __name__ == "__main__":
    app = TaskManagerApp()
    app.mainloop()