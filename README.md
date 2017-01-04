# Qubiter Quantum Compiler

##What is this?##
Qubiter Quantum Compiler is a collection of Python classes for decomposing an arbitrary unitary matrix into CNOTs and single qubit rotations using the (Cosine-Sine) CS decomposition of Linear Algebra. This is an addon for Qubiter https://github.com/artiste-qb-net/qubiter Just insert the contents of this repository into the folder called "quantum_compiler" in the main directory of Qubiter, and you are almost ready to go. 

The final step is to add some DLL's to your Python Interpreter. These DLL's contain a Python wrapper for the LAPACK subroutine cuncsd.f. More info on how to build these DLL's soon.

Qubiter Quantum Compiler is licensed under the GPLv.2 (Linux) license. See LICENSE.md. 

The main body of Qubiter at https://github.com/artiste-qb-net/qubiter is licensed under the BSD license (3 clause version) with an added clause at the end, taken almost verbatim from the Apache 2.0 license, granting additional Patent rights. 

##Contributors##

(Alphabetical Order)
* Dekant, Henning
* Tucci, Robert
