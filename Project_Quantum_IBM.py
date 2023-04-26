#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!pip install qiskit

from qiskit import QuantumCircuit, Aer, transpile, assemble, execute, Aer, IBMQ
from qiskit.visualization import plot_histogram
from qiskit.circuit.random import random_circuit
from qiskit.quantum_info import Statevector, partial_trace, state_fidelity

from random import random
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')

#provider = IBMQ.load_account()

print("Libraries Imported Successfully!")


# In[2]:


phaseflip_encode = QuantumCircuit(3)


# In[3]:


phaseflip_encode.cx(0,1)
phaseflip_encode.cx(0,2)


# In[4]:


phaseflip_encode.h(range(3))


# In[5]:


from qiskit import QuantumCircuit, QuantumRegister

# Initialize a circuit with 3 qubits
qreg_q = QuantumRegister(3, 'q')
phaseflip_correct = QuantumCircuit(qreg_q)

# Detect any errors by checking that the phases of the 3 qubits match using H gates and CNOTs
phaseflip_correct.h(qreg_q[0])
phaseflip_correct.cx(qreg_q[0], qreg_q[1])
phaseflip_correct.cx(qreg_q[0], qreg_q[2])

# Correct any errors using a Toffoli gate
phaseflip_correct.ccx(qreg_q[1], qreg_q[2], qreg_q[0])

phaseflip_correct.draw()


# In[6]:


# Import required libraries
from qiskit import QuantumCircuit, Aer
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
from qiskit.quantum_info import partial_trace

# Create the encoding circuit
phaseflip_encode = QuantumCircuit(3, 3)
phaseflip_encode.h(0)
phaseflip_encode.cx(0,1)
phaseflip_encode.cx(0,2)
phaseflip_encode.barrier()

# Create the correction circuit
phaseflip_correct = QuantumCircuit(3, 1)
phaseflip_correct.cx(0,1)
phaseflip_correct.cx(0,2)
phaseflip_correct.ccx(2,1,0)
phaseflip_correct.barrier()

# Combine encoding and correction circuits
full_code = QuantumCircuit(3, 3)
full_code = phaseflip_encode.compose(full_code, qubits=[0, 1, 2])
full_code.barrier()
full_code = full_code.compose(phaseflip_correct, qubits=[0, 1, 2])

# Get the initial and final states
initial_state = Statevector.from_instruction(full_code)
initial_state = partial_trace(initial_state, [1, 2]).to_statevector()

full_code.x(0)  # Introduce a bit-flip error on qubit 0

final_state = Statevector.from_instruction(full_code)
final_state = partial_trace(final_state, [1, 2]).to_statevector()

# Check if the initial and final states are equivalent
print(f"Initial and final states are equivalent: {initial_state.equiv(final_state)}")

# Draw the Bloch sphere of each state for visual comparison
plot_bloch_multivector(initial_state)
plot_bloch_multivector(final_state)

# Draw the full circuit
full_code.draw()


# In[7]:


from qiskit import QuantumCircuit, execute, Aer
from qiskit.quantum_info import Statevector, partial_trace
from qiskit.providers.aer.noise import pauli_error
from qiskit.providers.aer.noise.errors import pauli_error

# Create encoding circuit
phaseflip_encode = QuantumCircuit(3)
phaseflip_encode.h(0)
phaseflip_encode.cx(0, 1)
phaseflip_encode.cx(0, 2)

# Create correction circuit
phaseflip_correct = QuantumCircuit(3, 1)
phaseflip_correct.cx(0, 1)
phaseflip_correct.cx(0, 2)
phaseflip_correct.measure(0, 0)

# Combine encoding and correction circuits
full_code = QuantumCircuit(3, 1)
full_code.x(0)
full_code.h(0)
full_code.barrier()

full_code.compose(phaseflip_encode, qubits=[0, 1, 2], inplace=True)
full_code.barrier()

# Apply phase-flip error to qubit 1
error_gate = pauli_error([('X', 1.0)])
full_code.append(error_gate, [1])

full_code.barrier()
full_code.compose(phaseflip_correct, qubits=[0, 1, 2], inplace=True)

# Simulate the circuit
backend = Aer.get_backend('qasm_simulator')
shots = 1024
results = execute(full_code, backend=backend, shots=shots).result()
counts = results.get_counts()

print("Initial state:", initial_state.data)
print("Final state:", final_state.data)
print("Counts:", counts)


# In[8]:


initial_state.equiv(final_state)

initial_state.draw(output='bloch')

final_state.draw(output='bloch')


# In[9]:


from qiskit import QuantumCircuit, execute, Aer
from qiskit.quantum_info import Statevector, partial_trace

# Define encoding circuit
phaseflip_encode = QuantumCircuit(3)
phaseflip_encode.h(0)
phaseflip_encode.cx(0, 1)
phaseflip_encode.cx(0, 2)

# Define correcting circuit
phaseflip_correct = QuantumCircuit(3)
phaseflip_correct.cx(0, 1)
phaseflip_correct.cx(0, 2)
phaseflip_correct.h(0)

# Initialize a quantum circuit with 3 qubits and 1 classical bit
phaseflip_error = QuantumCircuit(3, 1)

# Prepare the initial state and save its statevector
phaseflip_error.x(0)
phaseflip_error.h(0)

initial_state = Statevector.from_instruction(phaseflip_error)
initial_state = partial_trace(initial_state, [1, 2]).to_statevector()

# Combine the encoding circuit, the phase-flip error, and the correcting circuit using `.compose(...)`.
phaseflip_error = phaseflip_error.compose(phaseflip_encode, qubits=[0, 1, 2])
phaseflip_error.barrier()

# Add an error gate, such as a Z gate on the first qubit
phaseflip_error.z(0)
phaseflip_error.barrier()

phaseflip_error = phaseflip_error.compose(phaseflip_correct, qubits=[0, 1, 2])

# Save the final statevector for comparison to the initial one
final_state = Statevector.from_instruction(phaseflip_error)
final_state = partial_trace(final_state, [1, 2]).to_statevector()

# Draw the circuit
phaseflip_error.draw()


# In[10]:


initial_state.equiv(final_state)

initial_state.draw(output='bloch')

final_state.draw(output='bloch')


# In[11]:


from qiskit import QuantumCircuit, execute, Aer
from qiskit.quantum_info import Statevector, partial_trace
from qiskit.circuit.library.standard_gates import XGate, ZGate

# Define encoding circuit
phaseflip_encode = QuantumCircuit(3, name='phaseflip_encode')
phaseflip_encode.h(0)
phaseflip_encode.cx(0, 1)
phaseflip_encode.cx(0, 2)

# Define correcting circuit
phaseflip_correct = QuantumCircuit(3, name='phaseflip_correct')
phaseflip_correct.ccx(0, 1, 2)
phaseflip_correct.cx(0, 1)
phaseflip_correct.cx(1, 2)

# Initialize a quantum circuit with 3 qubits and 1 classical bit
full_code = QuantumCircuit(3, 1)

# Prepare the initial state and save its statevector
full_code.h(0)

initial_state = Statevector.from_instruction(full_code)
initial_state = partial_trace(initial_state, [1, 2]).to_statevector()

# Combine the encoding circuit, the bit-flip error, and the correcting circuit using `.compose(...)`.
full_code = full_code.compose(phaseflip_encode, qubits=[0, 1, 2])
full_code.barrier()

full_code.x(0)
full_code.barrier()

full_code = full_code.compose(phaseflip_correct, qubits=[0, 1, 2])

# Save the final statevector for comparison to the initial one
final_state = Statevector.from_instruction(full_code)
final_state = partial_trace(final_state, [1, 2]).to_statevector()

# Draw the circuit
full_code.draw()


# In[12]:


bitflip_encode = QuantumCircuit(3)


# In[13]:


bitflip_encode.cx(0, 1)
bitflip_encode.cx(0, 2)


# In[14]:


bitflip_correct = QuantumCircuit(3)


# In[15]:


bitflip_correct.cx(0,1)
bitflip_correct.cx(0,2)
bitflip_correct.cx(1,2)


# In[16]:


bitflip_correct.ccx(1,2,0)
bitflip_correct.draw()


# In[17]:


from qiskit import QuantumCircuit, execute, Aer
from qiskit.quantum_info import Statevector, partial_trace
from qiskit.circuit.library import XGate, ZGate

# Define encoding circuit
bitflip_encode = QuantumCircuit(3)
bitflip_encode.h(0)
bitflip_encode.cx(0, 1)
bitflip_encode.cx(0, 2)

# Define correcting circuit
bitflip_correct = QuantumCircuit(3)
bitflip_correct.cx(0, 1)
bitflip_correct.cx(0, 2)
bitflip_correct.append(XGate().control(2), [0, 1, 2])
bitflip_correct.cx(0, 1)
bitflip_correct.cx(0, 2)

# Define the full bit-flip code
bitflip_code = QuantumCircuit(3, 3)
bitflip_code.barrier()
bitflip_code = bitflip_code.compose(bitflip_encode, qubits=[0, 1, 2])
bitflip_code.barrier()
bitflip_code.x(0)
bitflip_code.barrier()
bitflip_code = bitflip_code.compose(bitflip_correct, qubits=[0, 1, 2])
bitflip_code.barrier()
bitflip_code.measure([0, 1, 2], [0, 1, 2])

# Simulate the circuit without errors
initial_state = Statevector.from_label('000')
backend = Aer.get_backend('statevector_simulator')
result = execute(bitflip_code, backend=backend).result()
final_state = result.get_statevector()


# In[18]:


from qiskit import QuantumCircuit, execute, Aer
from qiskit.quantum_info import Statevector, partial_trace
from qiskit.visualization import plot_bloch_multivector

# Define encoding circuit
encoding = QuantumCircuit(3)
encoding.h(1)
encoding.cx(1, 2)
encoding.cx(0, 1)
encoding.cx(1, 2)

# Define correcting circuit
correcting = QuantumCircuit(3)
correcting.cx(0, 1)
correcting.cx(0, 2)
correcting.ccx(1, 2, 0)

# Define initial state
initial_state = Statevector.from_label('-00')

# Apply bit-flip error on qubit 0
error = QuantumCircuit(3)
error.x(0)

# Create the full bitflip code by combining the encoding, error, and correcting circuits
bitflip_code = encoding.compose(error).compose(correcting)

# Simulate the circuit
backend = Aer.get_backend('statevector_simulator')
final_state = execute(bitflip_code, backend).result().get_statevector()

# Compare initial and final state
print('Initial state:')
print(initial_state)
print('Final state:')
print(final_state)
print('Statevectors equal?', initial_state.equiv(final_state))

# Visualize states on Bloch sphere
plot_bloch_multivector(initial_state)
plot_bloch_multivector(final_state)


# In[ ]:





# In[2]:


shor_encode = QuantumCircuit(6)


# In[3]:


from qiskit import QuantumCircuit

# Define shor_encode circuit
n = 9  # replace 9 with the actual number of qubits
shor_encode = QuantumCircuit(n)
# add gates to shor_encode circuit

# Define phaseflip_encode circuit
phaseflip_encode = QuantumCircuit(3)
phaseflip_encode.h(0)
phaseflip_encode.cx(0, 1)
phaseflip_encode.cx(0, 2)
phaseflip_encode.h(0)

# Compose circuits
shor_encode = shor_encode.compose(phaseflip_encode, qubits=range(0, n, 3))


# In[4]:


shor_encode = shor_encode.compose(bitflip_encode, qubits=[i for i in range(n) if i % 3 == 0])


# In[5]:


shor_correct = QuantumCircuit(n, name='shor_correct')


# In[6]:


initial_state.equiv(final_state)
initial_state.draw(output = 'bloch')
final_state.draw(output = 'bloch')


# In[7]:


state_fidelity([1, 0], [1, 0])


# In[8]:


from qiskit.quantum_info import state_fidelity
from qiskit import QuantumCircuit, Aer

# Create the two states
qc0 = QuantumCircuit(1)
qc1 = QuantumCircuit(1)
qc1.x(0)

# Get the statevectors
backend = Aer.get_backend('statevector_simulator')
sv0 = backend.run(qc0).result().get_statevector()
sv1 = backend.run(qc1).result().get_statevector()

# Calculate the state fidelity
fidelity = state_fidelity(sv0, sv1)
print("State fidelity between |0⟩ and |1⟩:", fidelity)


# In[9]:


from qiskit.quantum_info import Statevector
from qiskit.quantum_info import state_fidelity

# Define the two states
state1 = Statevector.from_label('1')
state2 = Statevector.from_label('0')

# Calculate the fidelity
fidelity = state_fidelity(state1, state2)

print(f"The state fidelity between |1⟩ and |0⟩ is: {fidelity}")


# In[10]:


from qiskit.quantum_info import Statevector
from qiskit.quantum_info import state_fidelity

# Define the two states
state_0 = Statevector.from_label('0')
state_plus = Statevector.from_label('+')

# Calculate the state fidelity
fidelity = state_fidelity(state_0, state_plus)

print("State fidelity between |0> and |+>:", fidelity)


# In[11]:


from qiskit.quantum_info import state_fidelity
from qiskit import QuantumCircuit, Aer, execute

# Define the circuits
qc0 = QuantumCircuit(1)
qc1 = QuantumCircuit(1)
qc1.x(0)
qc1.h(0)
# Calculate the state fidelities
backend = Aer.get_backend('statevector_simulator')
state0 = execute(qc0, backend).result().get_statevector()
state1 = execute(qc1, backend).result().get_statevector()
fidelity = state_fidelity(state0, state1)
print("The state fidelity between |0⟩ and |−⟩ is:", fidelity)


# In[12]:


qc = QuantumCircuit(1)
qc.x(0)
initial_state = Statevector.from_instruction(qc)

# Apply the H-gate to create the |−⟩ state
qc.h(0)
final_state = Statevector.from_instruction(qc)

state_fidelity(initial_state, final_state)


# In[13]:


from qiskit.quantum_info import Statevector
from qiskit.quantum_info import state_fidelity
from qiskit.circuit.library import HGate, CXGate

# Create initial state |00>
qc = QuantumCircuit(2)
initial_state = Statevector.from_instruction(qc)

# Create final state |𝛽00⟩
qc.h(0)
qc.cx(0, 1)
final_state = Statevector.from_instruction(qc)

# Calculate state fidelity between initial and final state
fidelity = state_fidelity(initial_state, final_state)

print(f"The state fidelity between |00⟩ and 𝛽00⟩ is: {fidelity}")


# In[14]:


from qiskit.quantum_info import state_fidelity

fidelity = state_fidelity(initial_state, final_state)
print("State fidelity:", fidelity)


# In[ ]:




