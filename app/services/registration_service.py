from typing import Dict, Any
from sqlmodel import Session
from sqlalchemy import text

from app.schemas.registration import FullClientRegistration
from app.core.security import get_password_hash

def register_client_with_sp(session: Session, reg_data: FullClientRegistration) -> Dict[str, Any]:
    """
    Crea un nuevo Usuario y Cliente llamando al SP de forma robusta.
    Este método es más explícito y confiable para obtener los parámetros OUT.
    """
    user_data = reg_data.user_data
    client_data = reg_data.client_data

    # 1. La encriptación de la contraseña SIEMPRE se hace en Python.
    hashed_password = get_password_hash(user_data.Password)

    try:
        # 2. Preparamos y ejecutamos la llamada al SP.
        #    Usamos variables de sesión estándar de MySQL (@variable).
        query = text("""
            CALL sp_RegisterFullClientAndUser(
                :p_Usuario, :p_Password, :p_Rol,
                :p_Nombres, :p_Apellidos, :p_DNI, :p_Email, :p_FechaNac,
                :p_Direccion, :p_CodUbigeo, :p_Telefonos, :p_Movil,
                @p_Out_CodUsu, @p_Out_CodCliente, @p_Out_Message
            );
        """)
        
        session.execute(query, {
            "p_Usuario": user_data.Usuario,
            "p_Password": hashed_password,
            "p_Rol": user_data.Rol,
            "p_Nombres": client_data.Nombres,
            "p_Apellidos": client_data.Apellidos,
            "p_DNI": client_data.DNI,
            "p_Email": client_data.e_mail,
            "p_FechaNac": client_data.Fecha_Nac,
            "p_Direccion": client_data.Direccion,
            "p_CodUbigeo": client_data.CodUbigeo,
            "p_Telefonos": client_data.Telefonos,
            "p_Movil": client_data.Movil
        })
        

        out_params_result = session.execute(
            text("SELECT @p_Out_CodUsu, @p_Out_CodCliente, @p_Out_Message;")
        ).first()

        # 4. Verificamos si el SP devolvió un mensaje de error.
        #    El mensaje de error es el tercer valor (índice 2) que devuelve nuestro SELECT.
        print(f"Resultado devuelto por la BD (out_params_result): {out_params_result}")
        if out_params_result and out_params_result[2] != "OK":
            # Si el mensaje no es NULL, significa que hubo un error de negocio.
            raise ValueError(out_params_result[2])

        # 5. Si todo salió bien, devolvemos los códigos generados.
        #    El CodUsu es el primer valor (índice 0) y el CodCliente el segundo (índice 1).
        return {
            "CodUsu": out_params_result[0],
            "CodCliente": out_params_result[1]
        }

    except Exception as e:
        # Si algo falla (ya sea la ejecución del SP o una excepción que lanzamos),
        # nos aseguramos de que la transacción se revierta para no dejar datos a medias.
        session.rollback()
        # Re-lanzamos la excepción para que el endpoint la maneje y devuelva un error HTTP.
        raise e