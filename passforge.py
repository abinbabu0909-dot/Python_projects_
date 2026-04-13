import customtkinter as ctk
import random
import string
from tkinter import messagebox

class PasswordGeneratorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title("Password Generate")
        self.geometry("450x520")
        ctk.set_appearance_mode("dark")

        # --- Custom Theme: Sunset / Ember ---
        self.BG_COLOR = "#1c1917"          # Warm Dark Gray (Ash)
        self.CARD_COLOR = "#292524"        # Slightly lighter gray for cards
        self.ACCENT = "#f97316"            # Vibrant Orange (Ember)
        self.ACCENT_HOVER = "#ea580c"      # Darker Orange
        self.TEXT_MAIN = "#fafaf9"         # Off-white
        self.TEXT_MUTED = "#a8a29e"        # Muted gray text

        self.configure(fg_color=self.BG_COLOR)

        # --- HEADER ---
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(pady=(35, 15), fill="x")

        ctk.CTkLabel(header, text="Password Generate", font=ctk.CTkFont(size=28, weight="bold"), text_color=self.ACCENT).pack()
        ctk.CTkLabel(header, text="Warm, secure, and fast generation.", font=ctk.CTkFont(size=14), text_color=self.TEXT_MUTED).pack()

        # --- TOP CARD: SETTINGS ---
        settings_card = ctk.CTkFrame(self, fg_color=self.CARD_COLOR, corner_radius=12)
        settings_card.pack(padx=30, pady=10, fill="x")

        # Length Input (Manual Text Entry)
        length_frame = ctk.CTkFrame(settings_card, fg_color="transparent")
        length_frame.pack(pady=(20, 10), padx=20, fill="x")

        ctk.CTkLabel(length_frame, text="Password Length:", font=ctk.CTkFont(size=16, weight="bold"), text_color=self.TEXT_MAIN).pack(side="left")

        self.length_entry = ctk.CTkEntry(length_frame, placeholder_text="16", width=80, height=35, corner_radius=6,
                                         fg_color=self.BG_COLOR, border_width=1, border_color=self.TEXT_MUTED, text_color=self.TEXT_MAIN,
                                         font=ctk.CTkFont(size=16, weight="bold"), justify="center")
        self.length_entry.insert(0, "16")
        self.length_entry.pack(side="right")
        self.length_entry.bind("<Return>", lambda event: self.generate_password())

        # Symbols Checkbox
        self.special_var = ctk.BooleanVar(value=True)
        self.special_cb = ctk.CTkCheckBox(settings_card, text="Include Symbols (!@#$)", variable=self.special_var,
                                          font=ctk.CTkFont(size=14), text_color=self.TEXT_MAIN,
                                          fg_color=self.ACCENT, hover_color=self.ACCENT_HOVER, border_color=self.TEXT_MUTED)
        self.special_cb.pack(pady=(10, 20), padx=20, anchor="w")

        # --- BOTTOM CARD: ACTION & RESULT ---
        action_card = ctk.CTkFrame(self, fg_color=self.CARD_COLOR, corner_radius=12)
        action_card.pack(padx=30, pady=10, fill="x")

        # Generate Button
        self.generate_btn = ctk.CTkButton(action_card, text="GENERATE", height=50, corner_radius=6,
                                          font=ctk.CTkFont(size=16, weight="bold"),
                                          fg_color=self.ACCENT, hover_color=self.ACCENT_HOVER, text_color="white",
                                          command=self.generate_password)
        self.generate_btn.pack(fill="x", padx=20, pady=(20, 15))

        # Result Display Box
        self.result_entry = ctk.CTkEntry(action_card, height=50, corner_radius=6, font=ctk.CTkFont(size=20, weight="bold"),
                                         justify="center", fg_color=self.BG_COLOR, border_width=1, border_color=self.ACCENT, text_color=self.ACCENT)
        self.result_entry.pack(fill="x", padx=20, pady=(0, 15))
        self.result_entry.insert(0, "Ready to generate")
        self.result_entry.configure(state="readonly")

        # Copy Button
        self.copy_btn = ctk.CTkButton(action_card, text="Copy to Clipboard", height=35, corner_radius=6,
                                      font=ctk.CTkFont(size=14, weight="bold"),
                                      fg_color="transparent", border_width=1, border_color=self.TEXT_MUTED, text_color=self.TEXT_MAIN, hover_color=self.BG_COLOR,
                                      command=self.copy_to_clipboard)
        self.copy_btn.pack(pady=(0, 20), padx=20, fill="x")

    # --- Logic Functions ---

    def generate_password(self):
        # Validate the manual input safely
        length_str = self.length_entry.get().strip()
        
        if not length_str:
            messagebox.showerror("Error", "Please enter a password length.")
            return
            
        try:
            length = int(length_str)
            if length <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive number.")
            return

        use_special = self.special_var.get()

        # Build character pool
        characters = string.ascii_letters + string.digits
        if use_special:
            characters += string.punctuation

        # Generate password
        password = "".join(random.choices(characters, k=length))

        # Update the entry box
        self.result_entry.configure(state="normal") 
        self.result_entry.delete(0, "end")
        self.result_entry.insert(0, password)
        self.result_entry.configure(state="readonly") 

        # Reset copy button text
        self.copy_btn.configure(text="Copy to Clipboard", text_color=self.TEXT_MAIN, border_color=self.TEXT_MUTED)

    def copy_to_clipboard(self):
        password = self.result_entry.get()
        
        if password and password != "Ready to generate":
            self.clipboard_clear()
            self.clipboard_append(password)
            self.update() 
            
            # Visual feedback on copy
            self.copy_btn.configure(text="✓ Copied!", text_color=self.ACCENT, border_color=self.ACCENT)
            self.after(2000, lambda: self.copy_btn.configure(text="Copy to Clipboard", text_color=self.TEXT_MAIN, border_color=self.TEXT_MUTED))

if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.mainloop()
