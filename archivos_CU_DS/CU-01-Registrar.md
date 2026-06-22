## Caso de Uso 1: Registrar Número Ganador (Módulo de Gestión Customizado)

### Identificador

CU-01

### Objetivo

Permitir al Administrador de la Aplicación ingresar un nuevo número de lotería ganador y su fecha correspondiente a través del **Dashboard de control personalizado**, manteniendo la consistencia visual y de experiencia de usuario del sitio web.

### Actores

- **Actor Principal:** Administrador de la Aplicación (Usuario del negocio con un rol de gestión asignado. Interactúa exclusivamente a través del *frontend* personalizado; **no tiene acceso ni utiliza el `/admin` nativo de Django**).

- **Actores Secundarios:** Ninguno

### Disparador

El administrador hace clic en el botón "Nuevo Registro" dentro del menú lateral del Dashboard de gestión personalizado.

### Precondiciones

1. El Administrador debe haber iniciado sesión a través del formulario de *Login* propio y personalizado de la aplicación web.

2. La sesión del usuario debe contar con los permisos y roles de edición de datos (configurados mediante el sistema de usuarios de Django, pero consumidos desde las vistas del cliente).

3. El entorno web y la base de datos deben estar operativos.

### Flujo Principal

1. El Administrador accede a la sección de gestión de sorteos dentro del Dashboard adaptado.

2. El sistema (mediante una vista de Django y un *template* personalizado) renderiza un formulario web moderno que incluye los campos: *Número Ganador* y *Fecha del Sorteo*.

3. El Administrador ingresa el número premiado y selecciona la fecha mediante un componente gráfico de calendario (*datepicker* integrado en la UI).

4. El Administrador hace clic en el botón "Guardar Sorteo".

5. El sistema procesa la solicitud a través de una clase de formulario de Django (`forms.Form` o `ModelForm` customizado) para validar los datos.

6. El sistema almacena el registro de manera persistente en la base de datos a través del Modelo de Django.

7. El sistema redirige al Administrador al listado interno de control del Dashboard y muestra una notificación emergente estilizada (ej. un *Toast* o alerta CSS moderna) con el mensaje: *"Número ganador registrado exitosamente"*.

### Flujos Alternativos

| **ID**    | **Descripción**                                                                                                                                                                                                                         |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **FA-01** | **Cancelar Registro:** En el paso 3, el administrador decide no continuar y presiona el botón "Cancelar" diseñado en el formulario. El sistema interrumpe el proceso, no guarda datos y lo regresa al listado de control del Dashboard. |

### Flujos de Excepción

| **ID**    | **Descripción**                                                                                                                                                                                                                                                                                                                                     |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **FE-01** | **Error de Validación en Frontend/Backend:** En el paso 5, si el formulario customizado detecta que el número no cumple las condiciones o la fecha es inválida, Django recarga la vista del formulario resaltando los campos en rojo mediante clases CSS personalizadas y muestra el mensaje de error específico al lado del campo correspondiente. |
| **FE-02** | **Registro Duplicado para la Fecha:** En el paso 5, si la lógica del formulario/modelo detecta que ya existe un sorteo para esa fecha, se detiene la inserción y la interfaz propia despliega una alerta moderna: *"Ya existe un número ganador registrado para la fecha seleccionada"*.                                                            |

### Postcondiciones

El nuevo número ganador queda almacenado en la base de datos y se actualiza de manera inmediata tanto en el listado de control del Dashboard (vista privada) como en el listado público de la página principal para los visitantes (CU-02).

### Reglas de Negocio

- **RN-01 (Formato numérico):** La validación del formulario personalizado (`clean_field` en Django) debe asegurar que el número ganador contenga únicamente dígitos enteros válidos según el formato de la lotería.

- **RN-02 (Unicidad temporal):** Se restringe mediante lógica del modelo o del formulario la existencia de más de un número ganador para una misma fecha.

### Prioridad

Alta

### Frecuencia de Uso

Media (Acorde a la realización de cada sorteo).

### Casos Relacionados

- **CU-02** (Consultar Números Ganadores)
