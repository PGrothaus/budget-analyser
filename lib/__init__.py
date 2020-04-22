import collections


Transaction = collections.namedtuple(
    "Transaction", ["estado",
                    "descripcion",
                    "monto",
                    "saldo",
                    "nombreCuenta",
                    "numeroCuenta",
                    "idCuenta",
                    "canal",
                    "tipo",
                    "fecha",
                    "fechaContable",
                    "id",
                    "numeroDocumento",
                    "codigoTransaccionFlexcube",
                    "codigoTransaccionFlexcubeExtendido",
                    "descripcionOficina",
                    "fechaMovimiento",
                    "fechaContableMovimiento",
                    "montoMovimiento",
                    "saldoMovimiento",
                    "detalleMovimiento",
                    "detalleGlosa",
                    ])
