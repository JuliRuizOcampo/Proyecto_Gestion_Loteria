## Caso de Uso 2: Consultar Números Ganadores (Listar Números de Lotería)

### Identificador

CU-02

### Objetivo

Permitir a los usuarios finales y administradores visualizar, paginar y filtrar el histórico de números de lotería ganadores a través de una interfaz web pública, moderna y adaptable.

### Actores

- **Actor Principal:** Usuario General / Visitante

- **Actores Secundarios:** Ninguno (Operación de acceso público)

### Disparador

El usuario ingresa a la página de inicio o a la sección de "Historial de Sorteos" del sitio web.

### Precondiciones

El sistema debe estar en línea y la base de datos de Django configurada correctamente. No se requiere autenticación ni tokens de sesión.

### Flujo Principal (Visualización de la Lista)

1. El usuario navega hacia la URL de resultados del sitio web.

2. El sistema intercepta la solicitud a través de la vista encargada del listado (`SorteoListView`).

3. La vista solicita al Modelo de Django el listado completo de sorteos ordenados cronológicamente de forma descendente.

4. El sistema recupera los registros desde la base de datos.

5. La vista inyecta los datos en el *Template* HTML personalizado y procesa la estructura gráfica responsiva.

6. El sistema renderiza la página y presenta al usuario la tabla estilizada con los números ganadores y sus respectivas fechas.

### Flujos Alternativos

| **ID**    | **Descripción**                                                                                                                                                                                                                                                                                                                                      |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **FA-01** | **Filtrar por Fecha:** En el paso 2, el usuario interactúa con un componente de calendario (*datepicker*), selecciona una fecha específica y presiona el botón "Filtrar". La vista de Django procesa el parámetro `GET`, aplica un filtro (`.filter(fecha=...)`) sobre el modelo y refresca la pantalla mostrando únicamente el sorteo de esa fecha. |
| **FA-02** | **Navegación Paginada:** Si el histórico supera los 10 registros, la vista segmenta los resultados. El usuario hace clic en los botones de navegación ("Siguiente" / "Anterior") y el sistema recarga la sección enviando el parámetro de página correspondiente.                                                                                    |

### Flujos de Excepción

| **ID**    | **Descripción**                                                                                                                                                                                                                                                                                                                                                  |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **FE-01** | **Base de Datos Vacía o Filtro sin Coincidencias:** En los pasos 4 (Flujo Principal) o FA-01, si el conjunto de datos (*QuerySet*) devuelto por Django está vacío, la vista carga el template reemplazando la tabla por un contenedor dinámico con el mensaje informativo: *"No se encontraron números ganadores registrados para los criterios seleccionados"*. |

### Postcondiciones

El usuario visualiza la información solicitada de manera clara. El estado de la base de datos permanece inalterado (operación de solo lectura / idempotente).

### Reglas de Negocio

- **RN-03 (Acceso Irrestricto):** Al ser una consulta pública de interés general, no se aplican políticas de *middleware* de autenticación ni restricciones de permisos.

- **RN-04 (Criterio de Ordenamiento por Defecto):** El listado inicial siempre debe priorizar la inmediatez de la información, ordenando los registros de la fecha más reciente a la más antigua.

### Prioridad

Alta

### Frecuencia de Uso

Alta

### Casos Relacionados

- **CU-01** (Registrar Número Ganador)
