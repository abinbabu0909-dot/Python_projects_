import requests
import customtkinter
from PIL import Image

# Set the overall theme
customtkinter.set_appearance_mode("dark")

app = customtkinter.CTk()
app.geometry("600x450") # Widened slightly to match the landscape feel of the SVG
app.title("Wheather App")

# Updated background color to match the orange in your design
app.configure(fg_color="#e38b36")

API_KEY = "592826e13ba208386547ce38c45167e9"

def get_weather(event=None):
    city = city_entry.get()

    if not city:
        wheather_report.configure(text="Please enter a city name")
        return

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            wheather_report.configure(text="City not found")
            return

        # Formatting temp as an integer to match the "29" in your mockup
        temp = int(data["main"]["temp"])
        humidity = data["main"]["humidity"]
        desc = data["weather"][0]["description"].title()

        wheather_report.configure(
            text=f"Temperature: {temp}\n"
                 f"Humidity: {humidity}\n"
                 f"Weather: {desc}"
        )

    except:
        wheather_report.configure(text="Error fetching weather")

# --- UI Interface ---

# 1. Title
wheather_title = customtkinter.CTkLabel(app,
    text="WHEATHER APP",
    font=("Arial", 32, "bold"),
    text_color="white")
wheather_title.pack(pady=(25, 10))

# 2. Image (Moved up above the entry box)
try:
    wheather_img = customtkinter.CTkImage(
        Image.open("Weather-rafiki.png"),
        size=(180, 180)) # Adjusted size to fit the stack gracefully
    wheather_img_lab = customtkinter.CTkLabel(app, image=wheather_img, text="")
    wheather_img_lab.pack(pady=(0, 15))
except FileNotFoundError:
    print("Warning: 'Weather-rafiki.png' not found in the directory.")

# 3. Entry box 
city_entry = customtkinter.CTkEntry(master=app,
    placeholder_text="Enter the city name",
    width=300,
    height=35,
    corner_radius=0,
    fg_color="#d9d9d9",
    placeholder_text_color="#555555",
    text_color="black",
    border_width=0)
city_entry.pack(pady=(0, 25))

city_entry.bind("<Return>", get_weather)

# 4. Report Title
wheather_report_title = customtkinter.CTkLabel(app,
    text="Wheather Report :",
    font=("Arial", 22, "bold"),
    text_color="white")
wheather_report_title.pack(pady=(0, 10))

# 5. Report Text 
wheather_report = customtkinter.CTkLabel(app,
    text="Temperature: --\nHumidity: --\nWeather: --",
    font=("Arial", 16),
    text_color="#f0f0f0", # Made slightly off-white to match the design
    justify="center")
wheather_report.pack(pady=(0, 20))

app.mainloop()