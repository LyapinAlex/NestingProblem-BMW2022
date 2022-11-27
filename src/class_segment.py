from shapely.geometry import LineString, Point
from class_direction import is_collinear

from class_vector import Vector


class Segment:
    @staticmethod
    def split_by_intersections(segments):
        i = 0
        while (i < len(segments)):
            j = i+1
            while (j < len(segments)):
                intersection = Segment.segment_intersection(
                    segments[i], segments[j])
                if (len(intersection) == 2):
                    left_point = min(
                        segments[i][0], segments[i][1], segments[j][0], segments[j][1])
                    right_point = max(
                        segments[i][0], segments[i][1], segments[j][0], segments[j][1])
                    segments[i][0] = left_point
                    segments[i][1] = right_point
                    del segments[j]
                    i -= 1
                    break
                if (segments[i][0] == segments[j][0] or segments[i][0] == segments[j][1] or segments[i][1] == segments[j][0] or segments[i][1] == segments[j][1]):
                    if (is_collinear(segments[i][0]-segments[i][1], segments[j][0]-segments[j][1]) or is_collinear(segments[i][1]-segments[i][0], segments[j][0]-segments[j][1])):
                        left_point = min(
                            segments[i][0], segments[i][1], segments[j][0], segments[j][1])
                        right_point = max(
                            segments[i][0], segments[i][1], segments[j][0], segments[j][1])
                        segments[i][0] = left_point
                        segments[i][1] = right_point
                        del segments[j]
                        i -= 1
                        break
                j += 1
            i += 1

        new_segments = []
        for i in range(len(segments)):
            intersections = [segments[i][0], segments[i][1]]
            for j in range(len(segments)):
                if (i != j and not (segments[i][0] == segments[j][0] or segments[i][0] == segments[j][1] or segments[i][1] == segments[j][0] or segments[i][1] == segments[j][1])):
                    intersection = Segment.segment_intersection(
                        segments[i], segments[j])
                    if (intersection):
                        intersections += intersection
            intersections = list(set(intersections))
            intersections.sort()
            for j in range(len(intersections)-1):
                if ([intersections[j], intersections[j+1]] not in new_segments):
                    new_segments.append([intersections[j], intersections[j+1]])

        return new_segments

    @staticmethod
    def segment_intersection(segment1, segment2):
        A = (segment1[0].x, segment1[0].y)
        B = (segment1[1].x, segment1[1].y)

        C = (segment2[0].x, segment2[0].y)
        D = (segment2[1].x, segment2[1].y)

        line_1 = LineString([A, B])
        line_2 = LineString([C, D])
        int_pt = line_1.intersection(line_2)
        if type(int_pt) == Point:
            return [Vector(float(int_pt.x), float(int_pt.y))]
        elif type(int_pt) == LineString:
            if (len(int_pt.bounds) == 0):
                return []
            return [Vector(float(int_pt.bounds[0]), float(int_pt.bounds[1])), Vector(float(int_pt.bounds[2]), float(int_pt.bounds[3]))]
