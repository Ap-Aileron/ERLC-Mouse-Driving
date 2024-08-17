import tkinter as tk
from tkinter import ttk

def create_ui(update_settings, toggle_script, stop_script_function, middle_range, sensitivity, sensitivity_multiplier, full_press_sensitivity, hold_down_range, start_key, stop_key):
    # Create and configure the main window
    root = tk.Tk()
    root.title("Mouse Steering Script Settings")
    root.geometry("500x700")
    root.resizable(True, True)

    # Dark mode colors
    background_color = "#1e1e2e"
    foreground_color = "#ffffff"
    button_color = "#0e7fe0"
    entry_background_color = "#2e2e3e"
    entry_foreground_color = "#ffffff"

    # Apply dark mode
    root.configure(bg=background_color)

    # Create a canvas and a scrollbar
    canvas = tk.Canvas(root, bg=background_color)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=background_color)

    # Configure canvas
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    scrollable_frame.bind("<Configure>", on_frame_configure)

    # Style configurations
    style = ttk.Style()
    style.configure("TButton", font=('Helvetica', 14), padding=10, relief="flat", background=button_color, foreground=foreground_color)
    style.configure("TLabel", font=('Helvetica', 14), background=background_color, foreground=foreground_color)

    def rounded_button(master, text, command):
        return tk.Button(master, text=text, command=command, bg=button_color, fg=foreground_color, 
                         font=('Helvetica', 14), relief="flat", bd=0, highlightthickness=0, padx=10, pady=10, 
                         activebackground="#146eb4", activeforeground="#ffffff", overrelief="raised")

    def rounded_entry(master, textvariable=None):
        entry = tk.Entry(master, bg=entry_background_color, fg=entry_foreground_color, 
                         font=('Helvetica', 14), relief="flat", bd=0, highlightthickness=0)
        if textvariable:
            entry.config(textvariable=textvariable)
        entry.config(insertbackground="#ffffff")
        return entry

    # Center the content using grid layout and add space on the left
    scrollable_frame.grid_rowconfigure(0, weight=1)
    scrollable_frame.grid_rowconfigure(7, weight=1)
    scrollable_frame.grid_columnconfigure(0, weight=1)
    scrollable_frame.grid_columnconfigure(1, weight=1)

    # Create and place widgets with padding for left space
    tk.Label(scrollable_frame, text="Middle Range (pixels):", bg=background_color, fg=foreground_color).grid(row=0, column=0, sticky='w', pady=5, padx=(30, 5))
    entry_middle_range = rounded_entry(scrollable_frame)
    entry_middle_range.insert(0, "%.2f" % middle_range)
    entry_middle_range.grid(row=0, column=1, pady=5, sticky='ew')

    tk.Label(scrollable_frame, text="Sensitivity (seconds):", bg=background_color, fg=foreground_color).grid(row=1, column=0, sticky='w', pady=5, padx=(30, 5))
    entry_sensitivity = rounded_entry(scrollable_frame)
    entry_sensitivity.insert(0, "%.2f" % sensitivity)
    entry_sensitivity.grid(row=1, column=1, pady=5, sticky='ew')

    tk.Label(scrollable_frame, text="Sensitivity Multiplier:", bg=background_color, fg=foreground_color).grid(row=2, column=0, sticky='w', pady=5, padx=(30, 5))
    entry_sensitivity_multiplier = rounded_entry(scrollable_frame)
    entry_sensitivity_multiplier.insert(0, "%.2f" % sensitivity_multiplier)
    entry_sensitivity_multiplier.grid(row=2, column=1, pady=5, sticky='ew')

    tk.Label(scrollable_frame, text="Full Press Sensitivity (seconds):", bg=background_color, fg=foreground_color).grid(row=3, column=0, sticky='w', pady=5, padx=(30, 5))
    entry_full_press_sensitivity = rounded_entry(scrollable_frame)
    entry_full_press_sensitivity.insert(0, "%.2f" % full_press_sensitivity)
    entry_full_press_sensitivity.grid(row=3, column=1, pady=5, sticky='ew')

    tk.Label(scrollable_frame, text="Hold Down Range (pixels):", bg=background_color, fg=foreground_color).grid(row=4, column=0, sticky='w', pady=5, padx=(30, 5))
    entry_hold_down_range = rounded_entry(scrollable_frame)
    entry_hold_down_range.insert(0, "%.2f" % hold_down_range)
    entry_hold_down_range.grid(row=4, column=1, pady=5, sticky='ew')

    tk.Label(scrollable_frame, text="Start Keybind:", bg=background_color, fg=foreground_color).grid(row=5, column=0, sticky='w', pady=5, padx=(30, 5))
    entry_start_key = rounded_entry(scrollable_frame)
    entry_start_key.insert(0, start_key)
    entry_start_key.grid(row=5, column=1, pady=5, sticky='ew')

    tk.Label(scrollable_frame, text="Stop Keybind:", bg=background_color, fg=foreground_color).grid(row=6, column=0, sticky='w', pady=5, padx=(30, 5))
    entry_stop_key = rounded_entry(scrollable_frame)
    entry_stop_key.insert(0, stop_key)
    entry_stop_key.grid(row=6, column=1, pady=5, sticky='ew')

    # Update settings and control buttons
    update_button = rounded_button(scrollable_frame, text="Update Settings", command=lambda: update_settings(
        entry_middle_range, entry_sensitivity, entry_sensitivity_multiplier, entry_full_press_sensitivity, entry_hold_down_range,
        entry_start_key, entry_stop_key
    ))
    update_button.grid(row=7, column=0, columnspan=2, pady=10)

    start_button = rounded_button(scrollable_frame, text="Start Script", command=toggle_script)
    start_button.grid(row=8, column=0, columnspan=2, pady=10)

    stop_button = rounded_button(scrollable_frame, text="Stop Script", command=stop_script_function)
    stop_button.grid(row=9, column=0, columnspan=2, pady=10)

    return root, start_button
