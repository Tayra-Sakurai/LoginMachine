import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from csv import writer,reader
from tkinter.filedialog import askopenfilename, asksaveasfilename
from selenium.webdriver.support.ui import WebDriverWait
from tkinter.messagebox import showinfo, showerror, askyesno
from tkinter import Tk, StringVar
from tkinter.ttk import Entry, Button, Label, Frame, Combobox

# Function to login to a website using Selenium
def login (
    url:str,
    username: str,
    usernamefield: str,
    usernamefieldIdType: By,
    password: str,
    passwordfield: str,
    passwordfieldtype: By
    )-> webdriver:
    '''Function to login to a website using Selenium.
    Args:
        url (str): The URL of the website to login to.
        username (str): The username to login with.
        usernamefield (str): The name or ID of the username field.
        usernamefieldIdType (By): The type of identifier for the username field (e.g., By.ID, By.NAME).
        password (str): The password to login with.
        passwordfield (str): The name or ID of the password field.
        passwordfieldtype (By): The type of identifier for the password field.
    '''
    # Launch Microsoft Edge browser
    driver = webdriver.Edge()
    # Navigate to the specified URL
    driver.get(url)
    # Wait for the page to load
    WebDriverWait(
        driver,
        10).until(lambda d: d.find_element(usernamefieldIdType, usernamefield))
    # Find the username field and enter the username
    driver.find_element(usernamefieldIdType, usernamefield).send_keys(username)
    # Find the password field and enter the password
    driver.find_element(passwordfieldtype, passwordfield).send_keys(password)
    # Wait for the keys to be sent
    WebDriverWait(driver, 10).until(lambda d: d.find_element(
        passwordfieldtype, passwordfield).get_attribute('value') == password)
    # Submit the form
    driver.find_element(passwordfieldtype,
                        passwordfield).send_keys(Keys.RETURN)
    # Wait for the page to load after login
    WebDriverWait(driver, 10).until(lambda d: d.title != "")
    # Return the driver instance
    return driver

# Function to save login credentials to a CSV file
def save_credentials(
    url: str,
    username: str,
    usernamefield: str,
    usernamefieldIdType: By,
    password: str,
    passwordfield: str,
    passwordfieldtype: By
    )-> None:
    '''Function to save login credentials to a CSV file.
    Args:
        url (str): The URL of the website.
        username (str): The username.
        usernamefield (str): The name or ID of the username field.
        usernamefieldIdType (By): The type of identifier for the username field.
        password (str): The password.
        passwordfield (str): The name or ID of the password field.
        passwordfieldtype (By): The type of identifier for the password field.
    '''
    # Open a file dialog to save the credentials
    filename = asksaveasfilename(title="Save Credentials",
                                 defaultextension=".csv",
                                 filetypes=[("CSV files", "*.csv"),
                                            ("All files", "*.*")])
    if not filename:
        showerror("Error", "No file selected.")
        return
    # Write the credentials to the CSV file
    with open(filename, 'w', newline='') as file:
        csv_writer = writer(file)
        csv_writer.writerow([
            'URL', 'Username', 'Username Field', 'Username Field Type',
            'Password', 'Password Field', 'Password Field Type'
        ])
        csv_writer.writerow([
            url, username, usernamefield, usernamefieldIdType, password,
            passwordfield, passwordfieldtype
        ])
        showinfo("Success", "Credentials saved successfully.")
    return

# Function to get login credentials from user input via a GUI
def get_credentials() -> tuple:
    '''Function to get login credentials from user input via a GUI.
    Returns:
        tuple: A tuple containing the URL, username, username field, username field type,
               password, password field, and password field type.
    '''
    root = Tk()
    root.title("Login Credentials")
    # Create input fields
    url_var = StringVar()
    username_var = StringVar()
    username_field_var = StringVar()
    password_var = StringVar()
    password_field_var = StringVar()
    Label(root, text="URL:").grid(row=0, column=0)
    Entry(root, textvariable=url_var).grid(row=0, column=1)
    Label(root, text="Username:").grid(row=1, column=0)
    Entry(root, textvariable=username_var).grid(row=1, column=1)
    Label(root, text="Username Field:").grid(row=2, column=0)
    Entry(root, textvariable=username_field_var).grid(row=2, column=1)
    Label(root, text="Password:").grid(row=3, column=0)
    Entry(root, textvariable=password_var, show='*').grid(row=3, column=1)
    Label(root, text="Password Field:").grid(row=4, column=0)
    Entry(root, textvariable=password_field_var).grid(row=4, column=1)
    # Dropdown for field types
    field_types = [By.ID, By.NAME, By.CLASS_NAME, By.XPATH, By.CSS_SELECTOR]
    username_field_type_var = StringVar(value=field_types[0])
    password_field_type_var = StringVar(value=field_types[0])
    Label(root, text="Username Field Type:").grid(row=5, column=0)
    Combobox(
        root,
        textvariable=username_field_type_var,
        values=[By.ID, By.NAME, By.CLASS_NAME, By.XPATH, By.CSS_SELECTOR]
    ).grid(row=5, column=1)
    Label(root, text="Password Field Type:").grid(row=6, column=0)
    Combobox(root,
             textvariable=password_field_type_var,
             values=[By.ID, By.NAME, By.CLASS_NAME, By.XPATH,
                     By.CSS_SELECTOR]).grid(row=6, column=1)
    def submit():
        root.quit()
    Button(root, text="Submit", command=submit).grid(row=7, columnspan=2)

    root.mainloop()
    return (
        url_var.get(), username_var.get(), username_field_var.get(),
     username_field_type_var.get(), password_var.get(),
     password_field_var.get(), password_field_type_var.get())

# Function to read login credentials from a CSV file
def read_credentials(filename: str) -> list:
    '''Function to read login credentials from a CSV file.
    Args:
        filename (str): The path to the CSV file containing login credentials.
    Returns:
        list: A list of dictionaries containing the login credentials.
    '''
    credentials = []
    try:
        with open(filename, 'r', newline='') as file:
            csv_reader = reader(file)
            headers = next(csv_reader)
            for row in csv_reader:
                credentials.append(dict(zip(headers, row)))
    except FileNotFoundError:
        showerror("Error", "File not found.")
    except Exception as e:
        showerror("Error", f"An error occurred: {e}")
    return credentials

# Function to load credentials from a CSV file
def load_credentials() -> list:
    '''Function to load credentials from a CSV file.
    Returns:
        list: A list of dictionaries containing the login credentials.
    '''
    filename = askopenfilename(title="Open Credentials File",
                               defaultextension=".csv",
                               filetypes=[("CSV files", "*.csv"),
                                          ("All files", "*.*")])
    if not filename:
        showerror("Error", "No file selected.")
        return []
    return read_credentials(filename)

# Function to execute the login process
def execute_login ():
    '''Function to execute the login process or save credentials.
    '''
    # Ask user if they want to save credentials
    if askyesno("Save Credentials", "Do you want to save the credentials?"):
        url, username, usernamefield, usernamefieldIdType, password, passwordfield, passwordfieldtype = get_credentials(
        )
        save_credentials(url, username, usernamefield, usernamefieldIdType,
                         password, passwordfield, passwordfieldtype)
    else:
        credentials = load_credentials()
        if not credentials:
            return
        for cred in credentials:
            login(cred['URL'], cred['Username'], cred['Username Field'],
                  cred['Username Field Type'], cred['Password'],
                  cred['Password Field'],
                  cred['Password Field Type'])

# Main function to run the script
def main():
    '''Main function to run the script.
    '''
    execute_login()

main()