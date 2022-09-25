def get_pixel(li: list, iter: int):
    """
    По номеру пикселя в строке, возвращет содержание этого пикселя и номер ячейки в которой он содержится
    Returns:
        int: значение пикселя по iter
        i: номер ячейки к которой относится iter"""
    r = 0
    i = -1
    sign = 1
    while (r < iter + 1):
        i += 1
        r += abs(li[i])
    if li[i] < 0: sign = -1
    return sign * (r - iter), i