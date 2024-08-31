# Shor Code Error Correction Project


## Introduction
The Shor code is a quantum error correction code capable of correcting any single-qubit error, including bit-flips, phase-flips, or a combination of both. 
This project extends the fundamental concepts of quantum error correction, building upon the basic Bit-Flip and Phase-Flip codes to implement the Shor code using Qiskit. The project aims to simulate the Shor code, analyze its effectiveness, and compare it with scenarios where no error correction is used.


### Project Structure
The project is divided into the following main sections:

Part 1: Defining the Components
1. Implementing the Phase-Flip Code.
2. Implementing the Bit-Flip Code.

Part 2: Implementing the Shor Code
1. Combining the Phase-Flip and Bit-Flip codes to construct the Shor Code.
2. Simulating the Shor code with and without errors.

Part 3: Analyzing the Shor Code
1. Evaluating the effectiveness of the Shor code by measuring the fidelity of quantum states.
2. Comparing the Shor code’s performance with and without error correction.


### Requirements
1. Python 3.7+
2. Qiskit
3. Matplotlib

To install the required libraries, run:

`pip install qiskit matplotlib`

## Implementation Steps

### Part 1: Defining the Components
1.1 Implementing the Phase-Flip Code

The Phase-Flip code is the first part of the Shor code. The logical qubit is encoded into a 3-qubit code that protects against phase-flip errors.
1. Encoding Circuit: The logical qubit is entangled with two ancillary qubits using CNOT gates and placed in a superposition using Hadamard gates.
2. Correction Circuit: The correction circuit detects and corrects any phase-flip errors by checking the phases of the qubits and applying a Toffoli gate if necessary.

### Flow Diagram :

![Screenshot of a comment on a GitHub issue showing an image, added in the Markdown, of an Octocat smiling and raising a tentacle.]()
