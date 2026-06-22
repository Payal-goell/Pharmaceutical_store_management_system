# Pharmacy Management System

This project provides two versions of a pharmacy management system for managing customer records and pharmacy operations.

## Versions Available

### 1. **Command-Line Interface (CLI)** - `project source file.py`
- Text-based menu system
- Terminal-based interaction
- All original functionality intact

**To run:**
```bash
python "project source file.py"
```

### 2. **Graphical User Interface (GUI)** - `pharmacy_gui.py` (Recommended)
- User-friendly desktop application
- Windows-based forms and dialogs
- Easy navigation with buttons and input fields
- Professional appearance with data tables

**To run:**
```bash
python pharmacy_gui.py
```

## Requirements

Make sure you have the required packages installed:

```bash
pip install mysql-connector-python tabulate
```

## Database Setup

The system will automatically:
- Create the database if it doesn't exist
- Create the customer table with the required schema
- Connect using the configured credentials

**Current Configuration:**
- Host: localhost
- User: root
- Password: dstvtush04

(Update these in the code if your MySQL credentials are different)

## Features

1. **Add Customer Record** - Enter new customer information
2. **Display All Records** - View all customers in a table format
3. **Display Particular Record** - Search and view a specific customer
4. **Delete All Records** - Clear all customer data (with confirmation)
5. **Delete Particular Record** - Remove a specific customer
6. **Modify Record** - Update customer information (medicine, balance, purchase date)
7. **Exit** - Close the application

## Customer Record Fields

- **Customer ID** - Unique identifier (Primary Key)
- **Name** - Customer full name
- **Disease** - Medical condition
- **Medicine** - Prescribed medicine
- **Balance** - Account balance
- **Last Purchase Date** - Date in DD/MM/YYYY format

## Recommendation

Use **pharmacy_gui.py** for a better user experience with its intuitive graphical interface!
