Cerramos el ciclo CRUD con el último módulo esencial para la gestión del sistema: **CU-04: Borrar Número Ganador**.

Desde la perspectiva de la calidad del software y la experiencia de usuario (UX), una operación destructiva como la eliminación **nunca debe ejecutarse en un solo paso**. Por ello, se incorpora un mecanismo de seguridad crítico: un diálogo o modal de confirmación en el *frontend* antes de impactar de forma irreversible la base de datos.

Aquí tienes la especificación formal del caso de uso y su correspondiente diagrama de secuencia listo para **PlantText**.

## Caso de Uso 4: Borrar Número Ganador

### Identificador

CU-04

### Objetivo

Permitir al Administrador de la Aplicación eliminar un registro de sorteo específico del sistema a través del Dashboard personalizado, manteniendo la integridad del historial de la lotería.

### Actores

- **Actor Principal:** Administrador de la Aplicación (Autenticado en el frontend custom).

- **Actores Secundarios:** Ninguno.

### Disparador

El administrador hace clic en el botón "Eliminar" (icono de papelera) en la fila de un sorteo específico dentro del listado del Dashboard.

### Precondiciones

1. El Administrador debe estar autenticado con un rol de gestión que incluya permisos de eliminación.

2. El registro seleccionado debe existir en la base de datos.

### Flujo Principal (Eliminación Exitosa)

1. El Administrador solicita la eliminación de un registro desde el listado.

2. El sistema (en la interfaz del cliente) intercepta la acción y despliega un modal emergente de advertencia pidiendo confirmar la acción.

3. El Administrador hace clic en el botón "Confirmar Eliminación".

4. El sistema envía una petición segura (petición HTTP `POST` apuntando a la vista `SorteoDeleteView` de Django).

5. La vista localiza el registro por su ID y ejecuta el método de borrado del ORM.

6. El sistema elimina físicamente el registro de la base de datos a través de una instrucción *DELETE*.

7. El sistema redirige automáticamente al Administrador al listado actualizado y despliega una notificación flotante (*Toast*) con el mensaje: *"Sorteo eliminado permanentemente"*.

### Flujos Alternativos

| **ID**    | **Descripción**                                                                                                                                                                                                                  |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **FA-01** | **Cancelar Eliminación:** En el paso 3, el administrador desiste de la acción y hace clic en "Cancelar" dentro del modal. El sistema cierra la ventana emergente, aborta la petición y mantiene el registro intacto en la lista. |

### Flujos de Excepción

| **ID**    | **Descripción**                                                                                                                                                                                                                                                                                                                                                        |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **FE-01** | **Registro Inexistente por Concurrencia (404):** En el paso 5, si el registro ya fue eliminado previamente por otro usuario en otra sesión, Django no podrá localizar el objeto (`Sorteo.DoesNotExist`), detendrá el proceso de borrado y renderizará una respuesta controlada con un mensaje de advertencia: *"El elemento seleccionado ya no existe en el sistema"*. |

### Postcondiciones

El registro es removido de la base de datos de manera definitiva. La información se actualiza en tiempo real desapareciendo tanto del panel privado de control como de la vista pública de resultados (CU-02).

### Reglas de Negocio

- **RN-05 (Confirmación de Acción Destructiva):** Ningún elemento de la base de datos puede ser eliminado mediante un solo clic directo; la interfaz está obligada a presentar un paso intermedio de confirmación de intenciones al usuario.

### Prioridad

Alta

### Frecuencia de Uso

Baja

### Casos Relacionados

- **CU-02** (Consultar Números Ganadores / Listar)
