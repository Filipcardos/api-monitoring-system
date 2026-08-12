from monitor import classificar


def test_classificar_ok():
    assert classificar(200, 100) == "OK"


def test_classificar_lento():
    assert classificar(200, 1500) == "LENTO"


def test_classificar_erro():
    assert classificar(500, 100) == "ERRO"
