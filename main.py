import tkinter as tk


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window
        self.title("Zofia Calculator")
        self.geometry("320x420")
        self.resizable(False, False)
        self.configure(bg="#2c2f33")

        # Icon
        self.iconbitmap("zc.ico")
        self.icon = tk.PhotoImage(file="zc.png")
        self.iconphoto(False, self.icon)

        # State
        self.expression = ""

        # Display
        display_card = tk.Frame(
            self,
            bg="#23272a",
            height=90
        )
        display_card.pack(fill="x", padx=15, pady=(15,10))
        display_card.pack_propagate(False)

        self.expr_label = tk.Label(
            display_card,
            text="",
            font=("Segoe UI", 12),
            bg="#23272a",
            fg="#99aab5",
            anchor="e"
        )
        self.expr_label.place(relx=1.0, x=-10, y=5, anchor="ne")

        self.display = tk.Entry(
            display_card,
            font=("Segoe UI", 26, "bold"),
            bd=0,
            justify="right",
            bg="#23272a",
            fg="white",
            insertbackground="white"
        )
        self.display.place(relx=1.0, x=-10, y=40, anchor="ne", width=260)

        # Buttons Frame
        btn_frame = tk.Frame(self, bg="#2c2f33")
        btn_frame.pack(expand=True, fill="both", padx=10, pady=10)

        buttons = [
            ("7", "#99aab5"), ("8", "#99aab5"), ("9", "#99aab5"), ("/", "#7289da"),
            ("4", "#99aab5"), ("5", "#99aab5"), ("6", "#99aab5"), ("x", "#7289da"),
            ("1", "#99aab5"), ("2", "#99aab5"), ("3", "#99aab5"), ("-", "#7289da"),
            ("0", "#99aab5"), (".", "#99aab5"), ("C", "#f04747"), ("+", "#7289da"),
        ]

        row = col = 0
        for text, color in buttons:
            btn = self.rounded_button(
                btn_frame,
                text,
                color,
                lambda t=text: self.on_click(t)
            )
            btn.grid(row=row, column=col, padx=6, pady=6)

            col += 1
            if col > 3:
                col = 0
                row += 1

        # Equal Button
        equal_btn = self.rounded_button(
            btn_frame,
            "=",
            "#43b581",
            self.calculate,
            fg="white",
            w=300,
            h=55
        )
        equal_btn.grid(row=4, column=0, columnspan=4, padx=6, pady=6)

        # Grid Resize
        for i in range(5):
            btn_frame.rowconfigure(i, weight=1)
        for i in range(4):
            btn_frame.columnconfigure(i, weight=1)

        # Keyboard Bindings
        self.bind("<Key>", self.key_input)
        self.bind("<Return>", lambda e: self.calculate())
        self.bind("<BackSpace>", self.backspace)

        # Animation Function
    def animate_result(self, start_y=60, end_y=40, step=2):
        if start_y <= end_y:
            return
        
        self.display.place_configure(y=start_y)
        self.after(10, lambda: self.animate_result(start_y - step, end_y))


    # ---------- Functions ----------

    def rounded_button(self, parent, text, bg, command, fg="black", w=70, h=50):
        canvas = tk.Canvas(
            parent,
            width=w,
            height=h,
            bg=parent["bg"],
            highlightthickness=0
        )

        r = 20
        x1, y1, x2, y2 = 5, 5, w-5, h-5

        canvas.create_oval(x1, y1, x1+r, y1+r, fill=bg, outline=bg)
        canvas.create_oval(x2-r, y1, x2, y1+r, fill=bg, outline=bg)
        canvas.create_oval(x1, y2-r, x1+r, y2, fill=bg, outline=bg)
        canvas.create_oval(x2-r, y2-r, x2, y2, fill=bg, outline=bg)
        canvas.create_rectangle(x1+r//2, y1, x2-r//2, y2, fill=bg, outline=bg)
        canvas.create_rectangle(x1, y1+r//2, x2, y2-r//2, fill=bg, outline=bg)

        text_id = canvas.create_text(
            w//2, h//2,
            text=text,
            fill=fg,
            font=("Segoe UI", 14, "bold")
        )

        canvas.bind("<Button-1>", lambda e: command())
        canvas.bind("<Enter>", lambda e: canvas.itemconfig(text_id, fill="white"))
        canvas.bind("<Leave>", lambda e: canvas.itemconfig(text_id, fill=fg))

        return canvas

    # Fade_in Function
    def fade_in(self, i=0):
        colors = ["#555", "#777", "#999", "#bbb","#fff"]

        if i >= len(colors):
            return
        
        self.display.config(fg=colors[i])
        self.after(40, lambda: self.fade_in(i + 1))

    # Error Shake
    def shake_error(self, count=0, direction=1):
        if count >= 10:
            self.display.place_configure(x=-10)
            return
        
        offset = 5 * direction
        self.display.place_configure(x=-10 + offset)

        self.after(30, lambda: self.shake_error(count + 1, -direction))

    def on_click(self, value):
        if value == "C":
            self.expression = ""
            self.expr_label.config(text="")
            self.display.delete(0, tk.END)
        else:
            if value == "x":
                value = "*"
            self.expression += value
            self.expr_label.config(text=self.expression)

        self.display.delete(0, tk.END)
        self.display.insert(tk.END, self.expression)

    def calculate(self):
        try:
            result = eval(self.expression)
            if result == float('inf') or result == float('-inf'):
                raise ZeroDivisionError
            self.expression = str(result)
        except ZeroDivisionError:
            self.display.insert(0, "Cannot divide by 0")
            self.expression = ""
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, str(result))
            self.expr_label.config(text="")
            self.animate_result()
            self.fade_in()
            
        except:
            self.display.delete(0, tk.END)
            self.display.insert(0, "Error")
            self.expression = ""
            self.shake_error()
            self.display.config(fg="#f04747")
            self.after(300, lambda: self.display.config(fg="white"))

    def backspace(self, event=None):
        self.expression = self.expression[:-1]
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, self.expression)

    def key_input(self, event):
        if event.char in "0123456789+-*/.":
            self.on_click(event.char)


if __name__ == "__main__":
    app = Calculator()

    app.mainloop()

