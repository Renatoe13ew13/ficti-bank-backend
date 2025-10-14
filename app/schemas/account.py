from sqlmodel import SQLModel, Field
from typing import Optional, Literal
from datetime import date

# ===============================================================
# SCHEMAS PARA LA ENTRADA DE DATOS (REQUEST BODY)
# ===============================================================


class CuentaCreationData(SQLModel):
    """
    Define los datos necesarios para llamar al stored procedure
    sp_InsertarNuevaCuenta.
    """
    TipoCta: str = Field(..., max_length=2, description="Tipo de cuenta (AC, CC, PF)")
    Moneda: str = Field(..., max_length=2, description="Tipo de moneda (SO, DO)")
    SaldoInicial: float = Field(..., gt=0, description="Monto inicial de la cuenta")
    CodUsu: str = Field(..., max_length=10, description="Código del usuario que está creando/es dueño de la cuenta")

# ===============================================================
# SCHEMAS PARA LA SALIDA DE DATOS ESTANDARIZADA
# ===============================================================


class CuentaDetailsDTO(SQLModel):
    """
    DTO/Schema que mapea el conjunto de resultados devuelto por sp_ListarCuentas.
    Los nombres de los campos DEBEN coincidir con los alias del SELECT del SP.
    """
    NroCta: str = Field(..., max_length=20)
    TipoCta: str = Field(..., max_length=2, alias="TipoCta_Code")  # Opcional: renombrar si el front lo prefiere
    TipoCuenta: Optional[str] = Field(default=None, description="Descripción del tipo de cuenta.")
    CodCliente: str = Field(..., max_length=10)
    Moneda: str = Field(..., max_length=2)
    FechaApertura: date
    SaldoActual: float
    SaldoPromedio: float
    CodUsu: str = Field(..., max_length=10)
    UsuarioPropietario: str = Field(..., description="Nombre de usuario asociado (T_Usuario.Usuario)")
    Estado: str = Field(..., max_length=1)


class CuentaEstadoUpdate(SQLModel):
    """
    Define los datos requeridos en el cuerpo JSON para actualizar el estado de una cuenta.
    """
    nro_cta: str = Field(..., max_length=20, description="Número único de la cuenta a modificar.")
    
    # Usamos Literal para restringir los valores aceptados, reforzando la regla CHAR(1) del SP.
    nuevo_estado: Literal['A', 'I', 'B'] = Field(..., description="Nuevo estado de la cuenta ('A': Activa, 'I': Inactiva, 'B': Bloqueada).")
    
    cod_usu_modifica: str = Field(..., max_length=10, description="Código del usuario que autoriza el cambio (debe ser un administrador o rol autorizado).")
    
