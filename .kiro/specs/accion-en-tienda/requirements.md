# Requirements Document

## Introduction

El analizador de frescura ya identifica el producto, su etapa de madurez y su nutrición. Esta funcionalidad agrega la **acción recomendada en tienda** para el personal de frutas y verduras, según la política POL-FRV-001 (`negocio/politica-acciones-tienda.md`), incluida la **revisión humana** cuando el análisis no es concluyente.

## Glossary

- **Analizador**: el servicio que recibe la foto y responde el análisis (`app/frescura`).
- **Lectura**: lo que devuelve el modelo de visión: producto, índice de madurez, manchas, defectos y confianza.
- **Acción**: una de Mantener, Priorizar, Rebajar, Transformar, Donar, Retirar o Revisar.
- **Confianza**: valor de 0 a 1 que indica qué tan seguro está el modelo de su lectura.

## Requirements

### Requirement 1: Revisión humana

**User Story:** Como jefe de sección, quiero que los análisis dudosos queden marcados para revisión, para no aplicar una acción equivocada.

#### Acceptance Criteria

1. WHEN la confianza de la Lectura es menor a 0,70, THE Analizador SHALL recomendar la acción Revisar.
2. WHEN el producto no se reconoce, THE Analizador SHALL recomendar la acción Revisar.
3. WHEN la acción es Revisar, THE Analizador SHALL indicar que requiere confirmación del jefe de sección.

### Requirement 2: Productos con moho

**User Story:** Como auxiliar de frutas y verduras, quiero saber cuándo un producto debe descartarse, para no venderlo, transformarlo ni donarlo.

#### Acceptance Criteria

1. WHEN la Lectura incluye el defecto moho y la confianza es de 0,70 o más, THE Analizador SHALL recomendar la acción Retirar, sin importar la etapa.

### Requirement 3: Acción según la etapa

**User Story:** Como auxiliar de frutas y verduras, quiero una acción clara para cada producto, para que todas las tiendas decidan igual.

#### Acceptance Criteria

1. WHEN la etapa es verde o pintón, THE Analizador SHALL recomendar la acción Mantener.
2. WHEN la etapa es maduro, THE Analizador SHALL recomendar la acción Priorizar.
3. WHEN la etapa es sobremaduro, las manchas cubren menos del 30% y no hay zonas hundidas, THE Analizador SHALL recomendar la acción Rebajar.
4. WHEN la etapa es sobremaduro y las manchas cubren del 30% al 59%, o hay zonas hundidas, THE Analizador SHALL recomendar la acción Transformar.
5. WHEN la etapa es sobremaduro y las manchas cubren el 60% o más, THE Analizador SHALL recomendar la acción Donar.
6. THE Analizador SHALL aplicar las reglas de los requisitos 1, 2 y 3 en ese orden, y usar la primera que se cumpla.

### Requirement 4: Mensaje para el personal

**User Story:** Como auxiliar de frutas y verduras, quiero un texto corto que explique qué hacer, para aplicarlo sin consultar la política.

#### Acceptance Criteria

1. THE Analizador SHALL incluir en cada acción un mensaje en español de una sola frase.
2. WHEN la acción es Transformar, THE Analizador SHALL indicar en el mensaje el destino del producto según el catálogo (por ejemplo, "jugos o pulpa" para el mango).
3. WHEN la acción es Donar, THE Analizador SHALL indicar que requiere confirmación del jefe de sección.

### Requirement 5: Respuesta de la API

**User Story:** Como desarrollador de la app, quiero la acción dentro de la respuesta del análisis, para mostrarla sin otra llamada.

#### Acceptance Criteria

1. WHEN se analiza una foto, THE Analizador SHALL responder un campo `accion` con `tipo`, `mensaje` y `requiere_confirmacion`.
2. THE Analizador SHALL mantener sin cambios los demás campos de la respuesta actual.
