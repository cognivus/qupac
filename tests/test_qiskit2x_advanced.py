from qupac.parser import parse_qupac
from qupac.transpiler import transpile_to_python


def test_parse_ecr_gate():
    src = """
qubits: 2
apply ECR from 0 to 1
""".strip()
    ir = parse_qupac(src)
    ops = ir["ops"]
    assert any(
        o.get("op") == "apply" 
        and o.get("gate") == "ECR"
        and o.get("controls") == [0]
        and o.get("targets") == [1]
        for o in ops
    )


def test_transpile_ecr_gate():
    src = """
qubits: 2
apply ECR from 0 to 1
""".strip()
    ir = parse_qupac(src)
    py = transpile_to_python(ir)
    assert "qc.ecr(0, 1)" in py


def test_parse_iswap_gate():
    src = """
qubits: 2
apply iSWAP from 0 to 1
""".strip()
    ir = parse_qupac(src)
    ops = ir["ops"]
    assert any(
        o.get("op") == "apply" 
        and o.get("gate") == "iSWAP"
        for o in ops
    )


def test_transpile_iswap_gate():
    src = """
qubits: 2
apply iSWAP from 0 to 1
""".strip()
    ir = parse_qupac(src)
    py = transpile_to_python(ir)
    assert "qc.iswap(0, 1)" in py


def test_parse_crx_gate():
    src = """
qubits: 2
apply CRX(pi/2) from 0 to 1
""".strip()
    ir = parse_qupac(src)
    ops = ir["ops"]
    assert any(
        o.get("op") == "apply" 
        and o.get("gate") == "CRX"
        and len(o.get("params", [])) == 1
        for o in ops
    )


def test_transpile_crx_gate():
    src = """
qubits: 2
apply CRX(pi/4) from 0 to 1
""".strip()
    ir = parse_qupac(src)
    py = transpile_to_python(ir)
    assert "qc.crx((pi/4), 0, 1)" in py


def test_parse_cry_gate():
    src = """
qubits: 2
apply CRY(pi/3) from 0 to 1
""".strip()
    ir = parse_qupac(src)
    ops = ir["ops"]
    assert any(
        o.get("op") == "apply" 
        and o.get("gate") == "CRY"
        for o in ops
    )


def test_transpile_cry_gate():
    src = """
qubits: 2
apply CRY(pi/3) from 0 to 1
""".strip()
    ir = parse_qupac(src)
    py = transpile_to_python(ir)
    assert "qc.cry((pi/3), 0, 1)" in py


def test_parse_crz_gate():
    src = """
qubits: 2
apply CRZ(pi/6) from 0 to 1
""".strip()
    ir = parse_qupac(src)
    ops = ir["ops"]
    assert any(
        o.get("op") == "apply" 
        and o.get("gate") == "CRZ"
        for o in ops
    )


def test_transpile_crz_gate():
    src = """
qubits: 2
apply CRZ(pi/6) from 0 to 1
""".strip()
    ir = parse_qupac(src)
    py = transpile_to_python(ir)
    assert "qc.crz((pi/6), 0, 1)" in py


def test_parse_delay():
    src = """
qubits: 2
delay(100) on 0,1
""".strip()
    ir = parse_qupac(src)
    ops = ir["ops"]
    assert any(
        o.get("op") == "delay"
        and o.get("qubits") == [0, 1]
        for o in ops
    )


def test_transpile_delay():
    src = """
qubits: 2
delay(100) on 0,1
""".strip()
    ir = parse_qupac(src)
    py = transpile_to_python(ir)
    assert "qc.delay(100, 0)" in py
    assert "qc.delay(100, 1)" in py


def test_parse_save_statevector():
    src = """
qubits: 2
save statevector as my_state
""".strip()
    ir = parse_qupac(src)
    ops = ir["ops"]
    assert any(
        o.get("op") == "save_statevector"
        and o.get("label") == "my_state"
        for o in ops
    )


def test_transpile_save_statevector():
    src = """
qubits: 2
entangle 0,1
save statevector as bell_state
""".strip()
    ir = parse_qupac(src)
    py = transpile_to_python(ir)
    assert "qc.save_statevector(label='bell_state')" in py


def test_combined_advanced_features():
    src = """
qubits: 3
apply H to 0
apply ECR from 0 to 1
delay(50) on 1
apply CRX(pi/4) from 1 to 2
barrier 0,1,2
save statevector as final_state
""".strip()
    ir = parse_qupac(src)
    py = transpile_to_python(ir)
    assert "qc.h(0)" in py
    assert "qc.ecr(0, 1)" in py
    assert "qc.delay(50, 1)" in py
    assert "qc.crx((pi/4), 1, 2)" in py
    assert "qc.barrier(0, 1, 2)" in py
    assert "qc.save_statevector(label='final_state')" in py
