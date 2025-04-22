# Tools created by AIs

TOTP Generator generates one-time passwords (OTPs) based on a secret key and the current time, ensuring each code is unique and time-sensitive. There are two version, GUI and CLI.


What’s Included:


Add, List, Edit, Delete, and Display TOTP for accounts.

Accounts are saved in totp_data.json (just like the GUI version).

Supports both name and secret editing.



Prerequisites:

pip install pyotp

CLI Syntax:

1. Add Account:
python totp_cli_tool.py add <account_name> <secret>

3. List Accounts:
python totp_cli_tool.py list

4. Display TOTP for an Account:
python totp_cli_tool.py totp <account_name>

5. Edit Account (Change Name or Secret):
python totp_cli_tool.py edit <account_name> --new-name <new_name>
python totp_cli_tool.py edit <account_name> --new-secret <new_secret>

6. Delete Account:
python totp_cli_tool.py delete <account_name>

