import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pyotp
import time
import json
import os

DATA_FILE = "totp_data.json"

class MultiTOTPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Account TOTP Generator")
        self.root.geometry("350x250")
        self.root.resizable(False, False)

        self.accounts = self.load_accounts()
        self.current_account = None
        self.totp = None

        # Dropdown to select account
        self.account_var = tk.StringVar()
        self.account_menu = ttk.Combobox(root, textvariable=self.account_var, state="readonly")
        self.account_menu['values'] = list(self.accounts.keys())
        self.account_menu.bind("<<ComboboxSelected>>", self.change_account)
        self.account_menu.pack(pady=10)

        # TOTP code display
        self.code_var = tk.StringVar(value="------")
        self.code_label = ttk.Label(root, textvariable=self.code_var, font=("Helvetica", 24, "bold"))
        self.code_label.pack()

        # Progress bar
        self.progress = ttk.Progressbar(root, length=250, mode='determinate', maximum=30)
        self.progress.pack(pady=10)

        # Add account button
        self.add_button = ttk.Button(root, text="Add Account", command=self.add_account)
        self.add_button.pack(pady=5)

        # Edit account button
        self.edit_button = ttk.Button(root, text="Edit Account", command=self.edit_account)
        self.edit_button.pack(pady=5)

        # Delete account button
        self.delete_button = ttk.Button(root, text="Delete Account", command=self.delete_account)
        self.delete_button.pack(pady=5)

        # Start update loop
        self.update_loop()

    def load_accounts(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        return {}

    def save_accounts(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.accounts, f)

    def add_account(self):
        name = simpledialog.askstring("Account Name", "Enter account name:")
        if not name:
            return

        secret = simpledialog.askstring("Secret Key", "Enter base32 TOTP secret:")
        if not secret:
            return

        self.accounts[name] = secret
        self.save_accounts()
        self.account_menu['values'] = list(self.accounts.keys())
        self.account_var.set(name)
        self.change_account()

    def edit_account(self):
        selected = self.account_var.get()
        if selected:
            new_name = simpledialog.askstring("Edit Account Name", f"New name for {selected}:")
            if new_name and new_name != selected:
                if new_name in self.accounts:
                    messagebox.showerror("Error", "Account name already exists!")
                    return
                self.accounts[new_name] = self.accounts.pop(selected)

            new_secret = simpledialog.askstring("Edit Secret Key", "New base32 TOTP secret:")
            if new_secret:
                self.accounts[new_name or selected] = new_secret

            self.save_accounts()
            self.account_menu['values'] = list(self.accounts.keys())
            self.account_var.set(new_name or selected)
            self.change_account()
        else:
            messagebox.showwarning("Select Account", "Please select an account to edit.")

    def delete_account(self):
        selected = self.account_var.get()
        if selected:
            confirm = messagebox.askyesno("Delete Account", f"Are you sure you want to delete the account '{selected}'?")
            if confirm:
                del self.accounts[selected]
                self.save_accounts()
                self.account_menu['values'] = list(self.accounts.keys())
                self.account_var.set("")
                self.change_account()
        else:
            messagebox.showwarning("Select Account", "Please select an account to delete.")

    def change_account(self, event=None):
        selected = self.account_var.get()
        if selected in self.accounts:
            try:
                self.totp = pyotp.TOTP(self.accounts[selected])
                self.current_account = selected
                self.code_var.set(self.totp.now())
            except Exception as e:
                messagebox.showerror("Error", f"Failed to set TOTP for {selected}: {e}")
                self.totp = None
                self.code_var.set("------")
        else:
            self.totp = None
            self.code_var.set("------")

    def update_loop(self):
        try:
            if self.totp:
                seconds_remaining = 30 - (int(time.time()) % 30)
                if seconds_remaining == 30 or self.code_var.get() == "------":
                    self.code_var.set(self.totp.now())
                self.progress['value'] = 30 - seconds_remaining
            else:
                self.code_var.set("------")
                self.progress['value'] = 0
        except Exception as e:
            self.code_var.set("ERROR")
            print("Update error:", e)

        self.root.after(1000, self.update_loop)

if __name__ == "__main__":
    root = tk.Tk()
    app = MultiTOTPApp(root)
    root.mainloop()
