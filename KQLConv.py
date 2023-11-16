import tkinter as tk

def convert_text():
    input_text = input_text_box.get("1.0", "end-1c")
    formatted_text = input_text.replace('\n', '\\r\\n').replace('"', '\\"')
    output_text_box.delete("1.0", "end")
    output_text_box.insert("1.0", formatted_text)

# Create the main window
root = tk.Tk()
root.title("Text Converter")

# Input Text Box
input_text_box = tk.Text(root, height=10, width=50, wrap=tk.WORD)
input_text_box.pack(padx=10, pady=10)

# Convert Button
convert_button = tk.Button(root, text="Convert", command=convert_text)
convert_button.pack(pady=5)

# Output Text Box
output_text_box = tk.Text(root, height=10, width=50, wrap=tk.WORD)
output_text_box.pack(padx=10, pady=10)

# Run the Tkinter event loop
root.mainloop()
