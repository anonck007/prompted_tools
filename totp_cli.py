import pyotp
import time
import json
import os
import argparse

DATA_FILE = "totp_data.json"

class TOTPManager:
    def __init__(self):
        self.accounts = self.load_accounts()

    def load_accounts(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        return {}

    def save_accounts(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.accounts, f)

    def add_account(self, name, secret):
        if name in self.accounts:
            print(f"Error: Account with name '{name}' already exists.")
            return
        self.accounts[name] = secret
        self.save_accounts()
        print(f"Account '{name}' added successfully.")

    def list_accounts(self):
        if not self.accounts:
            print("No accounts found.")
        else:
            for name in self.accounts:
                print(f"- {name}")

    def display_totp(self, name):
        if name not in self.accounts:
            print(f"Error: Account '{name}' not found.")
            return
        totp = pyotp.TOTP(self.accounts[name])
        print(f"Current TOTP for '{name}': {totp.now()}")

    def edit_account(self, name, new_name=None, new_secret=None):
        if name not in self.accounts:
            print(f"Error: Account '{name}' not found.")
            return

        if new_name:
            if new_name in self.accounts:
                print(f"Error: Account name '{new_name}' already exists.")
                return
            self.accounts[new_name] = self.accounts.pop(name)
            print(f"Account name changed to '{new_name}'.")

        if new_secret:
            self.accounts[name if new_name is None else new_name] = new_secret
            print(f"Account secret updated.")

        self.save_accounts()

    def delete_account(self, name):
        if name not in self.accounts:
            print(f"Error: Account '{name}' not found.")
            return
        del self.accounts[name]
        self.save_accounts()
        print(f"Account '{name}' deleted successfully.")

def main():
    manager = TOTPManager()

    parser = argparse.ArgumentParser(description="TOTP CLI Manager")
    subparsers = parser.add_subparsers(dest="command")

    # Add account
    add_parser = subparsers.add_parser("add", help="Add a new account")
    add_parser.add_argument("name", help="Account name")
    add_parser.add_argument("secret", help="Account base32 secret")

    # List accounts
    subparsers.add_parser("list", help="List all accounts")

    # Display TOTP
    totp_parser = subparsers.add_parser("totp", help="Display TOTP for an account")
    totp_parser.add_argument("name", help="Account name")

    # Edit account
    edit_parser = subparsers.add_parser("edit", help="Edit account name or secret")
    edit_parser.add_argument("name", help="Account name to edit")
    edit_parser.add_argument("--new-name", help="New name for the account")
    edit_parser.add_argument("--new-secret", help="New base32 secret for the account")

    # Delete account
    delete_parser = subparsers.add_parser("delete", help="Delete an account")
    delete_parser.add_argument("name", help="Account name to delete")

    # Parse arguments
    args = parser.parse_args()

    if args.command == "add":
        manager.add_account(args.name, args.secret)
    elif args.command == "list":
        manager.list_accounts()
    elif args.command == "totp":
        manager.display_totp(args.name)
    elif args.command == "edit":
        manager.edit_account(args.name, args.new_name, args.new_secret)
    elif args.command == "delete":
        manager.delete_account(args.name)
    else:
        print("Invalid command. Use 'add', 'list', 'totp', 'edit', or 'delete'.")

if __name__ == "__main__":
    main()
