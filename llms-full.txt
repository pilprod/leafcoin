# Leafcoin — A concept for verifiable agriculture

Canonical presentation: [Leafcoin](https://leafcoin.org/).

This Markdown preserves the current homepage’s concept, including all expandable architecture details, the proposed roadmap, archival prototype scope and displayed image captions. [Structured relationships](https://leafcoin.org/concept.jsonld) identify the concept, prototype, repositories and images separately.

Agrotech / Personal R&D

## Real crops. Verifiable data.

Leafcoin is a personal agrotech R&D concept by Ilya Papou, exploring aeroponics, IoT telemetry, ML-assisted calibration and verifiable production records.

An exploration of how production data could support a more transparent agricultural ecosystem.

[Explore the architecture](https://leafcoin.org/#architecture)

[View the prototype](https://leafcoin.org/#prototype)

- **Status**: Concept & personal R&D
- **Foundation**: Home Aeroponics lab

![AI-generated concept illustration for Leafcoin (leafcoin.org): a compact home aeroponics lab with plants, grow lighting, a nutrient reservoir and a controller.](https://leafcoin.org/assets/images/hero-home-lab.jpg)

Home aeroponics [AI-generated concept illustration](https://leafcoin.org/docs/generated-illustrations.md#hero)

A proposed ecosystem

- Aeroponics
- IoT sensing
- ML calibration
- Ledger records
- Product passports

## 01 / Concept

Real production. Useful evidence.

### Start with the farm.

Before a digital asset can represent anything meaningful, the underlying production needs to be observable. Leafcoin starts with growing conditions, crop records and the quality of the data.

![AI-generated concept illustration of an aeroponic growing module with leafy plants, a mist chamber, reservoir, pump and sensors.](https://leafcoin.org/assets/images/section-concept.jpg)

[AI-generated concept illustration](https://leafcoin.org/docs/generated-illustrations.md#concept) Cultivation and observable growing conditions.

#### Grow with better visibility

The proposed monitoring layer would bring temperature, humidity, light, pH and nutrient readings together to help operators assess growing conditions.

#### Trace every batch

A proposed product passport would connect seed origin, growing conditions, crop cycles and harvest records, with access through a QR code.

#### Verify the record

The proposed verification layer would anchor report fingerprints on a ledger so readers could check whether a recorded report has changed.

Leafcoin is presented here as a concept and personal R&D project. The public lab materials document historical prototypes. The architecture and roadmap describe proposed work; implementation status beyond those materials is not established here.

## 02 / Architecture

From a reading to a verifiable record.

### A data layer before a token layer.

The proposed architecture separates data collection, off-chain storage and ledger-based integrity checks. Raw telemetry would remain off-chain, while the ledger would hold report hashes.

![AI-generated concept illustration linking crop sensors, a gateway, off-chain storage, ledger modules and a batch passport.](https://leafcoin.org/assets/images/section-architecture.jpg)

[AI-generated concept illustration](https://leafcoin.org/docs/generated-illustrations.md#architecture) A proposed path from measurements to verifiable records.

1. **Measure** — Farm sensors
2. **Validate** — Quality checks
3. **Store** — Off-chain data
4. **Verify** — Report hashes
5. **Use** — ML & passports

#### Collection & data quality · IoT

The proposed collection layer would timestamp readings and transport them through MQTT, retaining crop-cycle and device context. Data-quality checks would flag missing samples, outliers and calibration issues before readings are used in reports or model evaluation.

#### Storage & integrity · Ledger

The proposed design would store raw telemetry off-chain in an access-controlled repository and record report hashes on a ledger. A matching hash can indicate that a report has not changed since it was recorded; it does not establish the accuracy of the underlying sensor readings.

Besu with QBFT consensus is being considered as an option for a permissioned EVM network. Network membership, validator governance, operation and verification design would require evaluation.

Permissioning and consensus do not by themselves guarantee transaction confidentiality. Data visibility, access controls and any confidentiality mechanism would require separate design and validation.

#### Recommendations & traceability · ML / QR

The research direction includes evaluating ML models for forecasts and cultivation recommendations using validated data, with operator review before any cultivation changes. Dataset and model versioning would support investigation of recommendations.

A proposed batch passport would bring together seed origin, growing conditions, nutrient records, crop-cycle dates and harvest history. Which records could be shared, and with whom, would depend on access rules defined and validated for the implementation.

#### Future digital-asset integrations · Research

The concept explores whether verifiable production records could support asset-linked services. Token design, asset rights, custody, valuation and redemption are research questions.

The feasibility of any financial integration would require evaluation of applicable rules, responsibilities and any necessary authorisations. Partnership, investment and approval status are not established by the materials presented here.

## 03 / ML calibration

Observe. Adjust. Repeat.

### Learn from each growing cycle.

A proposed research loop would use repeated cultivation iterations to evaluate irrigation schedules and nutrient-solution composition against observed plant responses.

![AI-generated concept illustration of three comparable cultivation experiments with irrigation equipment, nutrient dosing reservoirs and sensing probes.](https://leafcoin.org/assets/images/section-calibration.jpg)

[AI-generated concept illustration](https://leafcoin.org/docs/generated-illustrations.md#calibration) Repeated experiments for irrigation and nutrient-solution research.

#### Record each iteration

Each experiment would record the solution recipe, dosing, irrigation intervals and duration, pH, electrical conductivity, water temperature, growing conditions and crop stage. Plant observations and crop outcomes would provide context for comparison.

#### Evaluate bounded adjustments

ML models could be evaluated for suggesting small changes to irrigation settings and solution composition. An operator would review each proposal against predefined experimental limits before a new iteration.

#### Repeat and compare

Successive iterations would compare predictions with observed responses under comparable conditions. Later iterations would be reserved for validation, with recipe, parameter and model versions retained so results could be traced.

This is a proposed research direction. Repeated measurements and experiments would be needed to establish model quality and useful operating limits. Sensor calibration would remain a separate requirement.

## 04 / Roadmap

Build in stages. Validate each step.

### A staged path from lab to ecosystem.

A proposed research sequence. Each stage would require validation; no completion status or launch dates are specified here.

![AI-generated concept illustration of four connected research stages combining crops, sensing, evaluation and additional growing modules.](https://leafcoin.org/assets/images/section-roadmap.jpg)

[AI-generated concept illustration](https://leafcoin.org/docs/generated-illustrations.md#roadmap) A proposed research sequence, with validation at each stage.

#### 01 — Telemetry MVP

Connect a pilot farm, validate readings and build monitoring views. Test report fingerprints and a basic batch passport.

Validate: sensor coverage, data quality and record verification.

#### 02 — Operator-reviewed ML

Evaluate forecasts and recommendations against recorded crop outcomes. Keep operators in control of cultivation changes.

Validate: model quality, reproducibility and operator review.

#### 03 — Regulated integrations

Research asset-linked services and partner requirements. Define legal responsibilities and user rights before building financial flows.

Validate: feasibility, partner scope and the regulatory path.

#### 04 — Additional farms & crops

Extend the system only after the pilot is useful and repeatable. Adapt monitoring and models to new sites and crops.

Validate: repeatable operations and sustainable unit economics.

## 05 / Prototype

The work behind the idea.

### Rooted in hands-on research.

The concept grew out of Home Aeroponics, a personal IoT and automation lab. Its public repositories preserve parts of that work.

LAB ARCHIVE / 9 IMAGES

1 / 9

### Historical lab images

![Development boards, sensors, wiring and soldering tools during prototyping.](https://leafcoin.org/assets/images/electronics-workbench.jpg)

#### Electronics workbench

Development boards, sensors, wiring and soldering tools during prototyping.

*AI-retouched background / identifying areas.*

[Published source](https://github.com/pilprod/aeroponics-iot-control/blob/9057bcd017df480416863801cf507760f6c2b6da/docs/images/electronics-workbench.jpg)

[Full image](https://leafcoin.org/assets/images/electronics-workbench.jpg).

![Breadboard-mounted sensor modules and jumper wiring during controller prototyping.](https://leafcoin.org/assets/images/breadboard-prototype-privacy-20260909.jpg)

#### Breadboard prototype

Breadboard-mounted sensor modules and jumper wiring during controller prototyping.

*Patterned wallpaper replaced with a neutral wall using AI assistance for privacy.*

[Published source](https://github.com/pilprod/aeroponics-iot-control/blob/83f7e6a2a1ab138aa541010033e774c1c7a1783b/docs/images/breadboard-prototype-privacy-20260909.jpg)

[Full image](https://leafcoin.org/assets/images/breadboard-prototype-privacy-20260909.jpg).

![A commercial power shield integrated into the electronics assembly.](https://leafcoin.org/assets/images/power-shield.jpg)

#### Power shield

A commercial power shield integrated into the electronics assembly.

*AI-retouched background / identifying areas.*

[Published source](https://github.com/pilprod/aeroponics-iot-control/blob/9057bcd017df480416863801cf507760f6c2b6da/docs/images/power-shield.jpg)

[Full image](https://leafcoin.org/assets/images/power-shield.jpg).

![Suspended fixtures, ventilation equipment and wiring inside the enclosure.](https://leafcoin.org/assets/images/lighting-ventilation.jpg)

#### Lighting and ventilation

Suspended fixtures, ventilation equipment and wiring inside the enclosure.

*AI-retouched background / identifying areas.*

[Published source](https://github.com/pilprod/aeroponics-iot-control/blob/9057bcd017df480416863801cf507760f6c2b6da/docs/images/lighting-ventilation.jpg)

[Full image](https://leafcoin.org/assets/images/lighting-ventilation.jpg).

![Climate and water measurements, lighting controls and device states.](https://leafcoin.org/assets/images/home-assistant-dashboard-privacy-20260909.jpg)

#### Home Assistant dashboard

Climate and water measurements, lighting controls and device states.

*Patterned wallpaper replaced with a neutral wall using AI assistance for privacy.*

[Published source](https://github.com/pilprod/aeroponics-iot-control/blob/994f20e27f54e8f3659731089f2d0208cead39c1/docs/images/home-assistant-dashboard-privacy-20260909.jpg)

[Full image](https://leafcoin.org/assets/images/home-assistant-dashboard-privacy-20260909.jpg).

![Camera placement within the experimental installation.](https://leafcoin.org/assets/images/enclosure-camera.jpg)

#### Enclosure camera

Camera placement within the experimental installation.

*AI-retouched background / identifying areas.*

[Published source](https://github.com/pilprod/aeroponics-iot-control/blob/9057bcd017df480416863801cf507760f6c2b6da/docs/images/enclosure-camera.jpg)

[Full image](https://leafcoin.org/assets/images/enclosure-camera.jpg).

![Reservoirs, dosing pumps, valves, tubing and circulation plumbing.](https://leafcoin.org/assets/images/water-system.jpg)

#### Water system

Reservoirs, dosing pumps, valves, tubing and circulation plumbing.

*AI-retouched background / identifying areas.*

[Published source](https://github.com/pilprod/aeroponics-iot-control/blob/9057bcd017df480416863801cf507760f6c2b6da/docs/images/water-system.jpg)

[Full image](https://leafcoin.org/assets/images/water-system.jpg).

![Original component-connection drawing from system design.](https://leafcoin.org/assets/images/wiring-diagram.jpg)

#### Wiring and I/O diagram

Original component-connection drawing from system design.

[Published source](https://github.com/pilprod/aeroponics-iot-control/blob/9057bcd017df480416863801cf507760f6c2b6da/docs/images/wiring-diagram.jpg)

[Full image](https://leafcoin.org/assets/images/wiring-diagram.jpg).

![Suspended roots and internal tubing in the chamber.](https://leafcoin.org/assets/images/root-chamber.webp)

#### Root chamber

Suspended roots and internal tubing in the chamber.

[Published source](https://github.com/pilprod/aeroponics-iot-control/blob/7c0c97df694f764d4c7354408b18146c63ca5864/docs/images/root-chamber.jpg)

[Full image](https://leafcoin.org/assets/images/root-chamber-original-1536.jpg).

Swipe or scroll to browse. Focus the gallery to use Left/Right arrows, Home or End.

Control layer

#### [Aeroponics IoT control](https://github.com/pilprod/aeroponics-iot-control)

Historical Python and MQTT controller examples, with monitoring and integration context.

GitHub

Device layer

#### [Aeroponics sensor firmware](https://github.com/pilprod/aeroponics-sensor-firmware)

Archived Arduino experiments for sensing, telemetry and relay control.

GitHub

Physical prototype

#### [Home Aeroponics lab](https://papou.work/portfolio.html#home)

Photographs and project context from the broader historical installation.

Portfolio

These archival materials provide context for the personal lab work. They do not establish the implementation status of the wider Leafcoin concept. Build, runtime and hardware limitations are documented in the repositories.

Concept creator

#### Ilya Papou

Platform / SRE engineer · Personal R&D

[CV & experience](https://papou.work/)

[Website source](https://github.com/pilprod/leafcoin)

## Site assets and source context

- [Supplied SVG brand mark](https://leafcoin.org/assets/leafcoin_revert.svg)
- [Supplied SVG favicon](https://leafcoin.org/assets/favicon.svg)
- [Supplied touch icon](https://leafcoin.org/assets/ios_ligth_leafcoin.png)
- [IBM Plex font license](https://leafcoin.org/assets/fonts/OFL.txt): SIL Open Font License 1.1.
- [Original Leafcoin presentation](https://old.leafcoin.org/): The source concept context used for the redesign, at the designated archive URL.

The five AI-generated concept illustrations are separate from the historical Home Aeroponics photographs. The photograph captions identify privacy retouching. Use the page’s scope statements and repository documentation when interpreting prototype evidence.

[Generated-illustration prompts and provenance](https://leafcoin.org/docs/generated-illustrations.md): The home-lab hero and four section illustrations are AI-generated concept visuals. The provenance record associates each image with its prompt and the proposed subject it depicts.

## Footer reference

- [Original version](https://old.leafcoin.org/)
