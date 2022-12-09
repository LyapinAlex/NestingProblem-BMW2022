from copy import copy


def pack_item(item, pallets, t_vector, r, best_rotation):
    item.t_vector = [t_vector, r]
    item.packed = True
    item.best_rotation = best_rotation
    for s in range(len(item.segments[best_rotation])):
        for l in range(len(item.segments[best_rotation][s])):
            new_line = [copy(item.segments[best_rotation][s][l][0]) + copy(item.t_vector[0]), copy(item.segments[best_rotation][s][l][1]) + copy(item.t_vector[0])]
            pallets.pallet_lines[r+s].append(copy(new_line))
        pallets.pallet_lines[r+s].sort(key=lambda x: int(x[0]), reverse=False)

    def first_elem(e):
      return e[0]

    for line in pallets.pallet_lines:
        for segment in line:
            segment.sort()
        line.sort(key=first_elem)
        i = 0
        while i < (len(line) - 1):
            if line[i][1] == line[i+1][0]:
                line[i][1] = line[i+1][1]
                line.pop(i+1)
                continue
            if line[i][1] > line[i+1][0]:
                if line[i][1] < line[i+1][1]:
                    line[i][1] = line[i+1][1]
                    line.pop(i+1)
                    continue
                elif line[i][1] >= line[i+1][1]:
                    line.pop(i+1)
                    continue
            i+=1

def pack_segments(items, pallets):
    for item in items:
        best_height = 10000
        best_t_vector = None
        best_rotation = None
        best_r = None
        for rotation in range(item.rotation + 1):
            segments = copy(item.segments[rotation])
            r = 0
            finish_flag = 0
            while r < len(pallets.pallet_lines) and item.packed == False and finish_flag == 0:
                row = pallets.pallet_lines[r]
                k = 1
                ex_flag = 0
                while k < len(row) and item.packed == False and ex_flag == 0:
                    t_vector = row[k-1][1] - segments[0][0][0]
                    i = 0
                    # l = len(segments[0])
                    while i < len(segments) and r + i < len(pallets.pallet_lines) and ex_flag == 0:
                            j = 0
                            while j < len(segments[i]) and ex_flag == 0:
                                m = 0
                                while m < len(pallets.pallet_lines[r+i]) and ex_flag == 0:
                                    # случаи пересечения линии и упаковки
                                    if segments[i][j][1] + t_vector > pallets.shape[0]:
                                        ex_flag = 1
                                    elif pallets.pallet_lines[r+i][m][0] <= segments[i][j][0] + t_vector < pallets.pallet_lines[r+i][m][1] and segments[i][j][0] + t_vector != segments[i][j][1] + t_vector:
                                        t_vector = pallets.pallet_lines[r+i][m][1]
                                        i = 0
                                        j = 0
                                    elif pallets.pallet_lines[r+i][m][0] < segments[i][j][1] + t_vector <= pallets.pallet_lines[r+i][m][1] and segments[i][j][0] + t_vector != segments[i][j][1] + t_vector:
                                        t_vector = pallets.pallet_lines[r+i][m][1]
                                        i = 0
                                        j = 0
                                    elif segments[i][j][0] + t_vector < pallets.pallet_lines[r + i][m][0] and \
                                            pallets.pallet_lines[r + i][m][1] < segments[i][j][1] + t_vector:
                                        t_vector = pallets.pallet_lines[r + i][m][1]
                                        i = 0
                                        j = 0
                                    elif segments[i][j][0] + t_vector < 0:
                                        t_vector = - segments[i][j][0]
                                        i = 0
                                        j = 0

                                    m += 1
                                j += 1
                            i += 1
                    # если объект влезает, добавляем его на палету
                    if ex_flag == 0:
                        # pack_item(item, pallets, t_vector, r)
                        if best_height > r :
                            best_height = copy(r)
                            best_r = copy(r)
                            best_t_vector = copy(t_vector)
                            best_rotation = copy(rotation)
                        finish_flag = 1
                        ex_flag = 1
                    k += 1
                r += 1
        pack_item(item, pallets, best_t_vector, best_r, best_rotation)

    return None
