from frescura.nutricion import nutricion_por_porcion


def test_por_defecto_son_100_gramos():
    datos = nutricion_por_porcion("banano")
    assert datos["gramos"] == 100
    assert datos["energia_kcal"] == 89


def test_escala_con_los_gramos():
    datos = nutricion_por_porcion("aguacate_hass", 150)
    assert datos["energia_kcal"] == 250.5
    assert datos["potasio_mg"] == 760.5


def test_producto_sin_datos():
    assert nutricion_por_porcion("pitahaya") is None
