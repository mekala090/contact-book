# Contact Book

A simple command-line contact manager written in Python. Contacts are saved
to a local `contacts.json` file, so they are still there the next time you run it.

## Features

- Add, view, search, update and delete contacts
- Input validation for names, phone numbers and emails
- Duplicate-name protection
- Safe handling of missing or corrupted data files
- Confirmation before deleting

## Requirements

- Python 3.8 or newer (no external packages needed)

## How to run

    python contact_book.py

## Validation rules

- Name: required, up to 50 characters, letters / spaces / . ' - only
- Phone: required, 10-15 digits, optional leading + (spaces and dashes are ignored)
- Email: optional, must look like name@example.com

## Project structure

- contact_book.py - the program
- contacts.json - created automatically when you add a contact
- README.md
