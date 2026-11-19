# Procedencia del snapshot orbital

## Origen

Snapshot de **CelesTrak** en seis grupos públicos, descargado el **2026-11-17** y
con referencia temporal de simulación **2026-11-16T12:05:12Z**.

| Grupo | Registros |
|---|---|
| Starlink | 11 185 |
| OneWeb | 651 |
| Amazon Leo | 391 |
| Galileo (UE) | 32 |
| GPS (EE. UU.) | 32 |
| Estaciones | 17 |
| **Total** | **12 308** |

## Qué verifica el repositorio

`python tools/verificar_fuentes.py` comprueba, contra
`app/content/orbita.sources.json`:

- que el manifiesto declare los seis grupos y las fechas de descarga y referencia;
- que cada grupo tenga recuento positivo, SHA-256 con formato válido y URL de
  origen en `https`;
- que la suma coincida con los **12 308** registros que muestra la aplicación.

La integración continua ejecuta esta comprobación en cada push.

## Qué no verifica

- **No descarga** los elementos de nuevo ni valida los TLE contra CelesTrak: un
  snapshot fijo no se revalida solo.
- **No recompone** el HTML distribuible a partir de fuentes separadas: el motor
  SGP4 y los datos viajan dentro de `app/index.html`.
- **No comprueba** la posición propagada contra un efemérides independiente.

## Límites científicos

- Snapshot fijo: la precisión depende de los elementos y de su distancia temporal.
- Los 17 registros de estaciones no son 17 estaciones espaciales distintas.
- El relieve es una textura desplazada con exageración, no un DEM calibrado.
- La atmósfera no es un modelo físico validado; la Luna tiene distancia visual
  comprimida y orientación ilustrativa.
- Un paso geométrico no implica visibilidad óptica, conectividad ni cobertura.

## Pendiente declarado

Separar el motor y los datos del HTML distribuible, con empaquetado reproducible,
sigue pendiente: requiere extraer el código del artefacto de 16.7 MB y no se hizo
en esta corrección para no sustituir el motor existente por uno nuevo.
