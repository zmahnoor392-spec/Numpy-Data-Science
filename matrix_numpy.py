import tkinter as tk
from tkinter import messagebox
import numpy as np
import sys

class MatrixNumpy:
    def add(self, A, B): return np.add(A, B)
    def subtract(self, A, B): return np.subtract(A, B)
    def multiply(self, A, B): return np.dot(A, B)
    def transpose(self, A): return A.T
    def determinant(self, A): return np.linalg.det(A)
    def inverse(self, A):
        try: return np.linalg.inv(A)
        except np.linalg.LinAlgError: return None

def print_matrix(name, res):
    print(f"\n{name}:")
    if res is None:
        print("  Singular Matrix (no inverse)")
        return
    if isinstance(res, np.ndarray):
        if res.ndim == 2:
            for i, row in enumerate(res):
                bracket = "⎡" if i == 0 else "⎢" if i == 1 else "⎣"
                end_bracket = "⎤" if i == 0 else "⎥" if i == 1 else "⎦"
                row_data = "  ".join([f"{val:8.2f}" for val in row])
                print(f"  {bracket} {row_data} {end_bracket}")
        else:
            print(" ", res)
    else:
        print(f"  {res}")

def run_cli():
    print("=" * 50)
    print("      MATRIX MASTER PRO 3x3 (NumPy CLI)")
    print("=" * 50)
    calc = MatrixNumpy()

    def input_matrix(name):
        print(f"\nEnter 3x3 Matrix {name} (3 numbers per line):")
        matrix = []
        for i in range(3):
            while True:
                try:
                    line = input(f"  Row {i+1}: ").strip()
                    row = [float(x) for x in line.split()]
                    if len(row) != 3:
                        print("  Error: Please enter exactly 3 space-separated numbers.")
                        continue
                    matrix.append(row)
                    break
                except ValueError:
                    print("  Error: Invalid numbers. Try again.")
        return np.array(matrix)

    m1 = input_matrix("A")
    m2 = input_matrix("B")

    print_matrix("Matrix A", m1)
    print_matrix("Matrix B", m2)

    while True:
        print("\n" + "-" * 40)
        print(" Choose Operation:")
        print(" 1. Addition (A + B)")
        print(" 2. Subtraction (A - B)")
        print(" 3. Multiplication (A * B)")
        print(" 4. Transpose (A^T)")
        print(" 5. Determinant (det(A))")
        print(" 6. Inverse (A^-1)")
        print(" 7. Re-enter Matrices")
        print(" 8. Exit")
        print("-" * 40)

        choice = input("Enter choice (1-8): ").strip()

        if choice == '1':
            print_matrix("A + B", calc.add(m1, m2))
        elif choice == '2':
            print_matrix("A - B", calc.subtract(m1, m2))
        elif choice == '3':
            print_matrix("A * B", calc.multiply(m1, m2))
        elif choice == '4':
            print_matrix("Transpose(A)", calc.transpose(m1))
        elif choice == '5':
            print(f"\nDeterminant of A: {calc.determinant(m1):.4f}")
        elif choice == '6':
            inv = calc.inverse(m1)
            print_matrix("Inverse(A)", inv)
        elif choice == '7':
            m1 = input_matrix("A")
            m2 = input_matrix("B")
        elif choice == '8':
            print("\nExiting Matrix Master Pro CLI. Goodbye!")
            break
        else:
            print("\nInvalid choice! Please select 1-8.")

class MatrixGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Master Pro")
        self.root.geometry("600x600")
        self.calc = MatrixNumpy()

        # Professional Dark Palette
        bg = "#0f172a"        # Deep Navy
        card_bg = "#1e293b"   # Slate
        fg = "#f8fafc"        # Off-White
        accent = "#8b5cf6"    # Vibrant Purple
        sec = "#22d3ee"       # Cyan
        text_f = "#94a3b8"

        root.configure(bg=bg)

        # Header Area
        tk.Label(root, text="MATRIX MASTER PRO", bg=bg, fg=accent, font=("Segoe UI", 24, "bold"), pady=20).pack()

        main_frame = tk.Frame(root, bg=bg)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20)

        # Matrix Inputs Frame
        inputs_frame = tk.Frame(main_frame, bg=card_bg, padx=20, pady=20)
        inputs_frame.pack(fill=tk.X, pady=10)

        self.entries_a, self.entries_b = [], []

        def create_matrix_grid(parent, title, list_to_fill):
            frame = tk.Frame(parent, bg=card_bg, highlightbackground="#334155", highlightthickness=1, padx=10, pady=10)
            frame.pack(side=tk.LEFT, padx=10)
            tk.Label(frame, text=title, bg=card_bg, fg=fg, font=("Segoe UI", 12, "bold")).pack(pady=(0, 10))
            grid = tk.Frame(frame, bg=card_bg)
            grid.pack(pady=5)
            for i in range(3):
                row = []
                for j in range(3):
                    e = tk.Entry(grid, width=5, bg="#0f172a", fg="white", insertbackground="white",
                                 relief="flat", font=("Consolas", 14), justify="center")
                    e.grid(row=i, column=j, padx=3, pady=3, ipady=5)
                    row.append(e)
                list_to_fill.append(row)

        create_matrix_grid(inputs_frame, "Matrix A", self.entries_a)
        create_matrix_grid(inputs_frame, "Matrix B", self.entries_b)

        # Controls
        controls = tk.Frame(main_frame, bg=bg, pady=20)
        controls.pack(fill=tk.X)

        btn_cfg = {"bg": accent, "fg": "white", "relief": "flat", "font": ("Segoe UI", 9, "bold"), "cursor": "hand2"}
        sec_btn = {"bg": sec, "fg": "#0f172a", "relief": "flat", "font": ("Segoe UI", 9, "bold"), "cursor": "hand2"}

        tk.Button(controls, text="Add", command=self.do_add, **btn_cfg).pack(side=tk.LEFT, expand=True, padx=5)
        tk.Button(controls, text="Sub", command=self.do_sub, **btn_cfg).pack(side=tk.LEFT, expand=True, padx=5)
        tk.Button(controls, text="Mul", command=self.do_mul, **btn_cfg).pack(side=tk.LEFT, expand=True, padx=5)
        tk.Button(controls, text="Trans(A)", command=self.do_trans, **sec_btn).pack(side=tk.LEFT, expand=True, padx=5)
        tk.Button(controls, text="Det(A)", command=self.do_det, **sec_btn).pack(side=tk.LEFT, expand=True, padx=5)
        tk.Button(controls, text="Inv(A)", command=self.do_inv, **sec_btn).pack(side=tk.LEFT, expand=True, padx=5)

        # Result Area
        res_frame = tk.Frame(main_frame, bg="#0f172a", padx=10, pady=10)
        res_frame.pack(fill=tk.BOTH, expand=True)

        self.result_text = tk.Text(res_frame, height=5, width=40, bg=card_bg, fg=sec,
                                  font=("Consolas", 14), relief="flat", padx=10, pady=10,
                                  highlightbackground=accent, highlightthickness=1)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        self.result_text.insert(tk.END, "Result will display here...")
        self.result_text.config(state=tk.DISABLED)

    def get_matrix(self, entries):
        try: return np.array([[float(e.get()) for e in row] for row in entries])
        except ValueError:
            messagebox.showerror("Error", "Please input numbers only.")
            return None

    def display_result(self, res):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)

        if isinstance(res, np.ndarray):
            if res.ndim == 2 and res.shape == (3, 3):
                res_str = ""
                for i, row in enumerate(res):
                    bracket = "⎡" if i == 0 else "⎢" if i == 1 else "⎣"
                    end_bracket = "⎤" if i == 0 else "⎥" if i == 1 else "⎦"
                    row_data = "  ".join([f"{val:8.2f}" for val in row])
                    res_str += f"{bracket} {row_data} {end_bracket}\n"
            else:
                res_str = "\n".join(["  ".join([f"{val:8.2f}" for val in row]) for row in res])
            self.result_text.insert(tk.END, res_str)
        else:
            self.result_text.insert(tk.END, f"Result: {str(res)}")

        self.result_text.config(state=tk.DISABLED)

    def do_add(self):
        a, b = self.get_matrix(self.entries_a), self.get_matrix(self.entries_b)
        if a is not None and b is not None: self.display_result(self.calc.add(a, b))

    def do_sub(self):
        a, b = self.get_matrix(self.entries_a), self.get_matrix(self.entries_b)
        if a is not None and b is not None: self.display_result(self.calc.subtract(a, b))

    def do_mul(self):
        a, b = self.get_matrix(self.entries_a), self.get_matrix(self.entries_b)
        if a is not None and b is not None: self.display_result(self.calc.multiply(a, b))

    def do_trans(self):
        a = self.get_matrix(self.entries_a)
        if a is not None: self.display_result(self.calc.transpose(a))

    def do_det(self):
        a = self.get_matrix(self.entries_a)
        if a is not None: self.display_result(f"{self.calc.determinant(a):.4f}")

    def do_inv(self):
        a = self.get_matrix(self.entries_a)
        if a is not None:
            inv = self.calc.inverse(a)
            if inv is not None: self.display_result(inv)
            else:
                self.result_text.config(state=tk.NORMAL)
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, "Singular Matrix (no inverse)")
                self.result_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        run_cli()
    else:
        root = tk.Tk()
        gui = MatrixGUI(root)
        root.mainloop()
