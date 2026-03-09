# SWMM Input File Format

Formal Grammar Reference in BNF Notation

*Version 5.2 | All sections covered*

## 1. Introduction

This document provides a formal grammar for the EPA SWMM 5 input file
format (.inp) using Backus-Naur Form (BNF) notation. It is intended as a
reference for parser implementers, geodatabase schema designers, and
tool developers working within the SWMM ecosystem.

Each section of the .inp file is described with its BNF grammar,
field-level definitions, and notes on optional versus required content.
The grammar reflects the full SWMM 5.2 specification.

### 1.1 BNF Notation Conventions

The following conventions are used throughout this document:

```bnf
<rule> ::= definition of a non-terminal

terminal literal text, case-insensitive keyword, or fixed token

[item] item is optional

{item} item may repeat zero or more times

item1 | item2 alternative choices

(item) grouping

<integer> a whole number

<real> a floating-point number

<name> an identifier string (no spaces, max 31 chars)

<string> a quoted or unquoted text value

;; comment line (ignored by parser)
```

### 1.2 File Structure

A SWMM input file consists of a sequence of named sections. Each section
begins with a bracketed keyword and continues until the next section
header or end of file.

```bnf
<swmm-input> ::= {<section>}

<section> ::= <section-header> <newline> {<comment-line> |
<data-line>}

<section-header> ::= '[' <section-name> ']'

<comment-line> ::= ';;' {<any-char>} <newline>

<data-line> ::= <field> {<whitespace> <field>} <newline>

<field> ::= <name> | <integer> | <real> | <string>

<whitespace> ::= ' ' | '\t'
```

## 2. Hydraulic Network Sections

### 2.1 [TITLE]

Provides a descriptive title for the project. Lines are free-form text.

```bnf
<title-section> ::= '[TITLE]' <newline> {<text-line>}

<text-line> ::= <string> <newline>
```

### 2.2 [OPTIONS]

Global simulation options. Each line is a keyword-value pair.

```bnf
<options-section> ::= '[OPTIONS]' <newline> {<option-line>}

<option-line> ::= <option-key> <option-value> <newline>

<option-key> ::= 'FLOW_UNITS' | 'INFILTRATION' |
'FLOW_ROUTING'

| 'LINK_OFFSETS' | 'FORCE_MAIN_EQUATION'

| 'IGNORE_RAINFALL' | 'IGNORE_SNOWMELT'

| 'IGNORE_GROUNDWATER' | 'IGNORE_RDII'

| 'IGNORE_ROUTING' | 'IGNORE_QUALITY'

| 'START_DATE' | 'START_TIME'

| 'REPORT_START_DATE' | 'REPORT_START_TIME'

| 'END_DATE' | 'END_TIME'

| 'SWEEP_START' | 'SWEEP_END'

| 'DRY_DAYS' | 'REPORT_STEP'

| 'WET_STEP' | 'DRY_STEP' | 'ROUTING_STEP'

| 'RULE_STEP' | 'LENGTHENING_STEP'

| 'VARIABLE_STEP' | 'MINIMUM_STEP'

| 'INERTIAL_DAMPING' | 'NORMAL_FLOW_LIMITED'

| 'MIN_SURFAREA' | 'MIN_SLOPE'

| 'MAX_TRIALS' | 'HEAD_TOLERANCE'

| 'THREADS' | 'TEMPDIR'

<flow-units> ::= 'CFS' | 'GPM' | 'MGD' | 'CMS' |
'LPS' | 'MLD'

<infiltration>::= 'HORTON' | 'MODIFIED_HORTON' |
'GREEN_AMPT'

| 'MODIFIED_GREEN_AMPT' | 'CURVE_NUMBER'

<flow-routing>::= 'STEADY' | 'KINWAVE' | 'DYNWAVE'

<date> ::= MM/DD/YYYY

<time> ::= HH:MM:SS

<timestep> ::= HH:MM:SS | <real> ;; seconds if no colon
```

### 2.3 [JUNCTIONS]

Defines junction nodes — points where conduits connect. Junctions have
a single invert elevation and optional surcharge/ponding parameters.

```bnf
<junctions-section> ::= '[JUNCTIONS]' <newline>
{<junction-line>}

<junction-line> ::= <name> <elevation> [<maxdepth>]
[<initdepth>]

[<surdepth>] [<aponded>] <newline>

<elevation> ::= <real> ;; invert elevation (ft or m)

<maxdepth> ::= <real> ;; max water depth (0 = crown of connecting
conduits)

<initdepth> ::= <real> ;; initial water depth

<surdepth> ::= <real> ;; additional surcharge depth

<aponded> ::= <real> ;; ponded surface area when flooded (ft2 or
m2)
```

| Field     | Type    | Required | Description                                  |
|-----------|---------|----------|----------------------------------------------|
| Name      | `<name>` | Yes      | Unique junction identifier                   |
| Elevation | `<real>` | Yes      | Invert elevation (ft or m)                   |
| MaxDepth  | `<real>` | No       | Maximum water depth (0 = auto)               |
| InitDepth | `<real>` | No       | Initial water depth                          |
| SurDepth  | `<real>` | No       | Additional surcharge depth allowed           |
| Aponded   | `<real>` | No       | Ponded surface area when flooded (ft^2 or m^2) |

### 2.4 [OUTFALLS]

Terminal nodes of the drainage network. Each outfall has a boundary
condition type that controls the tailwater elevation.

```bnf
<outfalls-section> ::= '[OUTFALLS]' <newline>
{<outfall-line>}

<outfall-line> ::= <name> <elevation> <outfall-type>

[<stage-data>] [<gated>] [<route-to>] <newline>

<outfall-type> ::= 'FREE' | 'NORMAL' | 'FIXED' | 'TIDAL'
| 'TIMESERIES'

<stage-data> ::= <real> ;; for FIXED: fixed stage elevation

| <name> ;; for TIDAL: curve name

| <name> ;; for TIMESERIES: timeseries name

<gated> ::= 'YES' | 'NO' ;; flap gate present

<route-to> ::= <name> ;; subcatchment to receive outfall
discharge
```

| Field     | Type              | Required | Description                                                      |
|-----------|-------------------|----------|------------------------------------------------------------------|
| Name      | `<name>`          | Yes      | Unique outfall identifier                                         |
| Elevation | `<real>`          | Yes      | Invert elevation (ft or m)                                        |
| Type      | keyword           | Yes      | `FREE`, `NORMAL`, `FIXED`, `TIDAL`, or `TIMESERIES`               |
| StageData | `<real>` / `<name>` | No       | Fixed stage elevation, tidal curve name, or timeseries name        |
| Gated     | `YES` / `NO`      | No       | Flap gate present (default `NO`)                                  |
| RouteTo   | `<name>`          | No       | Subcatchment that receives outfall discharge                      |

### 2.5 [DIVIDERS]

Flow divider nodes that split inflow between two conduits according to a
specified rule.

```bnf
<dividers-section> ::= '[DIVIDERS]' <newline>
{<divider-line>}

<divider-line> ::= <name> <elevation> <diverted-link>

<divider-type> <divider-params>

[<maxdepth>] [<initdepth>] [<surdepth>] [<aponded>]
<newline>

<divider-type> ::= 'OVERFLOW' | 'CUTOFF' | 'TABULAR' |
'WEIR'

<divider-params> ::= <real> ;; CUTOFF: cutoff flow

| <name> ;; TABULAR: diversion curve name

| <real> <real> <real> ;; WEIR: min flow, height, coefficient
```

### 2.6 [STORAGE]

Storage unit nodes representing ponds, tanks, or basins. Storage
geometry can be defined as a functional or tabular relationship.

```bnf
<storage-section> ::= '[STORAGE]' <newline>
{<storage-line>}

<storage-line> ::= <name> <elevation> <maxdepth>
<initdepth>

<storage-curve> [<ponded>] [<fevap>]

[<psi> <ksat> <imd>] <newline>

<storage-curve> ::= 'FUNCTIONAL' <a-coeff> <b-coeff>
<c-const>

| 'TABULAR' <curve-name>

<a-coeff> ::= <real> ;; A in A*depth^B + C surface area formula

<b-coeff> ::= <real>

<c-const> ::= <real>

<ponded> ::= <real> ;; ponded area when flooded

<fevap> ::= <real> ;; fraction of evaporation (0-1)

;; psi, ksat, imd: Green-Ampt infiltration parameters (optional)
```

### 2.7 [CONDUITS]

Conduits are pipes or channels connecting nodes. They carry flow between
junctions, outfalls, dividers, and storage units.

```bnf
<conduits-section> ::= '[CONDUITS]' <newline>
{<conduit-line>}

<conduit-line> ::= <name> <from-node> <to-node> <length>

<roughness> <in-offset> <out-offset>

[<initflow>] [<maxflow>] <newline>

<from-node> ::= <name> ;; upstream node name

<to-node> ::= <name> ;; downstream node name

<length> ::= <real> ;; conduit length (ft or m)

<roughness> ::= <real> ;; Manning's n

<in-offset> ::= <real> ;; inlet offset above node invert

<out-offset> ::= <real> ;; outlet offset above node invert

<initflow> ::= <real> ;; initial flow (default 0)

<maxflow> ::= <real> ;; maximum flow allowed (default unlimited)
```

| Field     | Type    | Required | Description                                   |
|-----------|---------|----------|-----------------------------------------------|
| Name      | `<name>` | Yes      | Unique conduit identifier                      |
| FromNode  | `<name>` | Yes      | Upstream node                                  |
| ToNode    | `<name>` | Yes      | Downstream node                                |
| Length    | `<real>` | Yes      | Conduit length (ft or m)                       |
| Roughness | `<real>` | Yes      | Manning's `n` roughness coefficient            |
| InOffset  | `<real>` | Yes      | Inlet offset above the upstream node invert    |
| OutOffset | `<real>` | Yes      | Outlet offset above the downstream node invert |
| InitFlow  | `<real>` | No       | Initial flow (default 0)                       |
| MaxFlow   | `<real>` | No       | Maximum flow (0 = unlimited)                   |

### 2.8 [PUMPS]

Pump links that lift flow from a lower to a higher node. Pump behavior
is defined by a pump curve.

```bnf
<pumps-section> ::= '[PUMPS]' <newline> {<pump-line>}

<pump-line> ::= <name> <from-node> <to-node> <pump-curve>

[<status>] [<startup>] [<shutoff>] <newline>

<pump-curve> ::= <name> ;; name of curve in [CURVES] section

| '*' ;; ideal pump (for IDEAL pump type)

<status> ::= 'ON' | 'OFF' ;; initial status (default ON)

<startup> ::= <real> ;; startup depth at inlet node

<shutoff> ::= <real> ;; shutoff depth at inlet node
```

### 2.9 [ORIFICES]

Orifice links representing openings in walls or barriers. Can be
circular or rectangular, side or bottom mounted.

```bnf
<orifices-section> ::= '[ORIFICES]' <newline>
{<orifice-line>}

<orifice-line> ::= <name> <from-node> <to-node>

<orifice-type> <offset> <Cd>

[<gated>] [<close-time>] <newline>

<orifice-type> ::= 'SIDE' | 'BOTTOM'

<offset> ::= <real> ;; height above inlet node invert

<Cd> ::= <real> ;; discharge coefficient

<gated> ::= 'YES' | 'NO'

<close-time> ::= <real> ;; time (hours) to open/close flap gate
```

### 2.10 [WEIRS]

Weir links that model overflow structures. Multiple weir types and
optional road overtopping are supported.

```bnf
<weirs-section> ::= '[WEIRS]' <newline> {<weir-line>}

<weir-line> ::= <name> <from-node> <to-node>

<weir-type> <crest-height> <Cd>

[<gated>] [<end-con>] [<Cd2>] [<surcharge>]

[<road-width> <road-surf>] <newline>

<weir-type> ::= 'TRANSVERSE' | 'SIDEFLOW' | 'V-NOTCH'

| 'TRAPEZOIDAL' | 'ROADWAY'

<crest-height> ::= <real> ;; offset of weir crest above inlet
invert

<Cd> ::= <real> ;; discharge coefficient

<end-con> ::= <real> ;; end contraction coefficient (0-2)

<Cd2> ::= <real> ;; discharge coefficient for triangular ends

<surcharge> ::= 'YES' | 'NO' ;; allow surcharge above weir

<road-width> ::= <real> ;; ROADWAY only: width of road (ft or m)

<road-surf> ::= 'PAVED' | 'GRAVEL'
```

### 2.11 [OUTLETS]

Outlet links with user-defined or functional rating curve discharge
relationships.

```bnf
<outlets-section> ::= '[OUTLETS]' <newline> {<outlet-line>}

<outlet-line> ::= <name> <from-node> <to-node> <offset>

<outlet-type> <outlet-params> [<gated>] <newline>

<outlet-type> ::= 'TABULAR/DEPTH' | 'TABULAR/HEAD'

| 'FUNCTIONAL/DEPTH' | 'FUNCTIONAL/HEAD'

<outlet-params> ::= <name> ;; TABULAR: curve name

| <coeff> <expon> ;; FUNCTIONAL: Q = coeff * depth^expon
```

### 2.12 [XSECTIONS]

Cross-sectional geometry for conduits, orifices, and weirs.

```bnf
<xsections-section> ::= '[XSECTIONS]' <newline>
{<xsection-line>}

<xsection-line> ::= <link-name> <shape> <geom1> [<geom2>]

[<geom3>] [<geom4>] [<barrels>] [<culvert>]
<newline>

<shape> ::= 'CIRCULAR' | 'FORCE_MAIN' | 'FILLED_CIRCULAR'

| 'RECT_CLOSED' | 'RECT_OPEN' | 'TRAPEZOIDAL'

| 'TRIANGULAR' | 'HORIZ_ELLIPSE' | 'VERT_ELLIPSE'

| 'ARCH' | 'PARABOLIC' | 'POWER' | 'RECT_TRIANGULAR'

| 'RECT_ROUND' | 'MODBASKETHANDLE' | 'EGG'

| 'HORSESHOE' | 'GOTHIC' | 'CATENARY' | 'SEMIELLIPTICAL'

| 'BASKETHANDLE' | 'SEMICIRCULAR' | 'IRREGULAR'

| 'CUSTOM' | 'DUMMY'

;; For IRREGULAR: geom1 = transect name from [TRANSECTS]

;; For CUSTOM: geom1 = shape curve name from [CURVES]

;; For most shapes: geom1 = full height, geom2-4 = shape-specific

<barrels> ::= <integer> ;; number of parallel barrels (default 1)

<culvert> ::= <integer> ;; culvert code (0 = not a culvert)
```

### 2.13 [TRANSECTS]

Natural channel cross-sections for irregular conduits. Uses a
station-elevation format borrowed from HEC-RAS convention.

```bnf
<transects-section> ::= '[TRANSECTS]' <newline>
{<transect-block>}

<transect-block> ::= <nc-line> <x1-line> {<gr-line>}

<nc-line> ::= 'NC' <n-left> <n-right> <n-channel>

;; Manning's n for left, right, channel

<x1-line> ::= 'X1' <name> <n-stations> <x-left> <x-right>

<0> <0> <meander> <x-factor> <y-factor>

<gr-line> ::= 'GR' {<elevation> <station>}

;; up to 8 elevation-station pairs per line
```

### 2.14 [LOSSES]

Local head loss coefficients for conduits at entry, exit, and average
along length. Also controls flap gate presence.

```bnf
<losses-section> ::= '[LOSSES]' <newline> {<loss-line>}

<loss-line> ::= <conduit-name> [<kin>] [<kout>]
[<kavg>]

[<flap-gate>] [<seepage>] <newline>

<kin> ::= <real> ;; entry loss coefficient

<kout> ::= <real> ;; exit loss coefficient

<kavg> ::= <real> ;; average loss coefficient along length

<flap-gate> ::= 'YES' | 'NO'

<seepage> ::= <real> ;; seepage loss rate (in/hr or mm/hr)
```

## 3. Hydrology Sections

### 3.1 [RAINGAGES]

Rain gage objects that provide rainfall input to subcatchments. Rainfall
can come from a time series or an external file.

```bnf
<raingages-section> ::= '[RAINGAGES]' <newline>
{<raingage-line>}

<raingage-line> ::= <name> <rain-type> <interval> <scf>

<source> <newline>

<rain-type> ::= 'INTENSITY' | 'VOLUME' | 'CUMULATIVE'

<interval> ::= <time> ;; recording interval HH:MM

<scf> ::= <real> ;; snow catch factor (default 1.0)

<source> ::= 'TIMESERIES' <ts-name>

| 'FILE' <filename> <station-id> <rain-units>

<rain-units> ::= 'IN' | 'MM'
```

### 3.2 [SUBCATCHMENTS]

Subcatchments are land areas that generate runoff from rainfall. Each
drains to a node or another subcatchment.

```bnf
<subcatchments-section> ::= '[SUBCATCHMENTS]' <newline>
{<subcatchment-line>}

<subcatchment-line> ::= <name> <rain-gage> <outlet>

<area> <imperv> <width>

<slope> [<curb-len>] [<snow-pack>] <newline>

<rain-gage> ::= <name> ;; rain gage providing rainfall

<outlet> ::= <name> ;; node or subcatchment receiving runoff

<area> ::= <real> ;; area (acres or ha)

<imperv> ::= <real> ;; percent impervious (0-100)

<width> ::= <real> ;; characteristic width (ft or m)

<slope> ::= <real> ;; average slope (percent)

<curb-len> ::= <real> ;; curb length for pollutant buildup

<snow-pack> ::= <name> ;; snow pack object name
```

### 3.3 [SUBAREAS]

Overland flow parameters for the pervious and impervious sub-areas
within each subcatchment.

```bnf
<subareas-section> ::= '[SUBAREAS]' <newline>
{<subarea-line>}

<subarea-line> ::= <subcatch-name> <n-imperv> <n-perv>

<ds-imperv> <ds-perv> <pct-zero>

[<route-to>] [<pct-routed>] <newline>

<n-imperv> ::= <real> ;; Manning's n for impervious area

<n-perv> ::= <real> ;; Manning's n for pervious area

<ds-imperv> ::= <real> ;; depression storage for impervious (in
or mm)

<ds-perv> ::= <real> ;; depression storage for pervious

<pct-zero> ::= <real> ;; percent of impervious with no depression
storage

<route-to> ::= 'IMPERVIOUS' | 'PERVIOUS' | 'OUTLET'

<pct-routed> ::= <real> ;; percent routed to above destination
```

### 3.4 [INFILTRATION]

Infiltration parameters for the pervious area of each subcatchment.
Parameter fields depend on the infiltration model selected in
[OPTIONS].

```bnf
<infiltration-section> ::= '[INFILTRATION]' <newline>
{<infiltration-line>}

;; Horton / Modified Horton:

<infiltration-line> ::= <subcatch-name> <max-rate> <min-rate>

<decay> <dry-time> [<max-infil>] <newline>

;; Green-Ampt / Modified Green-Ampt:

<infiltration-line> ::= <subcatch-name> <suction> <ksat>
<imd> <newline>

;; Curve Number:

<infiltration-line> ::= <subcatch-name> <curve-number>

[<conductivity>] [<dry-time>] <newline>
```

### 3.5 [LID_CONTROLS]

Low Impact Development control definitions. Each LID type is described
by a series of parameter lines.

```bnf
<lid-controls-section> ::= '[LID_CONTROLS]' <newline>
{<lid-block>}

<lid-block> ::= <lid-name> <lid-type> <newline>

{<lid-layer-line>}

<lid-type> ::= 'BC' | 'PP' | 'GR' | 'IT' | 'RB' |
'RO' | 'VS'

;; BC=Bio-Cell, PP=Porous Pavement, GR=Green Roof,

;; IT=Infiltration Trench, RB=Rain Barrel,

;; RO=Rooftop Disconnection, VS=Vegetative Swale

<lid-layer-line>::= <lid-name> <layer> <param1> ...
<paramN> <newline>

<layer> ::= 'SURFACE' | 'SOIL' | 'STORAGE' | 'PAVEMENT'

| 'DRAIN' | 'DRAINMAT'
```

### 3.6 [LID_USAGE]

Placement of LID controls within subcatchments.

```bnf
<lid-usage-section> ::= '[LID_USAGE]' <newline>
{<lid-usage-line>}

<lid-usage-line> ::= <subcatch-name> <lid-name> <number>

<area> <width> <initsat> <fromimperv>

<toperv> [<rptfile>] [<drainTo>] [<fromperv>]

<newline>
```

### 3.7 [AQUIFERS]

Groundwater aquifer properties used by subcatchments for groundwater
exchange calculations.

```bnf
<aquifers-section> ::= '[AQUIFERS]' <newline>
{<aquifer-line>}

<aquifer-line> ::= <name> <por> <wp> <fc> <ksat>
<kslope>

<tslope> <etloss> <etdepth> <tbot>

<psi> [<uzone-ksat>] [<uzone-init>] <newline>

;; por=porosity, wp=wilting point, fc=field capacity

;; ksat=conductivity, kslope=conductivity slope

;; tslope=tension slope, etloss=ET loss fraction

;; etdepth=water table depth at which ET ceases

;; tbot=elevation of aquifer bottom

;; psi=suction head at wetting front
```

### 3.8 [GROUNDWATER]

Links subcatchments to aquifers and defines groundwater flow parameters.

```bnf
<groundwater-section> ::= '[GROUNDWATER]' <newline>
{<gw-line>}

<gw-line> ::= <subcatch-name> <aquifer-name> <node-name>

<esurf> <a1> <b1> <a2> <b2> <a3>

<dsw> [<egwt>] [<ebot>] [<wgr>] [<umc>]

<newline>

;; a1,b1: lateral groundwater flow coefficients

;; a2,b2: deep groundwater flow coefficients

;; a3: surface water flow coefficient

;; dsw: fixed depth of surface water (or 0 to use computed value)

;; egwt: threshold water table elevation for flow to occur
```

### 3.9 [SNOWPACKS]

Snow accumulation and melt parameters. Each snow pack object has four
parameter lines covering plowable, impervious, pervious, and
melt/redistribution settings.

```bnf
<snowpacks-section> ::= '[SNOWPACKS]' <newline>
{<snowpack-block>}

<snowpack-block> ::= <snowpack-name> 'PLOWABLE' <params>
<newline>

<snowpack-name> 'IMPERVIOUS' <params> <newline>

<snowpack-name> 'PERVIOUS' <params> <newline>

<snowpack-name> 'REMOVAL' <removal-params> <newline>

<params> ::= <min-melt> <max-melt> <base-temp> <fwf>
<sdepth> <initsnow> [<initfree>]

;; min-melt/max-melt: melt coefficients at min/max temperatures

;; base-temp: temperature below which no melt occurs

;; fwf: free water holding capacity fraction

;; sdepth: depth of snow that covers full area (in or mm)
```

## 4. Water Quality Sections

### 4.1 [POLLUTANTS]

Defines pollutants to be simulated.

```bnf
<pollutants-section> ::= '[POLLUTANTS]' <newline>
{<pollutant-line>}

<pollutant-line> ::= <name> <units> [<rain-conc>]
[<gw-conc>]

[<rdii-conc>] [<decay>] [<snow-flag>]

[<co-pollutant>] [<co-fraction>]

[<cdwf>] [<cinit>] <newline>

<units> ::= 'MG/L' | 'UG/L' | 'COUNT/L'

<decay> ::= <real> ;; first-order decay coefficient (1/days)

<snow-flag> ::= 'YES' | 'NO' ;; buildup in snow

<co-pollutant>::= <name> ;; co-pollutant name

<co-fraction> ::= <real> ;; fraction of co-pollutant
```

### 4.2 [LANDUSES]

Land use categories for pollutant buildup and washoff calculations.

```bnf
<landuses-section> ::= '[LANDUSES]' <newline>
{<landuse-line>}

<landuse-line> ::= <name> [<sweep-interval>]
[<availability>]

[<last-swept>] <newline>
```

### 4.3 [BUILDUP]

Pollutant buildup functions for each land use and pollutant combination.

```bnf
<buildup-section> ::= '[BUILDUP]' <newline>
{<buildup-line>}

<buildup-line> ::= <landuse-name> <pollutant-name>

<func-type> <c1> <c2> <c3> <normalizer> <newline>

<func-type> ::= 'NONE' | 'POW' | 'EXP' | 'SAT' |
'EXT'

<normalizer> ::= 'AREA' | 'CURB'
```

### 4.4 [WASHOFF]

Pollutant washoff functions during rainfall events.

```bnf
<washoff-section> ::= '[WASHOFF]' <newline>
{<washoff-line>}

<washoff-line> ::= <landuse-name> <pollutant-name>

<func-type> <c1> <c2> <sweepeff> <bmpeff> <newline>

<func-type> ::= 'NONE' | 'EXP' | 'RC' | 'EMC'

<sweepeff> ::= <real> ;; street sweeping removal efficiency (0-1)

<bmpeff> ::= <real> ;; BMP removal efficiency (0-1)
```

### 4.5 [COVERAGES]

Fraction of each subcatchment's area assigned to each land use.

```bnf
<coverages-section> ::= '[COVERAGES]' <newline>
{<coverage-line>}

<coverage-line> ::= <subcatch-name> {<landuse-name>
<fraction>} <newline>

;; fractions for a subcatchment must sum to 1.0
```

### 4.6 [TREATMENT]

User-defined treatment functions for nodes. Expressions can reference
pollutant concentrations and hydraulic variables.

```bnf
<treatment-section> ::= '[TREATMENT]' <newline>
{<treatment-line>}

<treatment-line> ::= <node-name> <pollutant-name> '='
<expression> <newline>

;; expression variables:

;; C = inflow concentration of this pollutant

;; Cin = inflow concentration

;; HRT = hydraulic residence time (hours)

;; DT = routing step (seconds)

;; FLOW = inflow rate (CFS or CMS)

;; DEPTH = water depth

;; AREA = surface area

;; <pollutant> = concentration of named pollutant
```

### 4.7 [INFLOWS]

Direct external inflows of flow or pollutant mass to nodes.

```bnf
<inflows-section> ::= '[INFLOWS]' <newline> {<inflow-line>}

<inflow-line> ::= <node-name> ('FLOW' | <pollutant-name>)

<timeseries-name> <inflow-type>

[<units-factor>] [<scale-factor>]

[<baseline>] [<baseline-pattern>] <newline>

<inflow-type> ::= 'FLOW' | 'CONCEN' | 'MASS'
```

### 4.8 [DWF]

Dry weather flow baseline inflows to nodes for sanitary sewer modeling.

```bnf
<dwf-section> ::= '[DWF]' <newline> {<dwf-line>}

<dwf-line> ::= <node-name> ('FLOW' | <pollutant-name>)

<avg-value> [<pattern1>] [<pattern2>]

[<pattern3>] [<pattern4>] <newline>

;; up to 4 time patterns (MONTHLY, DAILY, HOURLY, WEEKEND)
```

## 5. Reference Data Sections

### 5.1 [CURVES]

X-Y data curves used for pump characteristics, storage geometry, rating
curves, and custom cross-sections. A curve is defined by its name and
type on the first line, followed by data point lines.

```bnf
<curves-section> ::= '[CURVES]' <newline> {<curve-block>}

<curve-block> ::= <curve-name> <curve-type> <x> <y>
<newline>

{<curve-name> <x> <y> <newline>}

<curve-type> ::= 'STORAGE' | 'SHAPE' | 'DIVERSION' |
'TIDAL'

| 'PUMP1' | 'PUMP2' | 'PUMP3' | 'PUMP4'

| 'RATING' | 'CONTROL'

;; PUMP1: volume vs. flow

;; PUMP2: depth vs. flow (inlet node depth)

;; PUMP3: head vs. flow

;; PUMP4: depth vs. flow (both nodes)
```

### 5.2 [TIMESERIES]

Time series data for rainfall, evaporation, inflows, and other
time-varying inputs. Values can be given inline or loaded from an
external file.

```bnf
<timeseries-section> ::= '[TIMESERIES]' <newline>
{<timeseries-block>}

;; Inline absolute date/time format:

<timeseries-block> ::= {<ts-name> <date> <time> <value>
<newline>}

;; Inline relative time format:

<timeseries-block> ::= {<ts-name> <hours> <value>
<newline>}

;; File reference:

<timeseries-block> ::= <ts-name> 'FILE' <filename>
<newline>

<hours> ::= <real> ;; hours from simulation start
```

### 5.3 [PATTERNS]

Time patterns of multipliers used with dry weather flow. Each pattern
type has a fixed number of multipliers.

```bnf
<patterns-section> ::= '[PATTERNS]' <newline>
{<pattern-block>}

<pattern-block> ::= <pattern-name> <pattern-type>

{<multiplier>} <newline>

<pattern-type> ::= 'MONTHLY' ;; 12 multipliers (Jan-Dec)

| 'DAILY' ;; 7 multipliers (Sun-Sat)

| 'HOURLY' ;; 24 multipliers (midnight to 11pm)

| 'WEEKEND' ;; 24 multipliers for weekend hours

;; multipliers may span multiple lines with same name prefix
```

## 6. Controls and Rules

### 6.1 [CONTROLS]

Rule-based control statements that modify link settings during
simulation. Each rule evaluates a condition and applies an action when
true.

```bnf
<controls-section> ::= '[CONTROLS]' <newline>
{<rule-block>}

<rule-block> ::= 'RULE' <rule-id> <newline>

'IF' <condition> <newline>

{'AND' <condition> <newline>}

{'OR' <condition> <newline>}

'THEN' <action> <newline>

{'AND' <action> <newline>}

['ELSE' <action> <newline>]

['PRIORITY' <real> <newline>]

<condition> ::= <object> <attribute> <relop> <value>

<action> ::= <object> <attribute> '=' <value>

<relop> ::= '=' | '<>' | '<' | '>' | '<=' |
'>='

<object> ::= 'NODE' <name> | 'LINK' <name> |
'SIMULATION'

<attribute> ::= 'DEPTH' | 'HEAD' | 'FLOW' | 'STATUS' |
'SETTING'

| 'TIME' | 'DATE' | 'CLOCKTIME' | 'DAY' | 'MONTH'
```

## 7. Spatial and Display Sections

### 7.1 [MAP]

Defines the bounding box of the map display and units for the coordinate
system.

```bnf
<map-section> ::= '[MAP]' <newline>

'DIMENSIONS' <x1> <y1> <x2> <y2> <newline>

['UNITS' <map-units>]

<map-units> ::= 'FEET' | 'METERS' | 'DEGREES' | 'NONE'
```

### 7.2 [COORDINATES]

X-Y coordinates of all nodes (junctions, outfalls, dividers, storage
units).

```bnf
<coordinates-section> ::= '[COORDINATES]' <newline>
{<coord-line>}

<coord-line> ::= <node-name> <x> <y> <newline>

<x> ::= <real> ;; X coordinate (map units)

<y> ::= <real> ;; Y coordinate (map units)
```

### 7.3 [VERTICES]

Interior vertex points for conduit links. Only conduits with bends or
curves require entries.

```bnf
<vertices-section> ::= '[VERTICES]' <newline>
{<vertex-line>}

<vertex-line> ::= <link-name> <x> <y> <newline>

;; multiple lines with same link-name define sequential vertices
```

### 7.4 [POLYGONS]

Boundary polygon vertices for subcatchments. Multiple lines per
subcatchment define the polygon.

```bnf
<polygons-section> ::= '[POLYGONS]' <newline>
{<polygon-line>}

<polygon-line> ::= <subcatch-name> <x> <y> <newline>

;; polygon is closed implicitly (first = last point not required)
```

### 7.5 [SYMBOLS]

X-Y coordinates of rain gage symbols on the map.

```bnf
<symbols-section> ::= '[SYMBOLS]' <newline> {<symbol-line>}

<symbol-line> ::= <raingage-name> <x> <y> <newline>
```

### 7.6 [LABELS]

Text labels placed on the map at specified coordinates.

```bnf
<labels-section> ::= '[LABELS]' <newline> {<label-line>}

<label-line> ::= <x> <y> <quoted-string>

[<anchor-node>] [<font>] [<size>]

[<bold>] [<italic>] <newline>

<quoted-string> ::= '"' {<any-char>} '"'

<bold> ::= 'YES' | 'NO'

<italic> ::= 'YES' | 'NO'
```

## 8. Reporting and RDII Sections

### 8.1 [REPORT]

Controls what output is written to the report file.

```bnf
<report-section> ::= '[REPORT]' <newline> {<report-line>}

<report-line> ::= <report-key> <report-value> <newline>

<report-key> ::= 'INPUT' | 'CONTINUITY' | 'FLOWSTATS'

| 'CONTROLS' | 'SUBCATCHMENTS' | 'NODES' | 'LINKS'

<report-value> ::= 'YES' | 'NO' | 'ALL' | {<name>}
```

### 8.2 [HYDROGRAPHS]

Unit hydrographs for RDII (Rainfall Dependent Inflow and Infiltration)
analysis. Each hydrograph set contains short-, medium-, and long-term
response triangles.

```bnf
<hydrographs-section> ::= '[HYDROGRAPHS]' <newline>
{<hydrograph-block>}

<hydrograph-block> ::= <uh-group-name> <raingage-name>
<newline>

{<uh-group-name> <month> <response>

<R> <T> <K> [<IA-max>] [<IA-rec>] [<IA-ini>]

<newline>}

<month> ::= 'ALL' | 'JAN' | 'FEB' | 'MAR' | 'APR' |
'MAY' | 'JUN'

| 'JUL' | 'AUG' | 'SEP' | 'OCT' | 'NOV' | 'DEC'

<response> ::= 'SHORT' | 'MEDIUM' | 'LONG'

<R> ::= <real> ;; fraction of rainfall that becomes RDII

<T> ::= <real> ;; time to peak of unit hydrograph (hours)

<K> ::= <real> ;; ratio of recession to rising limb time
```

### 8.3 [RDII]

Assigns RDII unit hydrograph groups to nodes and specifies the
contributing sewershed area.

```bnf
<rdii-section> ::= '[RDII]' <newline> {<rdii-line>}

<rdii-line> ::= <node-name> <uh-group-name> <sewer-area>
<newline>

<sewer-area> ::= <real> ;; area of sewershed (acres or ha)
```

### 8.4 [LOADINGS]

Initial pollutant buildup on subcatchment surfaces at the start of
simulation.

```bnf
<loadings-section> ::= '[LOADINGS]' <newline>
{<loading-line>}

<loading-line> ::= <subcatch-name> {<pollutant-name>
<loading>} <newline>

<loading> ::= <real> ;; initial buildup (lbs/acre or kg/ha)
```

## 9. Climate Sections

### 9.1 [EVAPORATION]

Evaporation data and its source. Only one evaporation type is active at
a time.

```bnf
<evaporation-section> ::= '[EVAPORATION]' <newline>
{<evap-line>}

<evap-line> ::= <evap-type> <evap-params> <newline>

<evap-type> ::= 'CONSTANT' <rate>

| 'MONTHLY' <rate-jan> ... <rate-dec>

| 'TIMESERIES' <ts-name>

| 'TEMPERATURE' ;; computed from temperature data

| 'FILE' ;; read from climate file

| 'RECOVERY' <pattern-name>

| 'DRY_ONLY' 'YES' | 'NO'

<rate> ::= <real> ;; in/day or mm/day
```

### 9.2 [TEMPERATURE]

Air temperature data for snowmelt computations.

```bnf
<temperature-section> ::= '[TEMPERATURE]' <newline>
{<temp-line>}

<temp-line> ::= <temp-type> <temp-params> <newline>

<temp-type> ::= 'TIMESERIES' <ts-name>

| 'FILE' <filename> [<start-date>]

| 'WINDSPEED' 'MONTHLY' <v1> ... <v12>

| 'WINDSPEED' 'FILE'

| 'SNOWMELT' <temp-base> <atm-heat>

<neg-heat> <rain-melt>

| 'ADC' 'IMPERVIOUS' {<fraction>}

| 'ADC' 'PERVIOUS' {<fraction>}
```

## 10. Metadata Sections

### 10.1 [TAGS]

Optional user-defined tags for categorizing objects. Any object type may
have an associated tag string.

```bnf
<tags-section> ::= '[TAGS]' <newline> {<tag-line>}

<tag-line> ::= <object-type> <object-name> <tag> <newline>

<object-type> ::= 'Node' | 'Link' | 'Subcatch'

<tag> ::= <string> ;; free-form label (no spaces)
```

### 10.2 [BACKDROP]

Background image for the map display window. Not used by the solver.

```bnf
<backdrop-section> ::= '[BACKDROP]' <newline>

['FILE' <filename> <newline>]

['DIMENSIONS' <x1> <y1> <x2> <y2> <newline>]
```

### 10.3 [PROFILE]

Defines profile views of the network for display purposes only.

```bnf
<profile-section> ::= '[PROFILE]' <newline>
{<profile-line>}

<profile-line> ::= <quoted-name> {<node-name>} <newline>
```

**Appendix A: Token Primitives**

```bnf
<name> ::= <letter> {<letter> | <digit> | '_' | '-'
| '.'}

;; max 31 characters, case-insensitive

<integer> ::= ['-'] <digit> {<digit>}

<real> ::= ['-'] <digit> {<digit>} ['.' {<digit>}]

['e' | 'E'] ['+' | '-'] <digit> {<digit>}

<date> ::= <month> '/' <day> '/' <year>

;; month/day/year, two or four digit year accepted

<time> ::= <hour> ':' <minute> [':' <second>]

<filename> ::= <quoted-string> | <unquoted-path>

;; Whitespace (spaces and tabs) separates fields.

;; Lines beginning with ;; are comments and are ignored.

;; Section names and keywords are case-insensitive.

;; Object names are case-insensitive and max 31 characters.
```

**Appendix B: Section Index**

Quick reference of all sections and their primary purpose.

| Section        | Category   | Purpose                                   |
|----------------|------------|-------------------------------------------|
| [TITLE]        | General    | Project description                        |
| [OPTIONS]      | General    | Simulation parameters and control flags    |
| [JUNCTIONS]    | Network    | Junction node geometry and depth parameters |
| [OUTFALLS]     | Network    | Terminal node boundary conditions           |
| [DIVIDERS]     | Network    | Flow diversion nodes                        |
| [STORAGE]      | Network    | Storage unit nodes                          |
| [CONDUITS]     | Network    | Pipe and channel links                      |
| [PUMPS]        | Network    | Pump links                                  |
| [ORIFICES]     | Network    | Orifice links                               |
| [WEIRS]        | Network    | Weir links                                  |
| [OUTLETS]      | Network    | Rating curve outlet links                   |
| [XSECTIONS]    | Network    | Cross-section geometry for links            |
| [TRANSECTS]    | Network    | Irregular natural channel cross-sections    |
| [LOSSES]       | Network    | Minor head losses and seepage               |
| [RAINGAGES]    | Hydrology  | Rainfall input objects                      |
| [SUBCATCHMENTS] | Hydrology  | Runoff-generating land areas                |
| [SUBAREAS]     | Hydrology  | Overland flow parameters                    |
| [INFILTRATION] | Hydrology  | Pervious area infiltration                  |
| [LID_CONTROLS] | Hydrology  | LID control definitions                     |
| [LID_USAGE]    | Hydrology  | LID placement in subcatchments              |
| [AQUIFERS]     | Hydrology  | Groundwater aquifer properties              |
| [GROUNDWATER]  | Hydrology  | Groundwater-subcatchment linkage            |
| [SNOWPACKS]    | Hydrology  | Snow accumulation and melt                  |
| [POLLUTANTS]   | Quality    | Pollutant definitions                       |
| [LANDUSES]     | Quality    | Land use categories                         |
| [BUILDUP]      | Quality    | Pollutant buildup functions                 |
| [WASHOFF]      | Quality    | Pollutant washoff functions                 |
| [COVERAGES]    | Quality    | Land use fractions per subcatchment         |
| [TREATMENT]    | Quality    | Node treatment functions                    |
| [INFLOWS]      | Quality    | External inflows to nodes                   |
| [DWF]          | Quality    | Dry weather flow inflows                    |
| [LOADINGS]     | Quality    | Initial pollutant buildup                   |
| [CURVES]       | Reference  | X-Y data curves                             |
| [TIMESERIES]   | Reference  | Time-varying data                           |
| [PATTERNS]     | Reference  | Periodic multiplier patterns                |
| [CONTROLS]     | Controls   | Rule-based link control                     |
| [HYDROGRAPHS]  | RDII       | Unit hydrograph groups                      |
| [RDII]         | RDII       | RDII node assignments                       |
| [EVAPORATION]  | Climate    | Evaporation data                            |
| [TEMPERATURE]  | Climate    | Temperature and snowmelt data               |
| [MAP]          | Spatial    | Map bounding box                            |
| [COORDINATES]  | Spatial    | Node X-Y coordinates                        |
| [VERTICES]     | Spatial    | Conduit interior vertices                   |
| [POLYGONS]     | Spatial    | Subcatchment boundary polygons              |
| [SYMBOLS]      | Spatial    | Rain gage map symbols                       |
| [LABELS]       | Spatial    | Map text labels                             |
| [TAGS]         | Metadata   | Object categorization tags                  |
| [BACKDROP]     | Metadata   | Background map image                        |
| [PROFILE]      | Metadata   | Profile view definitions                    |

