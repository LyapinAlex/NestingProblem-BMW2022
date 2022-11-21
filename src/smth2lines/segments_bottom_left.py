from copy import copy


def pack_item(item, pallets, t_vector, r):
    print()
    item.t_vector = [t_vector, r]
    item.packed = True
    for s in range(len(item.segments)):
        for l in range(len(item.segments[s])):
            new_line = [copy(item.segments[s][l][0]) + copy(item.t_vector[0]), copy(item.segments[s][l][1]) + copy(item.t_vector[0])]
            pallets.pallet_lines[r+s].append(copy(new_line))
        pallets.pallet_lines[r+s].sort(key=lambda x: int(x[0]), reverse=False)
        print('строка', r+s , ':', pallets.pallet_lines[r+s])

def pack_segments(items, pallets):
    for item in items:
        r = 0
        while r < len(pallets.pallet_lines) and item.packed == False:
            row = pallets.pallet_lines[r]
            k = 1
            ex_flag = 0
            while k < len(row) and item.packed == False and ex_flag == 0:
                t_vector = row[k-1][1] - item.segments[0][0][0]
                i = 0
                l = len(item.segments[0])
                while i < len(item.segments) and r + i < len(pallets.pallet_lines) and ex_flag == 0:
                        j = 0
                        while j < len(item.segments[i]) and ex_flag == 0:
                            m = 0
                            while m < len(pallets.pallet_lines[r+i]) and ex_flag == 0:
                                # случаи пересечения линии и упаковки
                                if pallets.pallet_lines[r+i][m][0] <= item.segments[i][j][0] + t_vector < pallets.pallet_lines[r+i][m][1]:
                                    t_vector += pallets.pallet_lines[r+i][m][1] - (item.segments[i][j][0] + t_vector)
                                    i = 0
                                elif pallets.pallet_lines[r+i][m][0] <= item.segments[i][j][1] + t_vector < pallets.pallet_lines[r+i][m][1]:
                                    t_vector += pallets.pallet_lines[r+i][m][1] - (item.segments[i][j][0] + t_vector)
                                    i = 0
                                # объект выходит за границы палеты
                                elif item.segments[i][j][0] + t_vector < 0:
                                    t_vector = - item.segments[i][j][0]
                                    i = 0
                                # наверное надо сделать это первым условием, будет чаще всего встречаться
                                elif item.segments[i][j][1] + t_vector > pallets.shape[0]:
                                    ex_flag = 1
                                m += 1
                            j += 1
                        i+=1
                # если объект влезает, добавляем его на палету
                if ex_flag == 0:
                    pack_item(item, pallets, t_vector, r)
                    ex_flag = 1
                k+=1
            r+=1

    return
