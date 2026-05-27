
"""
🏦 CAJERO AUTOMÁTICO - Versión con POO
Autor: [XXXXXX]
Fecha: 2026
Características: Herencia, Polimorfismo, Encapsulamiento, Abstracción
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict

# ═══════════════════════════════════════════════════════
# CLASES BASE (ABSTRACCIÓN)
# ═══════════════════════════════════════════════════════
class CuentaBancaria(ABC):
    """Clase abstracta que define el contrato para todas las cuentas."""

    def __init__(self, numero_cuenta: str, titular: str, saldo: float = 0):
        self._numero_cuenta = numero_cuenta  # Encapsulamiento
        self._titular = titular
        self._saldo = saldo
        self._historial: List[Dict] = []

    @abstractmethod
    def calcular_comision(self, monto: float) -> float:
        """Método abstracto: cada tipo de cuenta tiene su propia comisión."""
        pass

    @abstractmethod
    def get_tipo_cuenta(self) -> str:
        """Retorna el tipo de cuenta (polimorfismo)."""
        pass

    def depositar(self, monto: float) -> bool:
        """Método concreto heredado por todas las cuentas."""
        if monto > 0:
            self._saldo += monto
            self._registrar_transaccion("DEPÓSITO", monto)
            return True
        return False

    def retirar(self, monto: float) -> bool:
        """Método que puede ser sobrescrito (polimorfismo)."""
        comision = self.calcular_comision(monto)
        total_a_restar = monto + comision

        if total_a_restar <= self._saldo:
            self._saldo -= total_a_restar
            self._registrar_transaccion("RETIRO", -monto, f"Comisión: ${comision:,.0f}")
            return True
        return False

    def _registrar_transaccion(self, tipo: str, monto: float, detalle: str = ""):
        """Método protegido para registrar transacciones."""
        self._historial.append(
            {"fecha": datetime.now(), "tipo": tipo, "monto": monto, "detalle": detalle}
        )

    # Getters y Setters (Encapsulamiento)
    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def numero_cuenta(self) -> str:
        return self._numero_cuenta

    def get_historial(self) -> List[Dict]:
        return self._historial.copy()


# ═══════════════════════════════════════════════════════
# CLASES DERIVADAS (HERENCIA Y POLIMORFISMO)
# ═══════════════════════════════════════════════════════


class CuentaAhorros(CuentaBancaria):
    """Cuenta de ahorros con interés y sin comisión."""

    _tasa_interes = 0.05  # 5% anual - Variable de clase

    def __init__(self, numero_cuenta: str, titular: str, saldo: float = 0):
        super().__init__(numero_cuenta, titular, saldo)
        self._ultima_fecha_interes = datetime.now()

    def calcular_comision(self, monto: float) -> float:
        """Sin comisión para ahorros."""
        return 0.0

    def get_tipo_cuenta(self) -> str:
        return "💰 AHORROS"

    def aplicar_interes(self):
        """Aplica interés mensual a la cuenta."""
        interes_mensual = (self._tasa_interes / 12) * self._saldo
        if interes_mensual > 0:
            self._saldo += interes_mensual
            self._registrar_transaccion(
                "INTERÉS", interes_mensual, "Interés mensual aplicado"
            )
            return interes_mensual
        return 0


class CuentaCorriente(CuentaBancaria):
    """Cuenta corriente con sobregiro y comisión."""

    def __init__(
        self,
        numero_cuenta: str,
        titular: str,
        saldo: float = 0,
        limite_sobregiro: float = 500000,
    ):
        super().__init__(numero_cuenta, titular, saldo)
        self._limite_sobregiro = limite_sobregiro

    def calcular_comision(self, monto: float) -> float:
        """Comisión del 2% por transacción."""
        return monto * 0.02

    def get_tipo_cuenta(self) -> str:
        return "🏦 CORRIENTE"

    def retirar(self, monto: float) -> bool:
        """Permite sobregiro hasta el límite establecido."""
        comision = self.calcular_comision(monto)
        total_a_restar = monto + comision

        if total_a_restar <= (self._saldo + self._limite_sobregiro):
            self._saldo -= total_a_restar
            self._registrar_transaccion(
                "RETIRO",
                -monto,
                f"Comisión: ${comision:,.0f} | Saldo: ${self._saldo:,.0f}",
            )
            return True
        return False


class CuentaNomina(CuentaBancaria):
    """Cuenta nómina para empleados con beneficios."""

    def __init__(
        self, numero_cuenta: str, titular: str, saldo: float = 0, empresa: str = ""
    ):
        super().__init__(numero_cuenta, titular, saldo)
        self._empresa = empresa

    def calcular_comision(self, monto: float) -> float:
        """Sin comisión si es depósito de nómina, sino 1%."""
        return 0.0

    def get_tipo_cuenta(self) -> str:
        return "💼 NÓMINA"

    def depositar_nomina(self, monto: float) -> bool:
        """Depósito especial de nómina sin límites."""
        return self.depositar(monto)


# ═══════════════════════════════════════════════════════
# CLASE USUARIO (COMPOSICIÓN)
# ═══════════════════════════════════════════════════════


class Usuario:
    """Clase que representa un usuario del cajero."""

    def __init__(self, nombre: str, pin: str):
        self._nombre = nombre
        self._pin = pin
        self._cuentas: Dict[str, CuentaBancaria] = {}
        self._intentos_fallidos = 0

    def agregar_cuenta(self, cuenta: CuentaBancaria):
        """Agrega una cuenta al usuario."""
        self._cuentas[cuenta.numero_cuenta] = cuenta

    def verificar_pin(self, pin_ingresado: str) -> bool:
        """Verifica el PIN con control de intentos."""
        if pin_ingresado == self._pin:
            self._intentos_fallidos = 0
            return True
        else:
            self._intentos_fallidos += 1
            return False

    def get_cuenta(self, numero_cuenta: str) -> CuentaBancaria:
        return self._cuentas.get(numero_cuenta)

    def listar_cuentas(self) -> List[CuentaBancaria]:
        return list(self._cuentas.values())

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def intentos_fallidos(self) -> int:
        return self._intentos_fallidos


# ═══════════════════════════════════════════════════════
# CAJERO AUTOMÁTICO (SISTEMA PRINCIPAL)
# ═══════════════════════════════════════════════════════


class CajeroAutomatico:
    """Sistema principal del cajero automático."""

    def __init__(self):
        self._usuarios: Dict[str, Usuario] = {}
        self._usuario_actual: Usuario = None
        self._inicializar_usuarios_demo()

    def _inicializar_usuarios_demo(self):
        """Crea usuarios de demostración."""
        # Usuario 1: Con cuenta de ahorros
        usuario1 = Usuario("Julian Aguilera", "2005")
        cuenta_ahorros = CuentaAhorros("502", "Julian Aguilera", 1000000)
        usuario1.agregar_cuenta(cuenta_ahorros)
        self._usuarios["502"] = usuario1

        # Usuario 2: Con cuenta corriente
        usuario2 = Usuario("María García", "5678")
        cuenta_corriente = CuentaCorriente("002", "María García", 2000000, 500000)
        usuario2.agregar_cuenta(cuenta_corriente)
        usuario2.agregar_cuenta(CuentaAhorros("003", "María García", 500000))
        self._usuarios["002"] = usuario2

        # Usuario 3: Con cuenta nómina
        usuario3 = Usuario("Carlos López", "9999")
        cuenta_nomina = CuentaNomina("004", "Carlos López", 750000, "Tech Corp")
        usuario3.agregar_cuenta(cuenta_nomina)
        self._usuarios["004"] = usuario3
        

    def autenticar(self) -> bool:
        """Autentica al usuario."""
        print("\n🔐 " + "=" * 50)
        print("   AUTENTICACIÓN DE USUARIO")
        print("🔐 " + "=" * 50)

        intentos_restantes = 3
        while intentos_restantes > 0:
            numero_cuenta = input("Número de cuenta: ").strip()
            pin = input("PIN: ").strip()

            if numero_cuenta in self._usuarios:
                usuario = self._usuarios[numero_cuenta]
                if usuario.verificar_pin(pin):
                    self._usuario_actual = usuario
                    print(f"\n✅ ¡Bienvenido, {usuario.nombre}!")
                    return True
                else:
                    intentos_restantes -= 1
                    print(
                        f"❌ PIN incorrecto. Intentos restantes: {intentos_restantes}"
                    )
            else:
                intentos_restantes -= 1
                print(
                    f"❌ Cuenta no encontrada. Intentos restantes: {intentos_restantes}"
                )

        print("\n🔒 Cuenta bloqueada por seguridad.")
        return False

    def menu_principal(self):
        """Menú principal del cajero."""
        while True:
            cuentas = self._usuario_actual.listar_cuentas()

            print("\n" + "📋 " + "=" * 50)
            print("   MENÚ PRINCIPAL")
            print("📋 " + "=" * 50)

            # Mostrar cuentas disponibles
            for i, cuenta in enumerate(cuentas, 1):
                print(f"{i}. {cuenta.get_tipo_cuenta()} - {cuenta.numero_cuenta}")
                print(f"   💰 Saldo: ${cuenta.saldo:,.0f}")

            print(f"\n{len(cuentas) + 1}. 🔄 Cambiar de cuenta")
            print(f"{len(cuentas) + 2}. 📜 Ver historial")
            print(f"{len(cuentas) + 3}. 🚪 Salir")

            try:
                opcion = int(input("\n➡️  Seleccione una opción: "))

                if 1 <= opcion <= len(cuentas):
                    self._menu_operaciones(cuentas[opcion - 1])
                elif opcion == len(cuentas) + 1:
                    continue  # Volver a mostrar menú
                elif opcion == len(cuentas) + 2:
                    self._ver_historial_global()
                elif opcion == len(cuentas) + 3:
                    self.salir()
                    break
                else:
                    print("⚠️  Opción no válida.")

            except ValueError:
                print("⚠️  Ingrese un número válido.")

    def _menu_operaciones(self, cuenta: CuentaBancaria):
        """Menú de operaciones para una cuenta específica."""
        while True:
            print(f"\n🏦 " + "=" * 50)
            print(f"   CUENTA: {cuenta.get_tipo_cuenta()} - {cuenta.numero_cuenta}")
            print(f"   💰 Saldo actual: ${cuenta.saldo:,.0f}")
            print("🏦 " + "=" * 50)

            print("\n1. 💰 Consultar saldo")
            print("2. 📥 Depositar")
            print("3. 📤 Retirar")
            print("4. 📊 Ver detalles de cuenta")
            print("5. ⬅️  Volver al menú principal")

            try:
                opcion = int(input("\n➡️  Seleccione: "))

                if opcion == 1:
                    print(f"\n💰 Saldo disponible: ${cuenta.saldo:,.0f}")
                elif opcion == 2:
                    monto = float(input("Monto a depositar: $"))
                    if cuenta.depositar(monto):
                        print(f"✅ Depósito exitoso de ${monto:,.0f}")
                    else:
                        print("❌ Error en el depósito.")
                elif opcion == 3:
                    monto = float(input("Monto a retirar: $"))
                    if cuenta.retirar(monto):
                        print(f"✅ Retiro exitoso de ${monto:,.0f}")
                    else:
                        print("❌ Fondos insuficientes.")
                elif opcion == 4:
                    self._mostrar_detalles_cuenta(cuenta)
                elif opcion == 5:
                    break
                else:
                    print("⚠️  Opción no válida.")

            except ValueError:
                print("⚠️  Ingrese un número válido.")
            except KeyboardInterrupt:
                print("\n⚠️  Operación cancelada.")

    def _mostrar_detalles_cuenta(self, cuenta: CuentaBancaria):
        """Muestra detalles específicos del tipo de cuenta."""
        print("\n📊 " + "=" * 40)
        print("   DETALLES DE LA CUENTA")
        print("📊 " + "=" * 40)
        print(f"Tipo: {cuenta.get_tipo_cuenta()}")
        print(f"Número: {cuenta.numero_cuenta}")
        print(f"Titular: {cuenta._titular}")
        print(f"Saldo: ${cuenta.saldo:,.0f}")

        # Polimorfismo: cada tipo muestra información diferente
        if isinstance(cuenta, CuentaAhorros):
            print(f"Tasa de interés: {cuenta._tasa_interes * 100:.1f}% anual")
        elif isinstance(cuenta, CuentaCorriente):
            print(f"Límite de sobregiro: ${cuenta._limite_sobregiro:,.0f}")
        elif isinstance(cuenta, CuentaNomina):
            print(f"Empresa: {cuenta._empresa}")

        print("=" * 40)

    def _ver_historial_global(self):
        """Muestra el historial de todas las cuentas del usuario."""
        print("\n📜 " + "=" * 60)
        print("   HISTORIAL DE TRANSACCIONES")
        print("📜 " + "=" * 60)

        todas_las_transacciones = []
        for cuenta in self._usuario_actual.listar_cuentas():
            for trans in cuenta.get_historial():
                todas_las_transacciones.append(
                    {"cuenta": cuenta.numero_cuenta, **trans}
                )

        if not todas_las_transacciones:
            print("⚪ No hay transacciones registradas.")
        else:
            # Ordenar por fecha (más recientes primero)
            todas_las_transacciones.sort(key=lambda x: x["fecha"], reverse=True)

            print(
                f"{'FECHA':<15} {'CUENTA':<10} {'TIPO':<12} {'MONTO':>15} {'DETALLE'}"
            )
            print("-" * 70)
            for trans in todas_las_transacciones[:20]:  # Últimas 20
                fecha = trans["fecha"].strftime("%d/%m %H:%M")
                monto = (
                    f"${abs(trans['monto']):,.0f}" if trans["monto"] != 0 else "----"
                )
                print(
                    f"{fecha:<15} {trans['cuenta']:<10} {trans['tipo']:<12} {monto:>15} {trans['detalle']}"
                )

        print("=" * 60)

    def salir(self):
        """Muestra mensaje de despedida."""
        print("\n" + "🏦 " + "=" * 50)
        print("   👋 ¡Gracias por usar nuestro Cajero!")
        print("   💙 Que tenga un excelente día")
        print("🏦 " + "=" * 50 + "\n")


# ═══════════════════════════════════════════════════════
# PUNTO DE ENTRADA
# ═══════════════════════════════════════════════════════
if __name__ == "__main__":
    try:
        cajero = CajeroAutomatico()

        print("\n" + "🏦 " + "=" * 50)
        print("   CAJERO AUTOMÁTICO - SISTEMA AVANZADO")
        print("   Versión con Herencia y Polimorfismo")
        print("🏦 " + "=" * 50)

        print("\n👥 USUARIOS DE DEMOSTRACIÓN:")
        print("   • Julian Aguilera - Cuenta: 502 - PIN: 2005")
        print("   • María García - Cuenta: 002 - PIN: 5678")
        print("   • Carlos López - Cuenta: 004 - PIN: 9999")

        if cajero.autenticar():
            cajero.menu_principal()

    except Exception as e:
        print(f"\n❌ Error del sistema: {e}")
    finally:
        input("\nPresione ENTER para finalizar...")