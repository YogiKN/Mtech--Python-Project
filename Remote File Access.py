import docker
import tkinter as tk
from tkinter import filedialog, messagebox

# Initialize Docker client
client = docker.from_env()

# Function to list files in the container
def list_files(container_id):
    try:
        container = client.containers.get(container_id)
        files = container.exec_run('ls -l /').output.decode('utf-8')
        return files
    except Exception as e:
        return str(e)

# Function to delete selected file from the container
def delete_file(container_id, file_path):
    try:
        container = client.containers.get(container_id)
        container.exec_run(f'rm {file_path}')
        return True
    except Exception as e:
        return str(e)

# Function to handle file selection and deletion
def handle_delete():
    selected_file = listbox.get(tk.ACTIVE)
    if selected_file:
        confirmation = messagebox.askyesno("Confirmation", f"Are you sure you want to delete '{selected_file}'?")
        if confirmation:
            result = delete_file(container_id, selected_file)
            if result:
                listbox.delete(tk.ACTIVE)
                messagebox.showinfo("Success", f"File '{selected_file}' deleted successfully.")
            else:
                messagebox.showerror("Error", f"Failed to delete file '{selected_file}': {result}")
    else:
        messagebox.showwarning("Warning", "Please select a file to delete.")

# Function to refresh file list
def refresh_list():
    file_list = list_files(container_id)
    if file_list:
        listbox.delete(0, tk.END)
        for line in file_list.split('\n'):
            listbox.insert(tk.END, line)

# Function to handle container selection
def select_container():
    global container_id
    container_id = container_entry.get()
    refresh_list()

# GUI setup
root = tk.Tk()
root.title("Docker Container File Manager")

container_label = tk.Label(root, text="Container ID:")
container_label.grid(row=0, column=0, padx=5, pady=5)

container_entry = tk.Entry(root, width=50)
container_entry.grid(row=0, column=1, padx=5, pady=5)

select_button = tk.Button(root, text="Select Container", command=select_container)
select_button.grid(row=0, column=2, padx=5, pady=5)

listbox = tk.Listbox(root, width=100, height=20)
listbox.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

refresh_button = tk.Button(root, text="Refresh List", command=refresh_list)
refresh_button.grid(row=2, column=0, padx=5, pady=5)

delete_button = tk.Button(root, text="Delete Selected File", command=handle_delete)
delete_button.grid(row=2, column=1, padx=5, pady=5)

quit_button = tk.Button(root, text="Quit", command=root.quit)
quit_button.grid(row=2, column=2, padx=5, pady=5)

root.mainloop()

