import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ==========================================
# CLASE CUENTA (POO)
# ==========================================

class Cuenta:
    def __init__(self, titular, tipo, saldo):
        self.titular = titular
        self.tipo = tipo
        self.__saldo = saldo
        self.historial = []

    def depositar(self, monto):
        if monto > 0:
            self.__saldo += monto
            self.registrar_movimiento("Depósito", monto)
            return True
        return False

    def retirar(self, monto):
        if 0 < monto <= self.__saldo:
            self.__saldo -= monto
            self.registrar_movimiento("Retiro", monto)
            return True
        return False

    def obtener_saldo(self):
        return self.__saldo

    def registrar_movimiento(self, tipo, monto):
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.historial.append(f"{fecha} - {tipo}: ${monto:,}")

# ==========================================
# BASE DE USUARIOS
# ==========================================

usuarios = {
    "jeison": {
        "password": "1234",
        "cuenta": Cuenta("Jeyson Gallego", "Ahorros", 1700000)
    },
    "admin": {
        "password": "admin",
        "cuenta": Cuenta("Administrador", "Corriente", 5000000)
    },
    "invitado": {
        "password": "0000",
        "cuenta": Cuenta("Usuario Invitado", "Ahorros", 100000)
    }
}

# ==========================================
# INTERFAZ
# ==========================================

class CajeroGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("🏦 Cajero Automático Pro")
        self.root.geometry("500x500")
        self.root.configure(bg="#020205")

        self.usuario_actual = None

        self.crear_login()

    # ================= LOGIN =================
    def crear_login(self):
        self.limpiar()

        frame = tk.Frame(self.root, bg="#1e1e2f")
        frame.pack(expand=True)

        tk.Label(frame, text="CAJERO AUTOMÁTICO",
                 font=("Arial", 20, "bold"),
                 fg="white", bg="#1e1e2f").pack(pady=20)

        ttk.Label(frame, text="Usuario:").pack()
        self.entry_user = ttk.Entry(frame)
        self.entry_user.pack(pady=5)

        ttk.Label(frame, text="Contraseña:").pack()
        self.entry_pass = ttk.Entry(frame, show="*")
        self.entry_pass.pack(pady=5)

        ttk.Button(frame, text="Iniciar sesión",
                   command=self.validar_login).pack(pady=20)

    def validar_login(self):
        user = self.entry_user.get().lower()
        password = self.entry_pass.get()

        if user in usuarios and usuarios[user]["password"] == password:
            self.usuario_actual = usuarios[user]["cuenta"]
            self.menu_principal()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    # ================= MENÚ =================
    def menu_principal(self):
        self.limpiar()

        frame = tk.Frame(self.root, bg="#9898b9")
        frame.pack(expand=True)

        tk.Label(frame,
                 text=f"Bienvenido {self.usuario_actual.titular}",
                 font=("Arial", 16, "bold"),
                 fg="white", bg="#1e1e2f").pack(pady=10)

        tk.Label(frame,
                 text=f"Cuenta: {self.usuario_actual.tipo}",
                 fg="white", bg="#1e1e2f").pack()

        self.label_saldo = tk.Label(
            frame,
            text=f"Saldo: ${self.usuario_actual.obtener_saldo():,}",
            font=("Arial", 14),
            fg="#00ff88",
            bg="#1e1e2f"
        )
        self.label_saldo.pack(pady=10)

        ttk.Button(frame, text="Depositar",
                   command=self.depositar).pack(pady=5)

        ttk.Button(frame, text="Retirar",
                   command=self.retirar).pack(pady=5)

        ttk.Button(frame, text="Ver Historial",
                   command=self.ver_historial).pack(pady=5)

        ttk.Button(frame, text="Cerrar sesión",
                   command=self.crear_login).pack(pady=20)

    # ================= OPERACIONES =================
    def depositar(self):
        monto = self.pedir_monto("Monto a depositar")
        if monto and self.usuario_actual.depositar(monto):
            self.actualizar_saldo()
            messagebox.showinfo("Éxito", "Depósito realizado")
        else:
            messagebox.showerror("Error", "Monto inválido")

    def retirar(self):
        monto = self.pedir_monto("Monto a retirar")
        if monto and self.usuario_actual.retirar(monto):
            self.actualizar_saldo()
            messagebox.showinfo("Éxito", "Retiro realizado")
        else:
            messagebox.showerror("Error", "Fondos insuficientes")

    def actualizar_saldo(self):
        self.label_saldo.config(
            text=f"Saldo: ${self.usuario_actual.obtener_saldo():,}"
        )

    # ================= HISTORIAL =================
    def ver_historial(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Historial de Movimientos")
        ventana.geometry("400x300")

        lista = tk.Listbox(ventana, width=60)
        lista.pack(pady=10)

        for mov in self.usuario_actual.historial:
            lista.insert(tk.END, mov)

    # ================= MONTO =================
    def pedir_monto(self, mensaje):
        ventana = tk.Toplevel(self.root)
        ventana.title("Ingrese monto")
        ventana.geometry("300x150")

        ttk.Label(ventana, text=mensaje).pack(pady=10)
        entrada = ttk.Entry(ventana)
        entrada.pack(pady=5)

        resultado = {"valor": None}

        def aceptar():
            try:
                resultado["valor"] = float(entrada.get())
                ventana.destroy()
            except:
                messagebox.showerror("Error", "Número inválido")

        ttk.Button(ventana, text="Aceptar",
                   command=aceptar).pack(pady=10)

        ventana.grab_set()
        self.root.wait_window(ventana)

        return resultado["valor"]

    # ================= LIMPIAR =================
    def limpiar(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# ==========================================
# EJECUCIÓN
# ==========================================

if __name__ == "__main__":
    root = tk.Tk()
    app = CajeroGUI(root)
    root.mainloop()