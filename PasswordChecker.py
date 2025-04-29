import tkinter as tk
from tkinter import messagebox
import string
import random
import re

# Password checking logic
def passwordChecker(password):
    strength = 0
    feedback = []

    if len(password) >= 8:
        strength += 1
    else:
        feedback.append("Use at least 8 characters.")

    if re.search(r'[A-Z]', password) and re.search(r'[a-z]', password):
        strength += 1
    else:
        feedback.append("Include both uppercase and lowercase letters.")

    if re.search(r'\d', password):
        strength += 1
    else:
        feedback.append("Include at least one number.")

    if re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
        strength += 1
    else:
        feedback.append("Include at least one special character.")

    if strength == 4:
        return "Strong", feedback
    elif strength in [2, 3]:
        return "Moderate", feedback
    else:
        return "Weak", feedback

# Generate strong password
def generate_strong_password(length=12):
    all_chars = string.ascii_letters + string.digits + "!@#$%^&*(),.?\":{}|<>"
    while True:
        password = ''.join(random.choice(all_chars) for _ in range(length))
        strength, _ = passwordChecker(password)
        if strength == "Strong":
            return password

# App GUI
class PasswordApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Password Tool")
        self.geometry("500x400")
        self.configure(bg="#f4f4f4")
        self.resizable(False, False)
        
        self.frames = {}
        for Page in (HomePage, GeneratePage, CheckPage):
            frame = Page(self)
            self.frames[Page] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.show_frame(HomePage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

# Home Page
class HomePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f4f4f4")

        tk.Label(self, text="Welcome to Password Pro 🔐", font=("Segoe UI", 20, "bold"), bg="#f4f4f4").pack(pady=30)

        tk.Button(self, text="🔑 Generate Password", font=("Segoe UI", 14), width=25, bg="#2ecc71", fg="white",
                  command=lambda: parent.show_frame(GeneratePage)).pack(pady=20)

        tk.Button(self, text="🛡 Check Password Strength", font=("Segoe UI", 14), width=25, bg="#3498db", fg="white",
                  command=lambda: parent.show_frame(CheckPage)).pack(pady=10)

# Generate Password Page
class GeneratePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f4f4f4")

        tk.Label(self, text="🔑 Your Strong Password", font=("Segoe UI", 16, "bold"), bg="#f4f4f4").pack(pady=20)

        self.generated = tk.StringVar()
        self.generated.set(generate_strong_password())

        self.display = tk.Entry(self, font=("Segoe UI", 14), textvariable=self.generated, width=30, bd=2, justify="center")
        self.display.pack(pady=10)

        tk.Button(self, text="🔁 Regenerate", font=("Segoe UI", 12), command=self.regenerate).pack(pady=5)

        tk.Button(self, text="📋 Copy to Clipboard", font=("Segoe UI", 12),
                  command=self.copy_password).pack(pady=5)

        tk.Button(self, text="⬅ Back", font=("Segoe UI", 10),
                  command=lambda: parent.show_frame(HomePage)).pack(pady=20)

    def regenerate(self):
        self.generated.set(generate_strong_password())

    def copy_password(self):
        self.clipboard_clear()
        self.clipboard_append(self.generated.get())
        messagebox.showinfo("Copied", "Password copied to clipboard!")

# Check Password Strength Page
class CheckPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f4f4f4")

        tk.Label(self, text="🛡 Check Password Strength", font=("Segoe UI", 16, "bold"), bg="#f4f4f4").pack(pady=20)

        self.password_entry = tk.Entry(self, font=("Segoe UI", 12), width=30, show="*")
        self.password_entry.pack(pady=10)

        tk.Button(self, text="Check", font=("Segoe UI", 12), bg="#2980b9", fg="white", command=self.check_password).pack(pady=5)

        self.result = tk.Label(self, text="", font=("Segoe UI", 14, "bold"), bg="#f4f4f4")
        self.feedback = tk.Label(self, text="", font=("Segoe UI", 10), bg="#f4f4f4", fg="#555", wraplength=400, justify="left")

        # Create generate button but don't pack it at the start
        self.generate_button = tk.Button(self, text="Generate Strong Password", font=("Segoe UI", 12),
                                         bg="#27ae60", fg="white", command=self.show_generate_page)
        self.generated_password = tk.Label(self, text="", font=("Segoe UI", 12, "bold"), bg="#f4f4f4")

        tk.Button(self, text="⬅ Back", font=("Segoe UI", 10),
                  command=lambda: parent.show_frame(HomePage)).pack(pady=20)

    def check_password(self):
        password = self.password_entry.get()
        strength, tips = passwordChecker(password)

        color = {"Weak": "red", "Moderate": "orange", "Strong": "green"}[strength]
        self.result.config(text=f"Strength: {strength}", fg=color)
        self.result.pack(pady=10)

        if tips:
            self.feedback.config(text="\n".join(f"• {t}" for t in tips))
        else:
            self.feedback.config(text="Great job! Your password is strong.")
        self.feedback.pack()

        if strength in ["Weak", "Moderate"]:
            self.generate_button.pack(pady=5)
        else:
            self.generate_button.pack_forget()

    def show_generate_page(self):
        self.master.show_frame(GeneratePage)  # Show the GeneratePage when the button is clicked



# Run the app
if __name__ == "__main__":
    app = PasswordApp()
    app.mainloop()
