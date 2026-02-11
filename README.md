# Sistema REDAM - Registro de Deudores Alimentarios Morosos

Sistema de consulta del Registro de Deudores Alimentarios Morosos del Poder Judicial del Perú.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![PyQt5 Version](https://img.shields.io/badge/PyQt5-5.15.10-green)](https://pypi.org/project/PyQt5/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## Tabla de Contenidos

- [Estructura del proyecto](#-descripción)
- [Descripción](#-descripción)
- [Características](#-características)
- [Busqueda en Pantalla](#-busqueda-en-pantalla)
- [Requisitos del Sistema](#-requisitos-del-sistema)
- [Instalación](#-instalación)
  - [Windows](#windows)
  - [macOS](#macos)
  - [Linux](#linux)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Tecnologías](#-tecnologías)
- [Solución de Problemas](#-solución-de-problemas)
- [FAQ](#-preguntas-frecuentes)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)
- [Contacto](#-contacto)

---

## Estructura del Proyecto
Project_REDAM/
│
├── main.py                         # Punto de entrada
├── requirements.txt                # Dependencias
├── README.md                       # Este archivo
│
├── models/                         # Modelos de datos
│   ├── __init__.py
│   ├── consulta.py                 # Clase Consulta
│   ├── demandante.py               # Clase Demandante
│   ├── deudor_alimentario.py       # Clase DeudorAlimentario
│   └── expediente.py               # Clase ExpedienteJudicial
│
├── views/                          # Interfaces de usuario
│   ├── __init__.py
│   ├── ventana_principal.py        # Ventana principal
│   ├── tab_nombres.py              # Pestaña búsqueda nombres
│   ├── tab_dni.py                  # Pestaña búsqueda DNI
│   ├── tab_fechas.py               # Pestaña búsqueda fechas
│   └── ventana_detalle.py          # Ventana de detalle
│
├── controllers/                    # Lógica de negocio
│   ├── __init__.py
│   └── controlador_redam.py        # Controlador principal
│
├── services/                       # Servicios auxiliares
│   ├── __init__.py
│   └── generador_captcha.py        # Generador de captcha
│
├── data/                           # Datos
│   └── deudores_mock.json          # Datos de prueba
│
│
├── utils/                          # Utilidades
│   ├── __init__.py
│   └── validacioness.py            # Validaciones

## Descripción

El **Sistema REDAM** es una aplicación de escritorio desarrollada en Python que permite consultar información sobre deudores alimentarios morosos registrados en el Poder Judicial del Perú, conforme a la Ley N° 28970.

### ¿Qué hace este sistema?

Permite buscar información sobre personas que tienen deudas por pensiones alimenticias mediante tres métodos:

- **Búsqueda por Nombres y Apellidos**
- **Búsqueda por Documento de Identidad** (DNI, Carnet de Extranjería, Pasaporte)
- **Búsqueda por Rango de Fechas**

---

## Características

### Funcionalidades Principales

- **Múltiples métodos de búsqueda** - Por nombres, documento o fechas
- **Información detallada** - Expedientes judiciales, montos adeudados, demandantes
- **Sistema de seguridad** - Captcha alfanumérico de 4 caracteres
- **Validación en tiempo real** - Verifica datos antes de consultar
- **Interfaz intuitiva** - Diseño limpio con colores institucionales
- **Resultados organizados** - Tablas interactivas con opción de ver detalles
- **Multiplataforma** - Funciona en Windows, macOS y Linux

### Información Mostrada

Para cada deudor encontrado:

- Datos personales completos
- Número y detalles del expediente judicial
- Distrito judicial y órgano jurisdiccional
- Nombre del secretario judicial
- Pensión mensual establecida
- Importe total adeudado
- Intereses generados
- Información del demandante

---

## Busquedas en Pantalla

### Ventana Principal - Búsqueda por Nombres
![Búsqueda por Nombres]

### Búsqueda por DNI
![Búsqueda por DNI]

### Búsqueda por Fechas
![Búsqueda por Fechas]

### Ventana de Detalle
![Detalle del Deudor]

---

## Requisitos del Sistema

### Hardware Mínimo

| Componente            | Requisito Mínimo                          | Recomendado |

| **Procesador**        | Intel Core i3 o equivalente               | Intel Core i5 o superior |
| **RAM**               | 4 GB                                      | 8 GB o más |
| **Disco**             | 200 MB libres                             | 500 MB libres |
| **Pantalla**          | 1024x768 px                               | 1920x1080 px |

### Software Requerido

| Software              | Versión Mínima                            | Versión Recomendada |

| **Sistema Operativo** | Windows 10 / macOS 10.14 / Ubuntu 18.04   | Windows 11 / macOS 13+ / Ubuntu 22.04 |
| **Python**            | 3.8                                       | 3.11 o 3.12 |
| **pip**               | 20.0                                      | Última versión |

---

##  Instalación

### Windows

#### Paso 1: Instalar Python

1. Descargar Python desde [python.org](https://www.python.org/downloads/)
2. Ejecutar el instalador
3. **IMPORTANTE:** Marcar la casilla **"Add Python to PATH"**
4. Hacer clic en "Install Now"
5. Esperar a que termine y hacer clic en "Close"

### Instalar PyQt5
pip install PyQt5

**Verificar instalación:**

# Abrir CMD (Símbolo del sistema)

python --version
# Debe mostrar: Python 3.x.x

pip --version
# Debe mostrar: pip 24.x.x

### Iniciar con main.py
python main.py


