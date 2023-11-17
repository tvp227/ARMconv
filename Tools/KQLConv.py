import tkinter as tk

def convert_text():
# Converts text from input_text_box to a formatted version and displays it in output_text_box.
    input_text = input_text_box.get("1.0", "end-1c")
    formatted_text = input_text.replace('\n', '\\r\\n').replace('"', '\\"')
    output_text_box.delete("1.0", "end")
    output_text_box.insert("1.0", formatted_text)

def reverse_text():
# Reverses the changes made by convert_text and displays the original text in input_text_box.
    formatted_text = output_text_box.get("1.0", "end-1c")
    original_text = formatted_text.replace('\\r\\n', '\n').replace('\\"', '"')
    input_text_box.delete("1.0", "end")
    input_text_box.insert("1.0", original_text)

# Create the main window
root = tk.Tk()
root.title("Text Converter")

# Input Text Box
input_label = tk.Label(root, text="Input Text:")
input_label.pack()

input_text_box = tk.Text(root, height=10, width=50, wrap=tk.WORD)
input_text_box.pack(padx=10, pady=5)

# Convert Button
convert_button = tk.Button(root, text="Convert", command=convert_text)
convert_button.pack(pady=5)

# Output Text Box
output_label = tk.Label(root, text="Formatted Text:")
output_label.pack()

output_text_box = tk.Text(root, height=10, width=50, wrap=tk.WORD)
output_text_box.pack(padx=10, pady=5)

# Reverse Button
reverse_button = tk.Button(root, text="Reverse", command=reverse_text)
reverse_button.pack(pady=5)

# Make the window resizable
root.resizable(width=True, height=True)

# Run the Tkinter event loop
root.mainloop()
