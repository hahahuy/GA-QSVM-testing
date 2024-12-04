import qiskit
import qiskit.quantum_info as qi
import numpy as np, typing, types
from qiskit.primitives import Sampler
# from qiskit.providers.aer import noise
# from qiskit.ignis.mitigation.measurement import complete_meas_cal, CompleteMeasFitter
from ..backend import constant


# def generate_depolarizing_noise_model(prob: float) -> noise.NoiseModel:
#     """As its function name

#     Args:
#         - prob (float): from 0 to 1

#     Returns:
#         - qiskit.providers.aer.noise.NoiseModel: new noise model
#     """
#     prob_1 = prob  # 1-qubit gate
#     prob_2 = prob  # 2-qubit gate

#     # Depolarizing quantum errors
#     error_1 = noise.depolarizing_error(prob_1, 1)
#     error_2 = noise.depolarizing_error(prob_2, 2)

#     # Add errors to noise model
#     noise_model = noise.NoiseModel()
#     noise_model.add_all_qubit_quantum_error(error_1, ['u1', 'u2', 'u3'])
#     noise_model.add_all_qubit_quantum_error(
#         error_2, ['cx', 'cz', 'crx', 'cry', 'crz'])
#     return noise_model


# def generate_noise_model(num_qubit: int, error_prob: float) -> noise.NoiseModel:
#     """Create readout noise model

#     Args:
#         - num_qubit (int): number of qubit
#         - error_prob (float):from 0 to 1

#     Returns:
#         - qiskit.providers.aer.noise.NoiseModel: new noise model
#     """
#     noise_model = noise.NoiseModel()
#     for qi in range(num_qubit):
#         read_err = noise.errors.readout_error.ReadoutError(
#             [[1 - error_prob, error_prob], [error_prob, 1 - error_prob]])
#         noise_model.add_readout_error(read_err, [qi])
#     return noise_model


# def generate_measurement_filter(num_qubits: int, noise_model) -> CompleteMeasFitter:
#     """_summary_

#     Args:
#         - num_qubits (int)
#         - noise_model

#     Returns:
#         - CompleteMeasFitter
#     """
#     # for running measurement error mitigation
#     meas_cals, state_labels = complete_meas_cal(qubit_list=range(
#         num_qubits), qr=qiskit.QuantumRegister(num_qubits))
#     # Execute the calibration circuits
#     job = qiskit.execute(meas_cals, backend=constant.backend,
#                          shots=constant.NUM_SHOTS, noise_model=noise_model)
#     cal_results = job.result()
#     # Make a calibration matrix
#     meas_filter = CompleteMeasFitter(cal_results, state_labels).filter
#     return meas_filter


def measure(qc: qiskit.QuantumCircuit, parameter_values: np.ndarray = [], mode = constant.MEASURE_MODE):
    """Measuring the quantu circuit which fully measurement gates

    Args:
        - qc (QuantumCircuit): Measured circuit
        - qubits (np.ndarray): List of measured qubit

    Returns:
        - float: Frequency of 00.. cbit
    """
    if len(parameter_values) == 0:
        qc.measure_all()
        sampler = Sampler()
        result = sampler.run(qc, shots = 10000).result().quasi_dists[0].get(0, 0)
    else:
        if constant.MEASURE_MODE == constant.MeasureMode.THEORY.value:
            operator = qi.DensityMatrix(qc.assign_parameters(parameter_values)).data
            result = np.real(operator[0][0])
        elif constant.MEASURE_MODE == constant.MeasureMode.EXPERIMENT.value:
            qc.measure_all()
            sampler = Sampler()
            result = sampler.run(qc, parameter_values=parameter_values, shots = 10000).result().quasi_dists[0].get(0, 0)
        
        elif constant.MEASURE_MODE == constant.MeasureMode.SIMULATE.value:
            # from . import state
            # operator = qi.DensityMatrix(constant.UVDAGGER.assign_parameters(parameter_values)).data
            # result = np.real(operator[0][0])
            # print(constant.UVDAGGER.assign_parameters(parameter_values).draw())
            # print('True: ', result)
            psi = constant.PSI     
            # print("Psi: ", psi)
            # print(qc.assign_parameters(parameter_values).compose(state.specific(psi).inverse()).draw())
            # operator = qi.DensityMatrix(qc.assign_parameters(parameter_values).compose(state.specific(psi).inverse())).data
            # result1 = np.real(operator[0][0])
            # print('True_U: ', result1)
            # THIS QC is JUST U, NOT UVDAGGER
            phi_theta = qi.Statevector.from_instruction(qc.assign_parameters(parameter_values)).data
            result = np.real(np.dot(np.conjugate(psi), phi_theta))**2
            # print("Result_U: ", result2)
            # print(np.abs(result - result2))
    return result
    # The below is old version
    # n = len(qubits)
    # if cbits == []:
    #     cbits = qubits.copy()
    # if qc.num_clbits == 0:
    #     cr = qiskit.ClassicalRegister(qc.num_qubits, 'c')
    #     qc.add_register(cr)
    # for i in range(0, n):
    #     qc.measure(qubits[i], cbits[i])
    # # qc.measure_all() # 
    # if qsee.constant.NOISE_PROB > 0:
    #     noise_model = generate_noise_model(
    #         n, qsee.constant.NOISE_PROB)
    #     results = qiskit.execute(qc, backend=qsee.constant.backend,
    #                              noise_model=noise_model,
    #                              shots=qsee.constant.NUM_SHOTS).result()
    #     # Raw counts
    #     counts = results.get_counts()
    #     # Mitigating noise based on https://qiskit.org/textbook/ch-quantum-hardware/measurement-error-mitigation.html
    #     meas_filter = generate_measurement_filter(
    #         n, noise_model=noise_model)
    #     # # Mitigated counts
    #     counts = meas_filter.apply(counts.copy())
    # else:
    #     counts = qiskit.execute(
    #         qc, backend=qsee.constant.backend #,shots=qsee.constant.NUM_SHOTS
    #     ).result().get_counts()

    # return counts.get("0" * len(qubits), 0) / qsee.constant.NUM_SHOTS



def x_measurement(qc: qiskit.QuantumCircuit, qubits, cbits=[]):
    """As its function name

    Args:
        - qc (qiskit.QuantumCircuit): measuremed circuit
        - qubits (np.ndarray): list of measuremed qubit
        - cbits (list, optional): classical bits. Defaults to [].

    Returns:
        - qiskit.QuantumCircuit: added measure gates circuit
    """
    if cbits == []:
        cbits = qubits.copy()
    for i in range(0, len(qubits)):
        qc.h(qubits[i])
        qc.measure(qubits[i], cbits[i])
    return qc


def y_measurement(qc: qiskit.QuantumCircuit, qubits, cbits=[]):
    """As its function name

    Args:
        - qc (qiskit.QuantumCircuit): measuremed circuit
        - qubits (np.ndarray): list of measuremed qubit
        - cbits (list, optional): classical bits. Defaults to [].

    Returns:
        - qiskit.QuantumCircuit: added measure gates circuit
    """
    if cbits == []:
        cbits = qubits.copy()
    for i in range(0, len(qubits)):
        qc.sdg(qubits[i])
        qc.h(qubits[i])
        qc.measure(qubits[i], cbits[i])
    return qc


def z_measurement(qc: qiskit.QuantumCircuit, qubits, cbits=[]):
    """As its function name

    Args:
        - qc (qiskit.QuantumCircuit): measuremed circuit
        - qubits (np.ndarray): list of measuremed qubit
        - cbits (list, optional): classical bits. Defaults to [].

    Returns:
        - qiskit.QuantumCircuit: added measure gates circuit
    """
    if cbits == []:
        cbits = qubits.copy()
    for i in range(0, len(qubits)):
        qc.measure(qubits[i], cbits[i])
    return qc
