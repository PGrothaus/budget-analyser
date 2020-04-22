import unittest

from tests import helper
from lib.category_memberships import load_assignments
from lib import categoriser
from lib import parsers
from lib import Transaction


class ACategoriser(unittest.TestCase):

    def setUp(self):
        self.assignments = load_assignments()
        data = helper.load_transaction_data()
        self.transactions = parsers.parse_transactions(data)

    def test_can_assign_a_transaction_1(self):
        trans = self.transactions[1]  # Metrogas
        res = categoriser.categorise_transaction(trans, self.assignments)
        assert res == (trans, "Servicios", "Gas")

    def test_can_assign_a_transaction_2(self):
        trans = self.transactions[16]  # Permiso Circulacion
        res = categoriser.categorise_transaction(trans, self.assignments)
        assert res == (trans, "Transport", "Car")

    def test_can_assign_a_transaction_3(self):
        trans = self.transactions[17]  # Sueldo Letś Talk
        res = categoriser.categorise_transaction(trans, self.assignments)
        assert res == (trans, "Ingresos", "Sueldo")

    def test_can_assign_a_transaction_4(self):
        trans = {
            "estado": None,
            "descripcion": "unknown transaction",
            "monto": "2680000",
            "saldo": "5769102",
            "nombreCuenta": "Cuenta Corriente",
            "numeroCuenta": "003330159106",
            "idCuenta": "CTD003330159106",
            "canal": "Oficina Central",
            "tipo": "cargo",
            "fecha": "20200414 16:54:11",
            "fechaContable": "15/04/2020",
            "id": "CTD003330159106:20200414 16:54:11:2680000:cargo:1",
            "numeroDocumento": "",
            "codigoTransaccionFlexcube": "238",
            "codigoTransaccionFlexcubeExtendido": "12034",
            "descripcionOficina": "OFICINA CENTRAL",
            "fechaMovimiento": 1586897651000,
            "fechaContableMovimiento": 1586923200000,
            "montoMovimiento": 2680000,
            "saldoMovimiento": 5769102,
            "detalleMovimiento": None,
            "detalleGlosa": []
        }
        trans = Transaction(**trans)
        res = categoriser.categorise_transaction(trans, self.assignments)
        assert res == (trans, None, None)
