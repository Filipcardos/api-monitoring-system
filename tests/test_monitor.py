from monitor import classificar


<<<<<<< HEAD
def test_classificar_ok():
    assert classificar(200, 100) == "OK"


def test_classificar_lento():
    assert classificar(200, 1500) == "LENTO"


def test_classificar_erro():
    assert classificar(500, 100) == "ERRO"
=======
def test_classificar_online():
    assert classificar(200, 100, slow_threshold=1000) == "ONLINE"


def test_classificar_slow():
    assert classificar(200, 1500, slow_threshold=1000) == "SLOW"


def test_classificar_error():
    assert classificar(500, 100, slow_threshold=1000) == "ERROR"


def test_classificar_timeout():
    assert classificar(None, None, slow_threshold=1000) == "TIMEOUT"
>>>>>>> master
