class ApiError(Exception):
    code = 422
    description = "Default message"


class EmailBadRequestError(ApiError):
    code = 400
    description = "Los campos email o app_uuid no están presentes en la solicitud o email tiene un mal formato"


class EmailAlreadyExistsError(ApiError):
    code = 412
    description = "El correo ya está registrado"


class EmailNotFoundError(ApiError):
    code = 404
    # Usuario no encontrado
    description = "Email no encontrado"


class TokenNotFoundError(ApiError):
    code = 403
    # El token no está en el encabezado de la solicitud.
    description = "El token no está en el encabezado de la solicitud."


class TokenNotValidError(ApiError):
    code = 401
    # El token no es válido o está vencido.
    description = "El token no es válido o está vencido."


class ResetBlackListDBError(ApiError):
    code = 500
    #'Error al eliminar registros de blacklist.
    description = "Error al eliminar registros de blacklist"

class ApiErrorCallBack(ApiError):
    code = 500
    description = "Error al obtener callback de TrueNative API"

    