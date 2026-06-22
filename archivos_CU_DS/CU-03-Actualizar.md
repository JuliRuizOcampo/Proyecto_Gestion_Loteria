## Caso de Uso 3: Actualizar Número Ganador

### Identificador

CU-03

### Objetivo

Permitir al Administrador de la Aplicación modificar el número de lotería o la fecha de un sorteo ya registrado, utilizando el Dashboard de control personalizado para corregir errores de digitación.

### Actores

- **Actor Principal:** Administrador de la Aplicación (Autenticado en el frontend custom).

- **Actores Secundarios:** Ninguno.

### Disparador

El administrador hace clic en el botón "Editar" (icono de lápiz) en la fila de un sorteo específico dentro del listado del Dashboard.

### Precondiciones

1. El Administrador debe estar autenticado y tener rol de edición activo.

2. El registro que se desea modificar debe existir en la base de datos (identificado por su ID único).

### Flujo Principal (Modificación Exitosa)

1. El Administrador solicita la edición de un registro desde el listado.

2. El sistema (mediante una vista de actualización de Django `SorteoUpdateView`) recupera el registro por su ID desde la base de datos.

3. El sistema renderiza el formulario personalizado pre-cargado con los datos actuales del sorteo (Número y Fecha).

4. El Administrador realiza los cambios pertinentes en los campos.

5. El Administrador hace clic en "Guardar Cambios".

6. El sistema procesa los nuevos datos mediante el formulario de Django (`SorteoForm`) y ejecuta las validaciones.

7. El sistema sobrescribe el registro en la base de datos aplicando un cambio de estado (*UPDATE*).

8. El sistema redirige al listado del Dashboard emitiendo un mensaje de éxito: *"Sorteo actualizado correctamente"*.

### Flujos Alternativos

| **ID**    | **Descripción**                                                                                                                                                           |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **FA-01** | **Cancelar Edición:** En el paso 4, el administrador presiona "Volver" o "Cancelar". El sistema cancela la edición, descarta los cambios en memoria y regresa al listado. |

### Flujos de Excepción

| **ID**    | **Descripción**                                                                                                                                                                                                                                                                      |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **FE-01** | **Registro no Encontrado (404):** En el paso 2, si el registro fue eliminado por otro administrador simultáneamente, Django captura la excepción `Http404` y muestra una interfaz de error controlada: *"El sorteo que intenta editar ya no existe"*.                                |
| **FE-02** | **Conflicto de Fecha Duplicada:** En el paso 6, si el administrador cambia la fecha a una que **ya posee** otro número ganador asignado, el formulario invalida la acción y muestra el error de unicidad: *"No se puede actualizar. Ya existe un sorteo registrado para esa fecha"*. |

### Postcondiciones

El registro se actualiza de manera persistente. Los usuarios finales verán los cambios reflejados inmediatamente en la interfaz pública (CU-02).

### Reglas de Negocio

- **RN-01 y RN-02 (Persistentes):** Se heredan las validaciones de formato numérico y unicidad por fecha en la validación del backend de Django.

### Prioridad

Alta (Esencial para la gestión y corrección de datos).

### Frecuencia de Uso

Baja (Operación correctiva eventual).

### Casos Relacionados

- **CU-02** (Consultar Números Ganadores / Listar)
