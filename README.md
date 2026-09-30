# semi-automated-mcb-tester
semi automated high current short circuit for  mcb
# Semi-Automated MCB Tester

A hardware prototype for semi-automated testing of Miniature Circuit Breakers (MCBs), designed to improve repeatability, operator safety, and test workflow compared with fully manual testing.

## Project Overview

The system provides a controlled test station for MCB testing. A high-current test source is connected to the MCB under test, while the control and measurement system supervises the test process.

### Main Objectives

- Provide a universal MCB mounting/test station.
- Support single-pole, SPN, DP, TP and FP MCB configurations.
- Support the prototype target range of 0.5 A–63 A.
- Automate the mechanical test-position operation using a stepper motor.
- Measure current using a CT sensor and an STM32/measurement controller.
- Provide a safer and more repeatable test workflow.
- Provide wireless communication/monitoring where implemented.

### HARDWARE COMPONENTS 
- STM32F10C3 [BLUEPILL]
- ESP32
- MOTAR DRIVE DVF8825
- STEPPER MOTAR
- 10KOHM RESISTOR
- 33OHM RESISTOR
- 10MF 25V CAPACITOR
- COSTOM MADE HIGH CURRENT TRANSFORMER
- DC-DC BUCK CONVERTER
  

### SOFTWARE 
## System Description

This machine utilizes an **STM32F103C8T6 (Blue Pill)** as its main microcontroller. The controller is responsible for controlling and isolating the MCB under test through **motor drives and servo motors**.

The system also handles **data acquisition**, including measurement of the current flowing through the MCB and measurement of the **elapsed trip time**. The acquired data is communicated wirelessly to the **HMI (Human-Machine Interface) through an ESP32**, where the test data is displayed.

### Power Supply and High-Current Source

On the power-supply side, a **custom-made high-current transformer** connected in series with **XL inductors** provides the required **short-circuit test current**. It also provides the required **auxiliary power supply for the microcontrollers**.

### MCB Testing Capability

The machine is capable of performing tests on:

- **2-pole MCBs**
- **3-pole MCBs**
- **4-pole MCBs**

### Overall System

The complete system integrates the **STM32F103C8T6 controller, motor drives, servo motors, current measurement, elapsed-time measurement, ESP32 wireless communication, HMI, and custom high-current power supply** into a semi-automated MCB testing platform.
---

