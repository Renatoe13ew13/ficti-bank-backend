from sqlmodel import SQLModel, Field
from typing import Optional, List, Any

# ===============================================================
# SCHEMAS PARA LA SALIDA DE DATOS ESTANDARIZADA
# ===============================================================

class APIResponse(SQLModel):
    """
    Estructura de respuesta estandarizada para éxito o error.
    """
    mensaje: str = Field(..., description="Mensaje de éxito o descripción del error.")
    codigo: Optional[str] = Field(default=None, description="Código de referencia (ej: NroCta, Codigo de Error).")
    status_code: int = Field(..., description="Código de estado HTTP de la respuesta.")
    result: Optional[List[Any]] = Field(default=None, description="Contenedor para la lista de resultados de la operación.")
