# main.py
from turtle import color

import customtkinter as ctk
import threading
import pyttsx3
from brain import understand_command
from executor import execute_action

# ── Theme ──────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ── Voice Engine ───────────────────────────────────────────
engine = pyttsx3.init()
engine.setProperty('rate', 175)

def speak(text):
    """JARVIS speaks the response"""
    threading.Thread(
        target=lambda: (engine.say(text), engine.runAndWait()),
        daemon=True
    ).start()

# ── Main App ───────────────────────────────────────────────
class JarvisApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("⚡ JARVIS — Personal Assistant")
        self.geometry("600x700")
        self.resizable(False, False)
        
        # Keep window on top at startup
        self.attributes("-topmost", True)
        self.after(3000, lambda: self.attributes("-topmost", False))

        self.build_ui()
        self.after(500, self.welcome)

    def build_ui(self):
        # ── Header ─────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color="#1a1a2e", corner_radius=0, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header, text="⚡ J.A.R.V.I.S",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#00d4ff"
        ).pack(side="left", padx=20, pady=20)

        self.status_dot = ctk.CTkLabel(
            header, text="● ONLINE",
            font=ctk.CTkFont(size=12),
            text_color="#00ff88"
        )
        self.status_dot.pack(side="right", padx=20)

        # ── Chat Window ────────────────────────────────────
        self.chat_box = ctk.CTkTextbox(
            self, width=560, height=420,
            font=ctk.CTkFont(size=13),
            fg_color="#0d0d1a",
            text_color="#e0e0e0",
            corner_radius=10
        )
        self.chat_box.pack(padx=20, pady=(15, 10))
        self.chat_box.configure(state="disabled")

        # ── Input Area ─────────────────────────────────────
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.input_box = ctk.CTkEntry(
            input_frame,
            placeholder_text="Give me a command... (e.g. 'open VS Code')",
            height=45,
            font=ctk.CTkFont(size=13),
            corner_radius=10
        )
        self.input_box.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.input_box.bind("<Return>", lambda e: self.send_command())

        send_btn = ctk.CTkButton(
            input_frame, text="Send ➤",
            width=90, height=45,
            command=self.send_command,
            fg_color="#0078d4",
            hover_color="#005a9e",
            corner_radius=10
        )
        send_btn.pack(side="right")

        # ── Quick Command Buttons ──────────────────────────
        quick_frame = ctk.CTkFrame(self, fg_color="#111122", corner_radius=10)
        quick_frame.pack(fill="x", padx=20, pady=(0, 15))

        ctk.CTkLabel(
            quick_frame, text="Quick Commands:",
            font=ctk.CTkFont(size=11),
            text_color="#888"
        ).pack(anchor="w", padx=10, pady=(8, 4))

        buttons_row = ctk.CTkFrame(quick_frame, fg_color="transparent")
        buttons_row.pack(fill="x", padx=10, pady=(0, 10))

        quick_cmds = [
            ("💻 VS Code", "open vs code"),
            ("🎵 Lo-fi Music", "play lo-fi music on youtube in brave"),
            ("📁 Downloads", "open downloads folder"),
            ("🎙️ Podcasts", "open best podcast on youtube"),
        ]

        for label, cmd in quick_cmds:
            ctk.CTkButton(
                buttons_row, text=label,
                width=120, height=32,
                font=ctk.CTkFont(size=11),
                fg_color="#1e1e3a",
                hover_color="#2a2a50",
                command=lambda c=cmd: self.run_quick(c)
            ).pack(side="left", padx=4)

    def add_message(self, sender, text, color):
        self.chat_box.configure(state="normal")
        self.chat_box.insert("end", f"{sender}\n", "sender")
        self.chat_box.insert("end", f"{text}\n\n")
        self.chat_box.tag_config("sender", foreground=color)
        self.chat_box.configure(state="disabled")
        self.chat_box.see("end")

    def welcome(self):
        msg = "Hello! I'm JARVIS, your personal assistant.\nWhat would you like me to help with today?"
        self.add_message("🤖 JARVIS", msg, "#00d4ff")
        speak("Hello! I am JARVIS. What would you like me to help with today?")

    def send_command(self):
        user_input = self.input_box.get().strip()
        if not user_input:
            return
        self.input_box.delete(0, "end")
        self.add_message("👤 You", user_input, "#ffd700")

        # Disable input while processing
        self.status_dot.configure(text="● THINKING...", text_color="#ffaa00")
        threading.Thread(target=self.process, args=(user_input,), daemon=True).start()

    def run_quick(self, command):
        self.input_box.delete(0, "end")
        self.input_box.insert(0, command)
        self.send_command()

    def process(self, user_input):
        action_data = understand_command(user_input)
        result = execute_action(action_data)
        
        # Update UI from main thread
        self.after(0, lambda: self.show_result(result))

    def show_result(self, result):
        self.add_message("🤖 JARVIS", result, "#00d4ff")
        self.status_dot.configure(text="● ONLINE", text_color="#00ff88")
        speak(result)


if __name__ == "__main__":
    app = JarvisApp()
    app.mainloop()