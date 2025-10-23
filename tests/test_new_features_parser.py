from qupac.parser import parse_qupac


def test_parse_barrier_all():
    src = """
qubits: 2
barrier
""".strip()
    ir = parse_qupac(src)
    ops = ir["ops"]
    assert any(o.get("op") == "barrier" and "qubits" not in o for o in ops)


def test_parse_barrier_specific():
    src = """
qubits: 3
barrier 0,2
""".strip()
    ir = parse_qupac(src)
    ops = ir["ops"]
    assert any(o.get("op") == "barrier" and o.get("qubits") == [0, 2] for o in ops)


def test_parse_global_phase():
    src = """
qubits: 1
phase: pi/4
""".strip()
    ir = parse_qupac(src)
    assert ir.get("global_phase") == "(pi/4)"


def test_parse_u_gate():
    src = """
qubits: 1
apply U(pi/2, 0, pi) to 0
""".strip()
    ir = parse_qupac(src)
    ops = ir["ops"]
    assert any(
        o.get("op") == "apply" 
        and o.get("gate") == "U" 
        and len(o.get("params", [])) == 3
        for o in ops
    )


def test_parse_p_gate():
    src = """
qubits: 1
apply P(pi/4) to 0
""".strip()
    ir = parse_qupac(src)
    ops = ir["ops"]
    assert any(
        o.get("op") == "apply" 
        and o.get("gate") == "P" 
        and len(o.get("params", [])) == 1
        for o in ops
    )


def test_parse_gate_inverse():
    src = """
qubits: 1
apply H inv to 0
""".strip()
    ir = parse_qupac(src)
    ops = ir["ops"]
    assert any(
        o.get("op") == "apply" 
        and o.get("gate") == "H" 
        and o.get("modifier", {}).get("type") == "inverse"
        for o in ops
    )


def test_parse_gate_power():
    src = """
qubits: 1
apply X power(2) to 0
""".strip()
    ir = parse_qupac(src)
    ops = ir["ops"]
    assert any(
        o.get("op") == "apply" 
        and o.get("gate") == "X" 
        and o.get("modifier", {}).get("type") == "power"
        for o in ops
    )


def test_parse_sdg_tdg_sx():
    src = """
qubits: 1
apply Sdg to 0
apply Tdg to 0
apply SX to 0
""".strip()
    ir = parse_qupac(src)
    ops = ir["ops"]
    assert any(o.get("gate") == "Sdg" for o in ops)
    assert any(o.get("gate") == "Tdg" for o in ops)
    assert any(o.get("gate") == "SX" for o in ops)


def test_parse_cp_gate():
    src = """
qubits: 2
apply CP(pi/2) from 0 to 1
""".strip()
    ir = parse_qupac(src)
    ops = ir["ops"]
    assert any(
        o.get("op") == "apply" 
        and o.get("gate") == "CP"
        and o.get("controls") == [0]
        and o.get("targets") == [1]
        for o in ops
    )
