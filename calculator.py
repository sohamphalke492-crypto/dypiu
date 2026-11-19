"""
Simple Calculator - Python Mini Project

"""

import ast
import operator
import tkinter as tk

# ---------- Calculation logic ----------

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def safe_eval(expression):
    """Evaluate a math expression safely using Python's AST."""

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
            left, right = _eval(node.left), _eval(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 1000:
                raise ValueError("Exponent too large")
            return OPERATORS[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
            return OPERATORS[type(node.op)](_eval(node.operand))
        raise ValueError("Invalid expression")

    return _eval(ast.parse(expression, mode="eval"))


def format_result(value):
    """Show 8.0 as 8, and trim long decimals."""
    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        return str(round(value, 10))
    return str(value)


# ---------- GUI ----------

class Calculator(tk.Tk):
    BUTTONS = [
        ["C", "(", ")", "⌫"],
        ["7", "8", "9", "÷"],
        ["4", "5", "6", "×"],
        ["1", "2", "3", "-"],
        ["0", ".", "%", "+"],
        ["^", "="],
    ]

    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("320x460")
        self.resizable(False, False)
        self.configure(bg="#1e1e2e")

        self.expression = ""
        self.history_text = tk.StringVar()
        self.display_text = tk.StringVar(value="0")

        self._build_display()
        self._build_buttons()
        self._bind_keys()

    def _build_display(self):
        tk.Label(
            self, textvariable=self.history_text, anchor="e",
            font=("Segoe UI", 12), bg="#1e1e2e", fg="#9399b2",
        ).pack(fill="x", padx=15, pady=(15, 0))

        tk.Label(
            self, textvariable=self.display_text, anchor="e",
            font=("Segoe UI", 28, "bold"), bg="#1e1e2e", fg="#cdd6f4",
        ).pack(fill="x", padx=15, pady=(0, 10))

    def _build_buttons(self):
        frame = tk.Frame(self, bg="#1e1e2e")
        frame.pack(expand=True, fill="both", padx=10, pady=10)

        for r, row in enumerate(self.BUTTONS):
            frame.rowconfigure(r, weight=1)
            for c, label in enumerate(row):
                frame.columnconfigure(c, weight=1)
                span = 3 if label == "=" else 1
                if label == "=":
                    bg, fg = "#a6e3a1", "#1e1e2e"
                elif label in "÷×-+%^":
                    bg, fg = "#fab387", "#1e1e2e"
                elif label in ("C", "⌫"):
                    bg, fg = "#f38ba8", "#1e1e2e"
                else:
                    bg, fg = "#313244", "#cdd6f4"
                tk.Button(
                    frame, text=label, font=("Segoe UI", 16), bg=bg, fg=fg,
                    relief="flat", bd=0, activebackground="#585b70",
                    command=lambda x=label: self.on_press(x),
                ).grid(row=r, column=c, columnspan=span,
                       sticky="nsew", padx=3, pady=3)

    def _bind_keys(self):
        self.bind("<Return>", lambda e: self.on_press("="))
        self.bind("<KP_Enter>", lambda e: self.on_press("="))
        self.bind("<BackSpace>", lambda e: self.on_press("⌫"))
        self.bind("<Escape>", lambda e: self.on_press("C"))
        self.bind("<Key>", self._on_key)

    def _on_key(self, event):
        if event.char in "0123456789.+-%()":
            self.on_press(event.char)
        elif event.char == "*":
            self.on_press("×")
        elif event.char == "/":
            self.on_press("÷")
        elif event.char == "^":
            self.on_press("^")

    def on_press(self, key):
        if key == "C":
            self.expression = ""
            self.history_text.set("")
        elif key == "⌫":
            self.expression = self.expression[:-1]
        elif key == "=":
            self.calculate()
            return
        else:
            self.expression += key
        self.display_text.set(self.expression or "0")

    def calculate(self):
        if not self.expression:
            return
        # Convert display symbols to Python operators
        python_expr = (self.expression.replace("×", "*")
                       .replace("÷", "/").replace("^", "**"))
        try:
            result = format_result(safe_eval(python_expr))
            self.history_text.set(self.expression + " =")
            self.expression = result
            self.display_text.set(result)
        except ZeroDivisionError:
            self._show_error("Cannot divide by 0")
        except Exception:
            self._show_error("Invalid input")

    def _show_error(self, message):
        self.history_text.set(self.expression)
        self.display_text.set(message)
        self.expression = ""


if __name__ == "__main__":
    Calculator().mainloop()
