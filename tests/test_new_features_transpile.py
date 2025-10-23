from qupac.parser import parse_qupac
from qupac.transpiler import transpile_to_python


def test_transpile_barrier():
    src = """
qubits: 2
barrier
""".strip()
    ir = parse_qupac(src)
    py = transpile_to_python(ir)
    assert "qc.barrier()" in py


def test_transpile_barrier_specific():
    src = """
qubits: 3
barrier 0,2
""".strip()
    ir = parse_qupac(src)
    py = transpile_to_python(ir)
    assert "qc.barrier(0, 2)" in py


def test_transpile_global_phase():
    src = """
qubits: 1
phase: pi/2
""".strip()
    ir = parse_qupac(src)
    py = transpile_to_python(ir)
    assert "qc.global_phase = (pi/2)" in py


def test_transpile_u_gate():
    src = """
qubits: 1
apply U(pi/2, 0, pi) to 0
""".strip()
    ir = parse_qupac(src)
    py = transpile_to_python(ir)
    assert "qc.u((pi/2), 0, pi, 0)" in py


def test_transpile_p_gate():
    src = """
qubits: 1
apply P(pi/4) to 0
""".strip()
    ir = parse_qupac(src)
    py = transpile_to_python(ir)
    assert "qc.p((pi/4), 0)" in py


def test_transpile_gate_inverse():
    src = """
qubits: 1
apply H inv to 0
""".strip()
    ir = parse_qupac(src)
    py = transpile_to_python(ir)
    assert "qc.h(0).inverse()" in py


def test_transpile_gate_power():
    src = """
qubits: 1
apply X power(3) to 0
""".strip()
    ir = parse_qupac(src)
    py = transpile_to_python(ir)
    assert "qc.x(0).power(3)" in py


def test_transpile_sdg_tdg_sx():
    src = """
qubits: 1
apply Sdg to 0
apply Tdg to 0
apply SX to 0
apply SXdg to 0
""".strip()
    ir = parse_qupac(src)
    py = transpile_to_python(ir)
    assert "qc.sdg(0)" in py
    assert "qc.tdg(0)" in py
    assert "qc.sx(0)" in py
    assert "qc.sxdg(0)" in py


def test_transpile_cp_gate():
    src = """
qubits: 2
apply CP(pi/2) from 0 to 1
""".strip()
    ir = parse_qupac(src)
    py = transpile_to_python(ir)
    assert "qc.cp((pi/2), 0, 1)" in py


def test_transpile_identity_gate():
    src = """
qubits: 1
apply I to 0
""".strip()
    ir = parse_qupac(src)
    py = transpile_to_python(ir)
    assert "qc.id(0)" in py


def test_transpile_rotation_with_inverse():
    src = """
qubits: 1
apply RY(pi/3) inv to 0
""".strip()
    ir = parse_qupac(src)
    py = transpile_to_python(ir)
    assert "qc.ry((pi/3), 0).inverse()" in py
