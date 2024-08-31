


# Import necessary libraries
from qiskit import QuantumCircuit, Aer, transpile, assemble, execute, Aer, IBMQ
from qiskit.visualization import plot_histogram
from qiskit.circuit.random import random_circuit
from qiskit.quantum_info import Statevector, partial_trace, state_fidelity
from random import random
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Initialize Qiskit
# provider = IBMQ.load_account()
print("Libraries Imported Successfully!")

# Part 1: Defining the Components

# Part 1.1: The Phase-Flip Code

# Exercise 1: Phase-flip encode circuit

# 1. Initialize a circuit with 3 qubits
phaseflip_encode = QuantumCircuit(3, 1)

# 2. Entangle the state of qubit 0 with the other two qubits (CNOT gates)
phaseflip_encode.cx(0, 1)
phaseflip_encode.cx(0, 2)

# 3. Put all qubits in equal superpositions using Hadamard gates
phaseflip_encode.h(0)
phaseflip_encode.h(1)
phaseflip_encode.h(2)

# Display the circuit
phaseflip_encode.draw()

# Exercise 2: Phase-flip correct circuit

# 1. Initialize a circuit with 3 qubits
phaseflip_correct = QuantumCircuit(3, 1)

# 2. Detect errors by checking the phases with Hadamard and CNOT gates
phaseflip_correct.cx(0, 1)
phaseflip_correct.cx(0, 2)
phaseflip_correct.h(0)
phaseflip_correct.h(1)
phaseflip_correct.h(2)

# 3. Correct errors using a Toffoli gate
phaseflip_correct.ccx(1, 2, 0)

# Display the circuit
phaseflip_correct.draw()

# Exercise 3: Simulate the phase-flip code without errors

# Combine encoding and correction circuits
full_code = QuantumCircuit(3, 1)
full_code.cx(0, 1)
full_code.cx(0, 2)
full_code.h(0)

# Prepare the initial state and save its statevector
initial_state = Statevector.from_instruction(full_code)
initial_state = partial_trace(initial_state, [1, 2]).to_statevector()

full_code = full_code.compose(phaseflip_encode, qubits=[0, 1, 2])
full_code.barrier()

# No errors in this case

full_code.barrier()

# Detection and correction
full_code.cx(0, 1)
full_code.cx(0, 2)
full_code.ccx(1, 2, 0)

full_code = full_code.compose(phaseflip_correct, qubits=[0, 1, 2])
full_code.measure(0, 0)

# Save the final statevector for comparison to the initial one
final_state = Statevector.from_instruction(full_code)
final_state = partial_trace(final_state, [1, 2]).to_statevector()

# Display the circuit
full_code.draw()

# Compare the initial and final statevectors
print(initial_state.equiv(final_state))
initial_state.draw(output='bloch')
final_state.draw(output='bloch')

# Exercise 5: Simulate the phase-flip code with a phase-flip error on qubit 0

# Introducing a phase-flip error
full_code = full_code.compose(phaseflip_encode, qubits=[0, 1, 2])
full_code.z(0)  # Apply phase-flip (Z) error to qubit 0
full_code = full_code.compose(phaseflip_correct, qubits=[0, 1, 2])

# Save the final statevector for comparison to the initial one
final_state = Statevector.from_instruction(full_code)
final_state = partial_trace(final_state, [1, 2]).to_statevector()

# Display the circuit
full_code.draw()

# Compare the initial and final statevectors
print(initial_state.equiv(final_state))
initial_state.draw(output='bloch')
final_state.draw(output='bloch')

# Exercise 6: Simulate the phase-flip code with a bit-flip error on qubit 0

# Introducing a bit-flip error
full_code = full_code.compose(phaseflip_encode, qubits=[0, 1, 2])
full_code.x(0)  # Apply bit-flip (X) error to qubit 0
full_code = full_code.compose(phaseflip_correct, qubits=[0, 1, 2])

# Save the final statevector for comparison to the initial one
final_state = Statevector.from_instruction(full_code)
final_state = partial_trace(final_state, [1, 2]).to_statevector()

# Display the circuit
full_code.draw()

# Compare the initial and final statevectors
print(initial_state.equiv(final_state))
initial_state.draw(output='bloch')
final_state.draw(output='bloch')

# Part 1.2: The Bit-Flip Code

# Exercise 1: Bit-flip encode circuit

# 1. Initialize a circuit with 3 qubits
bitflip_encode = QuantumCircuit(3, 1)

# 2. Entangle the state of qubit 0 with the other two qubits (CNOT gates)
bitflip_encode.cx(0, 1)
bitflip_encode.cx(0, 2)

# Display the circuit
bitflip_encode.draw()

# Exercise 2: Bit-flip correct circuit

# 1. Initialize a circuit with 3 qubits
bitflip_correct = QuantumCircuit(3, 1)

# 2. Detect errors by checking the parity using CNOT gates
bitflip_correct.cx(0, 1)
bitflip_correct.cx(0, 2)

# 3. Correct errors using a Toffoli gate
bitflip_correct.ccx(1, 2, 0)

# Display the circuit
bitflip_correct.draw()

# Exercise 3: Simulate the bit-flip code without errors

# Combine encoding and correction circuits
full_code = QuantumCircuit(3, 1)
full_code.cx(0, 1)
full_code.cx(0, 2)

# Prepare the initial state and save its statevector
initial_state = Statevector.from_instruction(full_code)
initial_state = partial_trace(initial_state, [1, 2]).to_statevector()

full_code = full_code.compose(bitflip_encode, qubits=[0, 1, 2])
full_code.barrier()

# No errors in this case

full_code.barrier()

# Detection and correction
full_code.cx(0, 1)
full_code.cx(0, 2)
full_code.ccx(1, 2, 0)

full_code = full_code.compose(bitflip_correct, qubits=[0, 1, 2])
full_code.measure(0, 0)

# Save the final statevector for comparison to the initial one
final_state = Statevector.from_instruction(full_code)
final_state = partial_trace(final_state, [1, 2]).to_statevector()

# Display the circuit
full_code.draw()

# Compare the initial and final statevectors
print(initial_state.equiv(final_state))
initial_state.draw(output='bloch')
final_state.draw(output='bloch')

# Part 2: Implementing the Shor Code

# Exercise 1: Initialize a circuit with the correct number of qubits

shor_encode = QuantumCircuit(9, 1)

# Exercise 2: Apply phase-flip code every 3rd qubit

shor_encode = shor_encode.compose(phaseflip_encode, qubits=[0, 3, 6])

# Exercise 3: Encode each phase-flip code qubit using their own bit-flip code

shor_encode = shor_encode.compose(bitflip_encode, qubits=[0, 1, 2])
shor_encode = shor_encode.compose(bitflip_encode, qubits=[3, 4, 5])
shor_encode = shor_encode.compose(bitflip_encode, qubits=[6, 7, 8])

# Exercise 4: Initialize the correcting circuit with the correct number of qubits

shor_correct = QuantumCircuit(9, 1)

# Exercise 5: Correct bit-flips

shor_correct = shor_correct.compose(bitflip_correct, qubits=[0, 1, 2])
shor_correct = shor_correct.compose(bitflip_correct, qubits=[3, 4, 5])
shor_correct = shor_correct.compose(bitflip_correct, qubits=[6, 7, 8])

# Exercise 6: Correct phase-flips

shor_correct = shor_correct.compose(phaseflip_correct, qubits=[0, 3, 6])

# Exercise 7: Verify implementation by comparing initial and final statevectors

full_code = QuantumCircuit(9)

# Prepare the initial state
initial_state = Statevector.from_instruction(full_code)
initial_state = partial_trace(initial_state, [1, 2, 3, 4, 5, 6, 7, 8]).to_statevector()

# Encoding
full_code = full_code.compose(shor_encode, qubits=[0, 1, 2, 3, 4, 5, 6, 7, 8])
full_code.barrier()

# Introduce errors
full_code.x(0)  # Bit-flip error on qubit 0
full_code.z(0)  # Phase-flip error on qubit 0

full_code.barrier()

# Correction
full_code = full_code.compose(shor_correct, qubits=[0, 1, 2, 3, 4, 5, 6, 7, 8])

# Save the final statevector for comparison to the initial one
final_state = Statevector.from_instruction(full_code)
final_state = partial_trace(final_state, [1, 2, 3, 4, 5, 6, 7, 8]).to_statevector()

# Display the circuit
full_code.draw()

# Compare the initial and final statevectors
print(initial_state.equiv(final_state))
initial_state.draw(output='bloch')
final_state.draw(output='bloch')

# Exercise 8: Determine a way to break this error-correcting code

# Introducing errors to break the code
full_code = QuantumCircuit(9)
full_code = full_code.compose(shor_encode, qubits=[0, 1, 2, 3, 4, 5, 6, 7, 8])

# Apply both bit-flip and phase-flip errors on multiple qubits
full_code.x(0)
full_code.z(0)
full_code.x(1)
full_code.z(1)
full_code.x(2)
full_code.z(2)

# Apply the correction circuit
full_code = full_code.compose(shor_correct, qubits=[0, 1, 2, 3, 4, 5, 6, 7, 8])

# Final statevector comparison
final_state = Statevector.from_instruction(full_code)
final_state = partial_trace(final_state, [1, 2, 3, 4, 5, 6, 7, 8]).to_statevector()

# Compare the initial and final statevectors
print(initial_state.equiv(final_state))
initial_state.draw(output='bloch')
final_state.draw(output='bloch')

# Exercise 9: Simulate the Shor code for errors that occur 10% of the time

probability = 0.10
full_code = QuantumCircuit(9)

# Prepare the initial state
initial_state = Statevector.from_instruction(full_code)
initial_state = partial_trace(initial_state, [1, 2, 3, 4, 5, 6, 7, 8]).to_statevector()

# Encoding
full_code = full_code.compose(shor_encode, qubits=[0, 1, 2, 3, 4, 5, 6, 7, 8])
full_code.barrier()

# Introduce errors based on probability
for i in range(9):
    if random() < probability:
        full_code.x(i)
    if random() < probability:
        full_code.z(i)

full_code.barrier()

# Correction
full_code = full_code.compose(shor_correct, qubits=[0, 1, 2, 3, 4, 5, 6, 7, 8])

# Save the final statevector for comparison to the initial one
final_state = Statevector.from_instruction(full_code)
final_state = partial_trace(final_state, [1, 2, 3, 4, 5, 6, 7, 8]).to_statevector()

# Compare the initial and final statevectors
print(initial_state.equiv(final_state))
initial_state.draw(output='bloch')
final_state.draw(output='bloch')

# Exercise 10: Use the variable 'probability' for error occurrence

def get_fidelity(probability):
    full_code = QuantumCircuit(9)

    # Prepare the initial state
    initial_state = Statevector.from_instruction(full_code)
    initial_state = partial_trace(initial_state, [1, 2, 3, 4, 5, 6, 7, 8]).to_statevector()

    # Encoding
    full_code = full_code.compose(shor_encode, qubits=[0, 1, 2, 3, 4, 5, 6, 7, 8])
    full_code.barrier()

    # Introduce errors based on probability
    for i in range(9):
        if random() < probability:
            full_code.x(i)
        if random() < probability:
            full_code.z(i)

    full_code.barrier()

    # Correction
    full_code = full_code.compose(shor_correct, qubits=[0, 1, 2, 3, 4, 5, 6, 7, 8])

    # Save the final statevector for comparison to the initial one
    final_state = Statevector.from_instruction(full_code)
    final_state = partial_trace(final_state, [1, 2, 3, 4, 5, 6, 7, 8]).to_statevector()

    # Return the fidelity
    return state_fidelity(initial_state, final_state)

# Plotting the results
num_points = 50
num_trials_per_point = 100
average_fidelities_shor = []
probabilities = [p / num_points for p in range(num_points)]

for probability in probabilities:
    average_fidelity = 0
    for trial in range(num_trials_per_point):
        average_fidelity += get_fidelity(probability)

    average_fidelity /= num_trials_per_point
    average_fidelities_shor += [average_fidelity]

plt.figure(figsize=(11, 8))
plt.scatter(probabilities, average_fidelities_shor, label='Shor Code', color='orange')
plt.plot(probabilities, [(1 - p)**2 for p in probabilities], label='Without Error Correction', color='blue')

plt.title("Average Fidelity Using the Shor Code", fontsize='x-large')
plt.xlabel("Probability of an Error", fontsize='x-large')
plt.ylabel("Average Fidelity", fontsize='x-large')
plt.legend()
plt.show()

print("Shor Code simulation and analysis completed successfully!")


