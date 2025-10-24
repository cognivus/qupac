from qupac.parser import parse_qupac
from qupac.transpiler import transpile_to_python


def test_parse_ch_gate():
    src = """
qubits: 2
apply CH from 0 to 1
""".strip()
    ir = parse_qupac(src)
    ops = ir["ops"]
    assert any(
        o.get("op") == "apply" 
        and o.get("gate") == "CH"
        and o.get("controls") == [0]
        and o.get("targets") == [1]
        for o in ops
    )


def test_transpile_ch_gate():
    src = """
qubits: 2
apply CH from 0 to 1
""".strip()
    ir = parse_qupac(src)
    py = transpile_to_python(ir)
    assert "qc.ch(0, 1)" in py


def test_parse_cs_gate():
    src = """
qubits: 2
apply CS from 0 to 1
""".strip()
    ir = parse_qupac(src)
    ops = ir["ops"]
    assert any(
        o.get("op") == "apply" 
        and o.get("gate") == "CS"
        for o in ops
    )


def test_transpile_cs_gate():
    src = """
qubits: 2
apply CS from 0 to 1
""".strip()
    ir = parse_qupac(src)
    py = transpile_to_python(ir)
    assert "qc.cs(0, 1)" in py


def test_parse_rxx_gate():
    src = """
qubits: 2
apply RXX(pi/2) from 0 to 1
""".strip()
    ir = parse_qupac(src)
    ops = ir["ops"]
    assert any(
        o.get("op") == "apply" 
        and o.get("gate") == "RXX"
        and len(o.get("params", [])) == 1
        for o in ops
    )


def test_transpile_rxx_gate():
    src = """
qubits: 2
apply RXX(pi/4) from 0 to 1
""".strip()
    ir = parse_qupac(src)
    py = transpile_to_python(ir)
    assert "qc.rxx((pi/4), 0, 1)" in py


def test_parse_ryy_gate():
    src = """
qubits: 2
apply RYY(pi/3) from 0 to 1
""".strip()
    ir = parse_qupac(src)
    ops = ir["ops"]
    assert any(
        o.get("op") == "apply" 
        and o.get("gate") == "RYY"
        for o in ops
    )


def test_transpile_ryy_gate():
    src = """
qubits: 2
apply RYY(pi/3) from 0 to 1
""".strip()
    ir = parse_qupac(src)
    py = transpile_to_python(ir)
    assert "qc.ryy((pi/3), 0, 1)" in py


def test_parse_rzz_gate():
    src = """
qubits: 2
apply RZZ(pi/6) from 0 to 1
""".strip()
    ir = parse_qupac(src)
    ops = ir["ops"]
    assert any(
        o.get("op") == "apply" 
        and o.get("gate") == "RZZ"
        for o in ops
    )


def test_transpile_rzz_gate():
    src = """
qubits: 2
apply RZZ(pi/6) from 0 to 1
""".strip()
    ir = parse_qupac(src)
    py = transpile_to_python(ir)
    assert "qc.rzz((pi/6), 0, 1)" in py


def test_parse_repeat_loop():
    src = """
qubits: 1
repeat 3
  apply H to 0
end
""".strip()
    ir = parse_qupac(src)
    ops = ir["ops"]
    assert any(
        o.get("op") == "repeat"
        and o.get("count") == 3
        for o in ops
    )


def test_transpile_repeat_loop():
    src = """
qubits: 1
repeat 5
  apply X to 0
end
""".strip()
    ir = parse_qupac(src)
    py = transpile_to_python(ir)
    assert "for _repeat_idx in range(5):" in py
    assert "qc.x(0)" in py


def test_combined_extra_features():
    src = """
qubits: 3
apply CH from 0 to 1
apply RXX(pi/4) from 1 to 2
repeat 2
  apply H to 0
end
barrier
""".strip()
    ir = parse_qupac(src)
    py = transpile_to_python(ir)
    assert "qc.ch(0, 1)" in py
    assert "qc.rxx((pi/4), 1, 2)" in py
    assert "for _repeat_idx in range(2):" in py
    assert "qc.barrier()" in py


def test_cs_with_measurements():
    src = """
qubits: 2
classical: 2
apply H to 0
apply CS from 0 to 1
measure all
simulate
""".strip()
    ir = parse_qupac(src)
    py = transpile_to_python(ir)
    assert "qc.h(0)" in py
    assert "qc.cs(0, 1)" in py
    assert "qc.measure" in py
