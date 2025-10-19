import tkinter as tk
from tkinter import scrolledtext
import requests

API_KEY = "YOUR_GEMINI_API_KEY"

# === Keep conversation history ===
conversation_history = []

def get_gemini_response(user_input):
    conversation_history.append({"role": "user", "content": [{"text": user_input}]})

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": API_KEY
    }
    data = {
        "conversation": conversation_history  # pass entire conversation
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        # Parse Gemini response
        candidates = result.get("candidates", [])
        if not candidates:
            return "JetBot: Sorry, no response received."

        content = candidates[0].get("content", [])
        if not content:
            return "JetBot: Sorry, empty content."

        text = content[0].get("text", "")
        if not text:
            return "JetBot: Sorry, empty text response."

        # Add Gemini's reply to conversation history
        conversation_history.append({"role": "assistant", "content": [{"text": text}]})

        return text.strip()

    except Exception as e:
        return f"Error: {e}"

# === GUI (Tkinter) same as before ===
root = tk.Tk()
root.title("JetBot Chat (Gemini AI)")
root.geometry("600x500")

chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD)
chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_window.config(state='disabled')

entry = tk.Entry(root, width=80)
entry.pack(side=tk.LEFT, padx=(10,0), pady=(0,10), fill=tk.X, expand=True)
entry.bind("<Return>", lambda event: send_message())

send_button = tk.Button(root, text="Send", command=send_message) # pyright: ignore[reportUndefinedVariable]
send_button.pack(side=tk.RIGHT, padx=(0,10), pady=(0,10))

def send_message():
    user_input = entry.get()
    if not user_input.strip():
        return
    chat_window.config(state='normal')
    chat_window.insert(tk.END, "You: " + user_input + "\n")
    chat_window.config(state='disabled')
    entry.delete(0, tk.END)

    bot_response = get_gemini_response(user_input)
    chat_window.config(state='normal')
    chat_window.insert(tk.END, "JetBot: " + bot_response + "\n\n")
    chat_window.config(state='disabled')
    chat_window.yview(tk.END)

send_button = tk.Button(root, text="Send", command=send_message) # type: ignore
send_button.pack(side=tk.RIGHT, padx=(0,10), pady=(0,10))

root.mainloop()
