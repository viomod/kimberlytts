import os
import tkinter as tk
from tkinter import messagebox, ttk
import requests
import sounddevice as sd
import numpy as np
from pydub import AudioSegment

def get_audio_devices():
    return [device['name'] for device in sd.query_devices() if device['max_output_channels'] > 0]

def play_mp3_through_device(mp3_path, device_name):
    device_list = sd.query_devices()
    device_index = next((i for i, d in enumerate(device_list) if d['name'] == device_name), None)

    if device_index is None:
        messagebox.showerror("Error", f"Device '{device_name}' not found.")
        return

    audio = AudioSegment.from_mp3(mp3_path).set_channels(2).set_frame_rate(44100)
    samples = np.array(audio.get_array_of_samples()).astype(np.float32) / (2 ** 15)

    if audio.channels == 2:
        samples = samples.reshape((-1, 2))
    else:
        samples = np.stack([samples, samples], axis=1)

    sd.play(samples, samplerate=audio.frame_rate, device=device_index)
    sd.wait()

def on_button_click():
    text = entry.get().strip()
    if not text:
        messagebox.showwarning("Input Required", "Please enter some text.")
        return

    data = {
        "msg": text,
        "lang": "Kimberly",
        "source": "ttsmp3"
    }

    try:
        response = requests.post("https://ttsmp3.com/makemp3_new.php", data=data)
        json_data = response.json()
        if "URL" in json_data:
            mp3_url = json_data["URL"]
            selected_device = output_device.get()

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                mp3_data = requests.get(mp3_url).content
                temp_file.write(mp3_data)
                mp3_path = temp_file.name

            entry.delete(0, tk.END)

            play_mp3_through_device(mp3_path, selected_device)
        else:
            messagebox.showerror("TTS Error", f"Failed to get audio URL.\n\nResponse:\n{json_data}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

icon_url = "https://files.catbox.moe/3ry4b2.ico"
icon_path = os.path.join(tempfile.gettempdir(), "custom_icon.ico")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

try:
    r = requests.get(icon_url, headers=headers)
    r.raise_for_status()
    with open(icon_path, 'wb') as f:
        f.write(r.content)
except Exception as e:
    messagebox.showerror("Icon Download Error", f"Failed to download icon: {str(e)}")
    icon_path = None

root = tk.Tk()

if icon_path:
    root.iconbitmap(icon_path)
root.title("Kimberly TTS")
root.configure(bg="black")
root.geometry("800x300")

entry_frame = tk.Frame(root, bg="black")
entry = tk.Entry(entry_frame, bg="black", fg="white", insertbackground="white",
                 relief="flat", highlightthickness=0, borderwidth=0, font=("Arial", 16))
entry.pack(side="top", fill="x", padx=20)

underline = tk.Frame(entry_frame, height=2, bg="white")
underline.pack(side="top", fill="x", padx=20)

entry_frame.pack(pady=40, padx=40, fill="x")

device_label = tk.Label(root, text="Select Output Device:", fg="white", bg="black", font=("Arial", 12))
device_label.pack()

devices = get_audio_devices()
output_device = ttk.Combobox(root, values=devices, width=60)
output_device.pack(pady=10)
default_index = next((i for i, name in enumerate(devices) if 'vb-audio' in name.lower()), 0)
if devices:
    output_device.current(default_index)

button = tk.Button(root, text="Speak (or click enter)", command=on_button_click,
                   bg="black", fg="white", font=("Arial", 14),
                   activebackground="white", activeforeground="black")
button.pack(pady=30)

entry.bind("<Return>", lambda event: on_button_click())

root.mainloop()
