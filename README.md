MikroTik User Manager Migration Script

This Python script allows you to migrate users from one MikroTik RouterOS device (version 6) to another (version 7). It uses the RouterOS API to retrieve user data from a source RouterOS device and creates new users on a target RouterOS device. This script is ideal for those who need to transfer user data between two MikroTik routers running different versions of RouterOS.
Features:

    Imports users from RouterOS v6: Retrieves user data from a MikroTik RouterOS device running version 6.
    Exports user data to CSV: Saves user data to a CSV file for backup or further processing.
    Creates users on RouterOS v7: Adds users to a MikroTik RouterOS device running version 7 using the new API structure.
    Email handling: Users' email addresses (if available) are stored as comments for easy reference.

Requirements:

    Python 3.6 or later.
    routeros-api Python package.

Installation:

    Install dependencies:

pip install routeros-api

Clone the repository (or download the script):

git clone https://github.com/yourusername/mikrotik-user-migration.git

Configure your RouterOS devices:

    Update the IP addresses, usernames, and passwords for your source and target routers in the script.

Run the script:

    python3 user.py

Usage:

    The script will connect to the source RouterOS v6 device, import all user data, and then connect to the target RouterOS v7 device to create the users.
    If email addresses are provided, they will be included in the comment field of each user in the target device.

Example CSV output:

The script will also export the user data to a CSV file named exported_users.csv by default. The CSV will contain the following columns:

    Username: The username of the user.
    Password: The password of the user.
    Email: The email address (if provided), otherwise "brak".

License:

This project is licensed under the MIT License.
