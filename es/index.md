# Leafcoin: Cultivos reales. Datos verificables.

Presentación canónica: [Leafcoin](https://leafcoin.org/es/).

Este Markdown conserva el concepto de la página principal, incluidos todos los detalles desplegables de arquitectura, la hoja de ruta propuesta, el alcance del prototipo histórico y las leyendas de las imágenes. [Relaciones estructuradas](https://leafcoin.org/es/concept.jsonld) identifican por separado el concepto, el prototipo, los repositorios y las imágenes.

Agrotecnología / I+D personal

## Cultivos reales. Datos verificables.

De las raíces a los registros. Descubre Leafcoin, el concepto de I+D agrotecnológica de Ilya Papou que combina aeroponía, IoT, calibración con ML y registros verificables de cultivo.

A partir de un laboratorio doméstico de aeroponía, la investigación explora cómo los datos de cultivo podrían orientar el riego, la calibración de nutrientes y la trazabilidad de los registros.

[Explorar la arquitectura](https://leafcoin.org/es/#architecture)

[Ver el prototipo](https://leafcoin.org/es/#prototype)

- **Estado**: Concepto e I+D personal
- **Base**: Laboratorio Home Aeroponics

![Ilustración conceptual generada con IA para Leafcoin (leafcoin.org): un laboratorio doméstico compacto de aeroponía con plantas, iluminación de cultivo, un depósito de solución nutritiva y un controlador.](https://leafcoin.org/assets/images/hero-home-lab.jpg)

Aeroponía en casa [Ilustración conceptual generada con IA](https://leafcoin.org/docs/generated-illustrations.md#hero)

Un ecosistema propuesto

- Aeroponía
- Sensores IoT
- Calibración con ML
- Registros en el libro mayor
- Pasaportes de producto

## 01 / Concepto

Producción real. Evidencia útil.

### Empezar por el cultivo.

Para que un activo digital represente algo significativo, primero debe poder observarse la producción que lo sustenta. Leafcoin parte de las condiciones de cultivo, sus registros y la calidad de los datos.

![Ilustración conceptual generada con IA de una neblina nutritiva que llega a raíces suspendidas en una cámara aeropónica.](https://leafcoin.org/assets/images/article-nozzle-roots-detail.jpg)

[Ilustración conceptual generada con IA](https://leafcoin.org/docs/generated-illustrations.md#article-nozzle-roots-detail) Aporte de nutrientes a raíces suspendidas.

#### Cultivar con mayor visibilidad

La capa de monitorización propuesta reuniría lecturas de temperatura, humedad, luz, pH y nutrientes para ayudar a evaluar las condiciones de cultivo.

#### Seguir cada lote

Un pasaporte de producto propuesto vincularía el origen de las semillas, las condiciones de cultivo, los ciclos y los registros de cosecha, con acceso mediante un código QR.

#### Verificar el registro

La capa de verificación propuesta registraría huellas digitales de los informes en un libro mayor para comprobar si un informe registrado ha cambiado.

Leafcoin se presenta como un concepto y un proyecto personal de I+D. Los materiales públicos del laboratorio documentan prototipos históricos. La arquitectura y la hoja de ruta describen trabajo propuesto; estos materiales no permiten establecer el estado de implementación más allá de lo documentado.

## 02 / Arquitectura

De una lectura a un registro verificable.

### Primero los datos. Después los tokens.

La arquitectura propuesta separa la recopilación de datos, el almacenamiento fuera de la cadena y la comprobación de integridad mediante un libro mayor. La telemetría sin procesar permanecería fuera de la cadena, mientras que el libro mayor almacenaría hashes de los informes.

![Ilustración conceptual generada con IA que conecta sensores de cultivo, una pasarela, almacenamiento fuera de la cadena, módulos del libro mayor y un pasaporte de lote.](https://leafcoin.org/assets/images/section-architecture.jpg)

[Ilustración conceptual generada con IA](https://leafcoin.org/docs/generated-illustrations.md#architecture) Un recorrido propuesto de las mediciones a los registros verificables.

1. **Medir**: Sensores de cultivo
2. **Validar**: Controles de calidad
3. **Guardar**: Datos fuera de la cadena
4. **Verificar**: Hashes de informes
5. **Utilizar**: ML y pasaportes

#### Recopilación y calidad de datos · IoT

La capa de recopilación propuesta añadiría marcas de tiempo a las lecturas y las transmitiría mediante MQTT, conservando el contexto del dispositivo y del ciclo de cultivo. Los controles de calidad señalarían muestras ausentes, valores atípicos y problemas de calibración antes de utilizar las lecturas en informes o en la evaluación de modelos.

#### Almacenamiento e integridad · Libro mayor

El diseño propuesto almacenaría la telemetría sin procesar fuera de la cadena, en un repositorio con control de acceso, y registraría hashes de los informes en un libro mayor. Un hash coincidente puede indicar que un informe no ha cambiado desde su registro; no demuestra la precisión de las lecturas de los sensores.

Se considera Besu con consenso QBFT como una opción de red EVM con permisos. La participación en la red, la gobernanza de los validadores, la operación y el diseño de la verificación requerirían evaluación.

Los permisos y el consenso no garantizan por sí solos la confidencialidad de las transacciones. La visibilidad de los datos, los controles de acceso y cualquier mecanismo de confidencialidad necesitarían diseño y validación independientes.

#### Recomendaciones y trazabilidad · ML / QR

La línea de investigación incluye evaluar modelos de ML para pronósticos y recomendaciones de cultivo a partir de datos validados, con revisión humana antes de realizar cambios. El versionado de los conjuntos de datos y de los modelos facilitaría el análisis de las recomendaciones.

Un pasaporte de lote propuesto reuniría el origen de las semillas, las condiciones de cultivo, los registros de nutrientes, las fechas de los ciclos y el historial de cosecha. Los registros que podrían compartirse y sus destinatarios dependerían de reglas de acceso definidas y validadas para la implementación.

#### Futuras integraciones de activos digitales · Investigación

El concepto explora si los registros verificables de producción podrían respaldar servicios vinculados a activos. El diseño del token, los derechos sobre los activos, la custodia, la valoración y el reembolso son cuestiones de investigación.

La viabilidad de cualquier integración financiera requeriría evaluar las normas aplicables, las responsabilidades y las autorizaciones necesarias. Los materiales presentados no permiten establecer el estado de las alianzas, inversiones o aprobaciones.

## 03 / Calibración con ML

Observar. Ajustar. Repetir.

### Aprender de cada ciclo de cultivo.

Un ciclo de investigación propuesto utilizaría iteraciones de cultivo repetidas para evaluar los programas de riego y la composición de la solución nutritiva según las respuestas observadas en las plantas.

![Ilustración conceptual generada con IA de tres ensayos de cultivo comparables con equipos de riego, depósitos de dosificación y sondas de medición.](https://leafcoin.org/assets/images/section-calibration.jpg)

[Ilustración conceptual generada con IA](https://leafcoin.org/docs/generated-illustrations.md#calibration) Experimentos repetidos sobre riego y solución nutritiva.

#### Registrar cada iteración

Cada experimento registraría la receta de la solución, la dosificación, los intervalos y la duración del riego, el pH, la conductividad eléctrica, la temperatura del agua, las condiciones y la etapa del cultivo. Las observaciones de las plantas y los resultados aportarían contexto para la comparación.

#### Evaluar ajustes acotados

Se podrían evaluar modelos de ML para sugerir pequeños cambios en los parámetros de riego y la composición de la solución. Una persona revisaría cada propuesta dentro de límites experimentales predefinidos antes de iniciar otra iteración.

#### Repetir y comparar

Las iteraciones sucesivas compararían las predicciones con las respuestas observadas en condiciones comparables. Se reservarían iteraciones posteriores para la validación y se conservarían las versiones de recetas, parámetros y modelos para poder rastrear los resultados.

Esta es una línea de investigación propuesta. Se necesitarían mediciones y experimentos repetidos para establecer la calidad de los modelos y unos límites de operación útiles. La calibración de los sensores seguiría siendo un requisito independiente.

## 04 / Hoja de ruta

Construir por etapas. Validar cada paso.

### Un camino por etapas del laboratorio al ecosistema.

Una secuencia de investigación propuesta. Cada etapa requeriría validación; aquí no se indican estados de finalización ni fechas de lanzamiento.

![Ilustración conceptual generada con IA de cuatro etapas de investigación conectadas que combinan cultivos, sensores, evaluación y módulos adicionales de cultivo.](https://leafcoin.org/assets/images/section-hoja de ruta.jpg)

[Ilustración conceptual generada con IA](https://leafcoin.org/docs/generated-illustrations.md#hoja de ruta) Una secuencia de investigación propuesta, con validación en cada etapa.

#### 01: MVP de telemetría

Conectar un cultivo piloto, validar las lecturas y crear vistas de monitorización. Probar las huellas digitales de los informes y un pasaporte de lote básico.

Validar: cobertura de sensores, calidad de datos y verificación de registros.

#### 02: ML con revisión humana

Evaluar pronósticos y recomendaciones frente a los resultados de cultivo registrados. Mantener el control humano de los cambios de cultivo.

Validar: calidad del modelo, reproducibilidad y revisión humana.

#### 03: Integraciones reguladas

Investigar servicios vinculados a activos y requisitos de los socios. Definir responsabilidades legales y derechos de los usuarios antes de crear flujos financieros.

Validar: viabilidad, alcance de los socios y marco regulatorio.

#### 04: Más instalaciones y cultivos

Ampliar el sistema solo cuando el piloto sea útil y repetible. Adaptar la monitorización y los modelos a nuevas instalaciones y cultivos.

Validar: operaciones repetibles y viabilidad económica por unidad.

## 05 / Prototipo

El trabajo detrás de la idea.

### Una idea nacida de la experimentación.

El concepto nació de Home Aeroponics, un laboratorio personal de IoT y automatización. Sus repositorios públicos conservan parte de ese trabajo.

ARCHIVO DEL LABORATORIO / 9 IMÁGENES

1 / 9

### Imágenes históricas del laboratorio

![Placas de desarrollo, sensores, cableado y herramientas de soldadura durante la creación de prototipos.](https://leafcoin.org/assets/images/electronics-workbench.jpg)

#### Banco de electrónica

Placas de desarrollo, sensores, cableado y herramientas de soldadura durante la creación de prototipos.

*Fondo y zonas identificativas retocados con IA.*

[Fuente publicada](https://github.com/pilprod/aeroponics-iot-control/blob/9057bcd017df480416863801cf507760f6c2b6da/docs/images/electronics-workbench.jpg)

[Imagen completa](https://leafcoin.org/assets/images/electronics-workbench.jpg).

![Módulos de sensores y cables de conexión montados en una protoboard durante el desarrollo del controlador.](https://leafcoin.org/assets/images/breadboard-prototype-privacy-20260909.jpg)

#### Prototipo en protoboard

Módulos de sensores y cables de conexión montados en una protoboard durante el desarrollo del controlador.

*Papel pintado sustituido por una pared neutra con ayuda de IA para proteger la privacidad.*

[Fuente publicada](https://github.com/pilprod/aeroponics-iot-control/blob/83f7e6a2a1ab138aa541010033e774c1c7a1783b/docs/images/breadboard-prototype-privacy-20260909.jpg)

[Imagen completa](https://leafcoin.org/assets/images/breadboard-prototype-privacy-20260909.jpg).

![Un módulo de potencia comercial integrado en el conjunto electrónico.](https://leafcoin.org/assets/images/power-shield.jpg)

#### Módulo de potencia

Un módulo de potencia comercial integrado en el conjunto electrónico.

*Fondo y zonas identificativas retocados con IA.*

[Fuente publicada](https://github.com/pilprod/aeroponics-iot-control/blob/9057bcd017df480416863801cf507760f6c2b6da/docs/images/power-shield.jpg)

[Imagen completa](https://leafcoin.org/assets/images/power-shield.jpg).

![Luminarias suspendidas, equipos de ventilación y cableado dentro del recinto.](https://leafcoin.org/assets/images/lighting-ventilation.jpg)

#### Iluminación y ventilación

Luminarias suspendidas, equipos de ventilación y cableado dentro del recinto.

*Fondo y zonas identificativas retocados con IA.*

[Fuente publicada](https://github.com/pilprod/aeroponics-iot-control/blob/9057bcd017df480416863801cf507760f6c2b6da/docs/images/lighting-ventilation.jpg)

[Imagen completa](https://leafcoin.org/assets/images/lighting-ventilation.jpg).

![Mediciones del clima y del agua, controles de iluminación y estados de los dispositivos.](https://leafcoin.org/assets/images/home-assistant-dashboard-privacy-20260909.jpg)

#### Panel de Home Assistant

Mediciones del clima y del agua, controles de iluminación y estados de los dispositivos.

*Papel pintado sustituido por una pared neutra con ayuda de IA para proteger la privacidad.*

[Fuente publicada](https://github.com/pilprod/aeroponics-iot-control/blob/994f20e27f54e8f3659731089f2d0208cead39c1/docs/images/home-assistant-dashboard-privacy-20260909.jpg)

[Imagen completa](https://leafcoin.org/assets/images/home-assistant-dashboard-privacy-20260909.jpg).

![Ubicación de la cámara dentro de la instalación experimental.](https://leafcoin.org/assets/images/enclosure-camera.jpg)

#### Cámara del recinto

Ubicación de la cámara dentro de la instalación experimental.

*Fondo y zonas identificativas retocados con IA.*

[Fuente publicada](https://github.com/pilprod/aeroponics-iot-control/blob/9057bcd017df480416863801cf507760f6c2b6da/docs/images/enclosure-camera.jpg)

[Imagen completa](https://leafcoin.org/assets/images/enclosure-camera.jpg).

![Depósitos, bombas dosificadoras, válvulas, tubos y circuito de circulación.](https://leafcoin.org/assets/images/water-system.jpg)

#### Sistema de agua

Depósitos, bombas dosificadoras, válvulas, tubos y circuito de circulación.

*Fondo y zonas identificativas retocados con IA.*

[Fuente publicada](https://github.com/pilprod/aeroponics-iot-control/blob/9057bcd017df480416863801cf507760f6c2b6da/docs/images/water-system.jpg)

[Imagen completa](https://leafcoin.org/assets/images/water-system.jpg).

![Dibujo original de conexión de los componentes realizado durante el diseño del sistema.](https://leafcoin.org/assets/images/wiring-diagram.jpg)

#### Esquema de cableado y E/S

Dibujo original de conexión de los componentes realizado durante el diseño del sistema.

[Fuente publicada](https://github.com/pilprod/aeroponics-iot-control/blob/9057bcd017df480416863801cf507760f6c2b6da/docs/images/wiring-diagram.jpg)

[Imagen completa](https://leafcoin.org/assets/images/wiring-diagram.jpg).

![Raíces suspendidas y tubos dentro de la cámara.](https://leafcoin.org/assets/images/root-chamber.webp)

#### Cámara de raíces

Raíces suspendidas y tubos dentro de la cámara.

[Fuente publicada](https://github.com/pilprod/aeroponics-iot-control/blob/7c0c97df694f764d4c7354408b18146c63ca5864/docs/images/root-chamber.jpg)

[Imagen completa](https://leafcoin.org/assets/images/root-chamber-original-1536.jpg).

Desliza o desplázate para ver las imágenes. Con la galería enfocada, utiliza las flechas izquierda y derecha, Inicio o Fin.

Capa de control

#### [Control IoT de aeroponía](https://github.com/pilprod/aeroponics-iot-control)

Ejemplos históricos de controladores con Python y MQTT, con contexto de monitorización e integración.

GitHub

Capa de dispositivos

#### [Firmware de sensores de aeroponía](https://github.com/pilprod/aeroponics-sensor-firmware)

Experimentos archivados de Arduino para sensores, telemetría y control de relés.

GitHub

Prototipo físico

#### [Laboratorio Home Aeroponics](https://papou.work/portfolio.html#home)

Fotografías y contexto del proyecto de la instalación histórica.

Portafolio

Estos materiales de archivo aportan contexto al trabajo del laboratorio personal. No permiten establecer el estado de implementación del concepto Leafcoin en su conjunto. Los repositorios documentan las limitaciones de compilación, ejecución y hardware.

Creador del concepto

#### Ilya Papou

Ingeniero Platform / SRE · I+D personal

[CV y experiencia](https://papou.work/)

[Código del sitio](https://github.com/pilprod/leafcoin)

## 06 / Artículos

Comprender las raíces. Evaluar el sistema.

### ¿Qué ocurre debajo de las hojas?

Descubre cómo funciona la aeroponía, en qué aspectos puede mejorar otros métodos de cultivo y qué hace fiable a un sistema. Cuatro guías con fuentes de investigación y ventajas e inconvenientes prácticos.

01 / Fundamentos

#### [¿Qué es la aeroponía? Cómo crecen las raíces sin suelo](https://leafcoin.org/es/articles/what-is-aeroponics.html)

Descubre cómo la aeroponía alimenta raíces suspendidas con una neblina nutritiva, qué contiene un sistema y en qué se diferencia de la hidroponía y la agricultura vertical.

02 / Comparación

#### [Aeroponía e hidroponía: ventajas, límites y cómo compararlas](https://leafcoin.org/es/articles/aeroponics-vs-hydroponics.html)

Compara la aeroponía con NFT y el cultivo en agua profunda: oxígeno en las raíces, uso de agua, mantenimiento, respuesta ante fallos y resultados de los ensayos.

03 / Control y aprendizaje

#### [Por qué es difícil gestionar un sistema aeropónico y cómo podría ayudar el ML](https://leafcoin.org/es/articles/aeroponic-system-control.html)

Comprende los fallos de las boquillas, los tiempos de riego, el pH y la CE, la deriva de los sensores y un ciclo de ML propuesto para mejorar las decisiones de riego y nutrientes mediante ensayos.

04 / Agricultura del futuro

#### [Cómo podría cambiar la aeroponía la agricultura y qué debe ocurrir primero](https://leafcoin.org/es/articles/future-of-aeroponics.html)

Explora la aeroponía en la propagación, el cultivo controlado y la agricultura basada en datos, con límites realistas de energía, mantenimiento, costes y escala.

[Explorar todos los artículos de aeroponía](https://leafcoin.org/es/articles/index.html)

## Recursos del sitio y contexto de las fuentes

- [Logotipo SVG proporcionado](https://leafcoin.org/assets/leafcoin_revert.svg)
- [Favicon SVG proporcionado](https://leafcoin.org/assets/favicon.svg)
- [Icono táctil proporcionado](https://leafcoin.org/assets/ios_ligth_leafcoin.png)
- [Licencia de la fuente IBM Plex](https://leafcoin.org/assets/fonts/OFL.txt): SIL Open Font License 1.1.
- [Presentación original de Leafcoin](https://old.leafcoin.org/): Contexto original utilizado en el rediseño, disponible en la dirección de archivo indicada.

Las ilustraciones conceptuales generadas con IA se distinguen de las fotografías históricas de Home Aeroponics. Las leyendas identifican los retoques de privacidad. Consulta las declaraciones de alcance y la documentación de los repositorios al interpretar la evidencia del prototipo.

[Instrucciones y procedencia de las ilustraciones generadas](https://leafcoin.org/docs/generated-illustrations.md): La imagen del laboratorio doméstico y las cuatro ilustraciones de sección son visualizaciones conceptuales generadas con IA. El registro de procedencia vincula cada imagen con sus instrucciones y el tema propuesto que representa.

## Referencia del pie de página

- [Versión original](https://old.leafcoin.org/)
