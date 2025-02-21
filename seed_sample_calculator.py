import tkinter as tk
import keyboard
import threading
import math

code_map = {
    "82-82-75-75-76-76": "-",
    "82-82-75-75-77-77": ".",
    "82-82-75-75-72-72": "0",
    "82-82-75-75-73-73": "1",
    "82-82-76-76-82-82": "2",
    "82-82-76-76-79-79": "3",
    "82-82-76-76-80-80": "4",
    "82-82-76-76-81-81": "5",
    "82-82-76-76-75-75": "6",
    "82-82-76-76-76-76": "7",
    "82-82-76-76-77-77": "8",
    "82-82-76-76-71-71": "9",
    "82-82-79-79-81-81": "",
    "82-82-79-79-82-82": "done",
}

scale_input = ""
cur = []
reading = False
def on_key_event(event):
    global scale_input, cur, reading

    if event.scan_code == 28:
        scale_input = ""
    elif event.scan_code == 56:
        if reading:
            new = code_map.get("-".join(cur))
            cur = []
            if new == "done":
                entry1.delete(0, tk.END)
                entry1.insert(0, scale_input)
                scale_input = ""
                get_sampling_steps()
            elif new is not None:
                scale_input = scale_input + new
        reading = not reading
    elif reading:
        cur.append(str(event.scan_code))

def on_enter():
    if window.focus_displayof():
        get_sampling_steps()

def start_listener():
    keyboard.hook(on_key_event)
    keyboard.wait()

def get_sampling_steps():
    output = ""
    try:
        original_weight = float(entry1.get())
        desired_weight = float(entry2.get())
        tolerance = float(entry3.get()) / 100
        margin = float(entry4.get()) / 100

        if desired_weight <= 0 or desired_weight * (1 + tolerance) >= original_weight or tolerance <= 0 or margin <= 0 or 0.5 <= margin:
            output = "Invalid input"
        else:
            desired_fraction = desired_weight / original_weight
            denominator = 1
            for i in range(25):
                denominator *= 2
                numerator = math.ceil(desired_fraction * denominator * (1 + tolerance * margin))
                if numerator < desired_fraction * denominator * (1 + tolerance * (1 - margin)):
                    while i > 0:
                        output = f" ({numerator:.0f}/{denominator:.0f} = {original_weight * numerator / denominator:.3f}g)\n{output}"
                        if numerator < denominator/2:
                            new = "L"
                        else:
                            new = "R"
                            numerator -= denominator/2
                        output = f"{i}: {new}{output}"
                        
                        denominator /= 2
                        i -= 1
                    break
    except ValueError:
        output = "Invalid input"
    result_label.config(text=output)

listener_thread = threading.Thread(target=start_listener, daemon=True)
listener_thread.start()
keyboard.add_hotkey("enter", lambda: on_enter())

window = tk.Tk()
window.title("Seed Sample Calculator")
font = ("Consolas", 15)

entry1 = tk.Entry(window, justify="left", font=font)
entry2 = tk.Entry(window, justify="left", font=font)
entry3 = tk.Entry(window, justify="left", font=font)
entry4 = tk.Entry(window, justify="left", font=font)
entry3.insert(0, "10")
entry4.insert(0, "10")
tk.Label(window, text="Original weight (g)", anchor="w", font=font).pack(fill="x")
entry1.pack()
tk.Label(window, text="Desired weight (g)", anchor="w", font=font).pack(fill="x")
entry2.pack()
tk.Label(window, text="Tolerance (%)", anchor="w", font=font).pack(fill="x")
entry3.pack()
tk.Label(window, text="Margin (%)", anchor="w", font=font).pack(fill="x")
entry4.pack()

calculate_button = tk.Button(window, text="Calculate (Enter)", command=get_sampling_steps, justify="left", font=font)
calculate_button.pack()

result_label = tk.Label(window, text="", anchor="w", justify="left", font=font)
result_label.pack(fill="x")

window.mainloop()
