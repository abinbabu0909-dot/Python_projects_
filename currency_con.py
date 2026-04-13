import customtkinter as ctk
import requests
from tkinter import messagebox
from PIL import Image

API_KEY = "a9694d800bff07b5e8cb8275"

ctk.set_appearance_mode("light") 

app = ctk.CTk()
app.title("Currency Converter")
app.geometry("750x450")
    
app.configure(fg_color="#cbf5ce") 

currencies = [
    "USD", "INR", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY"
]

def convert_currency(event=None): 
    try:
        amount = float(amount_entry.get())
        from_currency = from_currency_var.get()
        to_currency = to_currency_var.get()

        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{from_currency}"
        response = requests.get(url, timeout=10)
        data = response.json()

        rate = data["conversion_rates"][to_currency]
        result = amount * rate

        # Update the result labels
        result_title.configure(text="Currency converted")
        result_path.configure(text=f"{from_currency} => {to_currency}")
        result_label.configure(
            text=f"{amount} {from_currency} = {result:.2f} {to_currency}"
        )

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number.")
    except KeyError:
        messagebox.showerror("Error", "Invalid currency selected.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch exchange rate\n{e}")

# --- UI Layout ---

# Main Title (Centered at the top now)
ctk.CTkLabel(app, 
    text="CURRENCY CONVERTER", 
    font=("Arial", 32, "bold"), 
    text_color="black").pack(pady=(30, 0))

# Left Frame (for inputs and text)
left_frame = ctk.CTkFrame(app, fg_color="transparent")
left_frame.place(x=50, y=110) # Moved down slightly to accommodate the top title

# Amount Entry 
amount_entry = ctk.CTkEntry(left_frame, 
    placeholder_text="Enter the Amount", 
    width=300, height=35, 
    corner_radius=0, 
    fg_color="#d9d9d9", 
    placeholder_text_color="#555",
    text_color="black",
    border_width=0)
amount_entry.pack(anchor="w", pady=(0, 20))

amount_entry.bind("<Return>", convert_currency) 

# Dropdowns Frame 
dropdown_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
dropdown_frame.pack(anchor="w", pady=(0, 20))

# From Currency
from_currency_var = ctk.StringVar(value="USD")
ctk.CTkOptionMenu(dropdown_frame, 
    values=currencies, variable=from_currency_var, 
    width=135, height=35, corner_radius=0, 
    fg_color="#4b9afb", button_color="#0f51a1", button_hover_color="#0a3973").pack(side="left", padx=(0, 30))

# To Currency
to_currency_var = ctk.StringVar(value="INR")
ctk.CTkOptionMenu(dropdown_frame, 
    values=currencies, variable=to_currency_var, 
    width=135, height=35, corner_radius=0, 
    fg_color="#4b9afb", button_color="#0f51a1", button_hover_color="#0a3973").pack(side="left")

# Convert Button
ctk.CTkButton(left_frame, text="Convert", command=convert_currency, 
    width=300, height=35, corner_radius=0, 
    fg_color="#4b9afb", hover_color="#3a82db", text_color="white", font=("Arial", 14)).pack(anchor="w", pady=(0, 30))

# Results Section (Text color updated to black)
result_title = ctk.CTkLabel(left_frame, text="", font=("Arial", 18, "bold"), text_color="black")
result_title.pack(pady=(0, 5))

result_path = ctk.CTkLabel(left_frame, text="", font=("Arial", 16), text_color="black")
result_path.pack(pady=(0, 5))

result_label = ctk.CTkLabel(left_frame, text="", font=("Arial", 16), text_color="black")
result_label.pack()

# Right Frame (for the image)
right_frame = ctk.CTkFrame(app, fg_color="transparent")
right_frame.place(x=400, y=90) 

# Image setup
try:
    coins_img = ctk.CTkImage(Image.open("Money income-bro.png"), size=(300, 300)) 
    img_label = ctk.CTkLabel(right_frame, image=coins_img, text="")
    img_label.pack()
except FileNotFoundError:
    print("Warning: 'Coins-amico.png' not found in the directory.")

app.mainloop()