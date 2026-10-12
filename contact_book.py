"""Contact Book - a simple command-line contact manager.

Contacts are stored in a JSON file (contacts.json) next to this script.
"""

import json
import re
from pathlib import Path

DATA_FILE = Path(__file__).with_name("contacts.json")
EMAIL_PATTERN = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


def normalize_phone(value):
    return re.sub(r"[\s\-()]", "", str(value)).strip()


# ---------- Validation ----------

def validate_name(value):
    value = " ".join(value.split())  # collapse extra spaces
    if not value:
        raise ValueError("name cannot be empty.")
    if len(value) > 50:
        raise ValueError("name must be 50 characters or fewer.")
    if not any(ch.isalpha() for ch in value):
        raise ValueError("name must contain at least one letter.")
    if not all(ch.isalpha() or ch in " .'-" for ch in value):
        raise ValueError("name can only contain letters, spaces, . ' and -")
    return value


def validate_phone(value):
    cleaned = normalize_phone(value)
    if not re.fullmatch(r"\+?\d{10,15}", cleaned):
        raise ValueError("phone must have 10-15 digits (optional leading +).")
    return cleaned


def validate_email(value):
    value = value.strip()
    if value and not EMAIL_PATTERN.match(value):
        raise ValueError("email must look like name@example.com.")
    return value


def ask(prompt, validator, default=None):
    """Keep asking until the input is valid.

    If default is given, pressing Enter returns the default.
    """
    while True:
        raw = input(prompt).strip()
        if raw == "" and default is not None:
            return default
        try:
            return validator(raw)
        except ValueError as err:
            print(f"  Invalid input: {err}")


# ---------- File handling ----------

def load_contacts():
    """Load contacts from disk. Returns an empty dict if nothing usable."""
    if not DATA_FILE.exists():
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError("unexpected file format")
    except (json.JSONDecodeError, ValueError):
        backup = DATA_FILE.with_suffix(".json.bak")
        try:
            DATA_FILE.replace(backup)
            print(f"Warning: contacts file was corrupted. Saved a copy as {backup.name}.")
        except OSError:
            print("Warning: contacts file was corrupted and could not be backed up.")
        return {}
    except OSError as err:
        print(f"Error: could not read contacts file ({err}).")
        return {}

    normalized = {}
    for raw_key, contact in data.items():
        if not isinstance(contact, dict):
            continue
        name = str(contact.get("name", "")).strip()
        phone = normalize_phone(contact.get("phone", ""))
        email = str(contact.get("email", "")).strip()
        if not name or not phone:
            continue
        key = " ".join(name.lower().split())
        normalized[key] = {"name": name, "phone": phone, "email": email}
    return normalized


def save_contacts(contacts):
    """Save contacts to disk. Returns True on success."""
    temp_file = DATA_FILE.with_suffix(".json.tmp")
    try:
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(contacts, f, indent=2, ensure_ascii=False)
        temp_file.replace(DATA_FILE)
        return True
    except OSError as err:
        print(f"Error: could not save contacts ({err}).")
        return False


# ---------- Features ----------

def show_contact(contact):
    email = contact.get("email", "") or "-"
    print(f"  {contact['name']:<20} {contact['phone']:<16} {email}")


def add_contact(contacts):
    name = ask("Name: ", validate_name)
    key = name.lower()
    if key in contacts:
        print(f"'{contacts[key]['name']}' already exists. Use Update instead.")
        return
    phone = ask("Phone: ", validate_phone)
    email = ask("Email (optional, press Enter to skip): ", validate_email, default="")
    contacts[key] = {"name": name, "phone": phone, "email": email}
    if save_contacts(contacts):
        print(f"Added {name}.")


def view_contacts(contacts):
    if not contacts:
        print("No contacts yet.")
        return
    print(f"\n  {'NAME':<20} {'PHONE':<16} EMAIL")
    print("  " + "-" * 50)
    for key in sorted(contacts):
        show_contact(contacts[key])
    print(f"\nTotal: {len(contacts)}")


def search_contacts(contacts):
    term = input("Search (name or phone): ").strip().lower()
    if not term:
        print("Search term cannot be empty.")
        return
    normalized_term = normalize_phone(term)
    matches = []
    for contact in contacts.values():
        name = str(contact.get("name", "")).lower()
        phone = normalize_phone(contact.get("phone", ""))
        if term in name or normalized_term in normalize_phone(phone):
            matches.append(contact)
    if not matches:
        print("No matching contacts.")
        return
    print(f"\nFound {len(matches)}:")
    for contact in sorted(matches, key=lambda c: c["name"].lower()):
        show_contact(contact)


def update_contact(contacts):
    name = input("Name of contact to update: ").strip().lower()
    name = " ".join(name.split())
    if name not in contacts:
        print("Contact not found.")
        return
    current = contacts[name]
    print("Press Enter to keep the current value.")
    phone = ask(f"Phone [{current['phone']}]: ", validate_phone, default=current["phone"])
    email = ask(f"Email [{current.get('email', '') or '-'}]: ", validate_email, default=current.get("email", ""))
    current["phone"] = phone
    current["email"] = email
    if save_contacts(contacts):
        print(f"Updated {current['name']}.")


def delete_contact(contacts):
    name = input("Name of contact to delete: ").strip().lower()
    name = " ".join(name.split())
    if name not in contacts:
        print("Contact not found.")
        return
    display = contacts[name]["name"]
    confirm = input(f"Delete {display}? (y/n): ").strip().lower()
    if confirm != "y":
        print("Cancelled.")
        return
    removed = contacts.pop(name)
    if save_contacts(contacts):
        print(f"Deleted {display}.")
    else:
        contacts[name] = removed  # keep memory consistent with disk


MENU = """
===== Contact Book =====
1. Add contact
2. View all contacts
3. Search contacts
4. Update contact
5. Delete contact
6. Exit
"""

ACTIONS = {
    "1": add_contact,
    "2": view_contacts,
    "3": search_contacts,
    "4": update_contact,
    "5": delete_contact,
}


def main():
    contacts = load_contacts()
    while True:
        print(MENU)
        try:
            choice = input("Choose an option (1-6): ").strip()
            if choice == "6":
                print("Goodbye!")
                break
            action = ACTIONS.get(choice)
            if action is None:
                print("Please enter a number from 1 to 6.")
                continue
            action(contacts)
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()