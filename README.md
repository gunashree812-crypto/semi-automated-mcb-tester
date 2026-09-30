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
    PYTHON FOR HMI [HUMAN MACHINE INTERFACE]

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

 The complete system integrates the **STM32F103C8T6 controller, motor drives, servo motors, current measurement, elapsed-time measurement, ESP32 wireless           communication, HMI, and custom high-current power supply** into a semi-automated MCB testing platform.
 
## Working Sequence
   1. The MCB under test is mounted in the testing setup.
    2. The STM32F103C8T6 initializes and controls the testing system.
    3. Motor drives and servo motors position and isolate the MCB as required.
    4. The custom high-current transformer and XL inductors provide the required test current.
    5. The current flowing through the MCB is measured by the data-acquisition system.
    6. The elapsed time until the MCB operates is measured.
    7. The acquired data is transmitted wirelessly through the ESP32.
    8. The data is displayed on the HMI.
    9. After completion of the test, the system returns to its safe state.
      
## Advantages

- Reduces manual intervention during testing
- Provides repeatable test operation
- Enables electronic measurement of current and trip time
- Allows wireless transfer of test data to the HMI
- Supports multiple MCB pole configurations
- Integrates control, measurement and display into a single test platform

## Applications

The proposed system can be used for:

- MCB testing laboratories
- Electrical protection testing
- Educational laboratories
- Circuit-breaker testing demonstrations
- Electrical equipment research and development

## Future Improvements

Possible future improvements include:

- Automatic test-result storage
- Improved measurement accuracy
- Automatic generation of test reports
- Touchscreen HMI
- Remote monitoring
- Automated MCB identification
- Cloud-based data logging
- Improved safety interlocks
- Fully automated test sequencing

  ## Team

**Project:** Semi-Automated MCB Tester  
**Domain:** Electrical Engineering / Embedded Systems / Automation  
**Project Type:** Hardware Prototype / Hackathon Project
