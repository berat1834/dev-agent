def topla(a: int | float, b: int | float) -> int | float:
    """
    İki sayıyı toplar ve sonucu döndürür.

    Bu fonksiyon, verilen iki sayısal değeri (tam sayı veya ondalıklı sayı)
    toplar ve toplamın sonucunu geri verir.

    Args:
        a (int | float): Toplanacak birinci sayı.
        b (int | float): Toplanacak ikinci sayı.

    Returns:
        int | float: İki sayının toplamı.

    Examples:
        >>> topla(5, 3)
        8
        >>> topla(2.5, 3.5)
        6.0
        >>> topla(-10, 20)
        10
    """
    return a + b