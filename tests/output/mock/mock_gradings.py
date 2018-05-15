import datetime
from typing import List
from shapely.geometry import Polygon

from generator.business.model.grading import Grading
from generator.business.model.isochrone import Isochrone
from generator.business.util.public_transport_stop_grade import PublicTransportStopGrade

a_1_polygon = [
    [
        9.52538251876831,
        46.85436577799184
    ], [
        9.524309635162354,
        46.852091269332334
    ], [
        9.525661468505858,
        46.8497139379716
    ], [
        9.529480934143066,
        46.84958186092171
    ], [
        9.532163143157959,
        46.85213529299477
    ], [
        9.530553817749022,
        46.85424838635416
    ], [
        9.52538251876831,
        46.85436577799184
    ]]

b_1_polygon = [[
    9.524867534637451,
    46.8551434911099
], [
    9.522120952606201,
    46.85169505474643
], [
    9.524331092834473,
    46.848040938008346
], [
    9.530317783355713,
    46.847688720849746
], [
    9.533772468566895,
    46.85041834341926
], [
    9.534823894500732,
    46.85251682989097
], [
    9.532527923583984,
    46.85529022817105
], [
    9.524867534637451,
    46.8551434911099
]]

a_2_polygon = [
    [
        9.539780616760254,
        46.86092462800162
    ],
    [
        9.53832149505615,
        46.85884114279012
    ],
    [
        9.542291164398193,
        46.85702169521199
    ],
    [
        9.543921947479248,
        46.8588851609193
    ],
    [
        9.539780616760254,
        46.86092462800162
    ]
]

a_3_polygon = [
    [
        9.537248611450195,
        46.85696300232818
    ],
    [
        9.539995193481445,
        46.8551434911099
    ],
    [
        9.542548656463623,
        46.856155968670215
    ],
    [
        9.541969299316406,
        46.85821021230618
    ],
    [
        9.539201259613037,
        46.85887048821356
    ],
    [
        9.537248611450195,
        46.85696300232818
    ]]

c_4_polygon = [
    [
        9.541218280792236,
        46.853485334454284
    ],
    [
        9.538986682891846,
        46.850873267027694
    ],
    [
        9.542527198791504,
        46.84977263877843
    ],
    [
        9.544157981872557,
        46.85150428371813
    ],
    [
        9.541218280792236,
        46.853485334454284
    ]]


def mock_gradings():
    # intersects b_1_polygon of lower grade
    grade_a_1 = _create_grading(PublicTransportStopGrade.A, a_1_polygon, 300)
    # intersects a_1_polygon of higher grade
    grade_b_1 = _create_grading(PublicTransportStopGrade.B, b_1_polygon, 500)

    # intersects a_3_polygon of same grade
    grade_a_2 = _create_grading(PublicTransportStopGrade.A, a_2_polygon, 300)
    # intersects a_2_polygon of same grade
    grade_a_3 = _create_grading(PublicTransportStopGrade.A, a_3_polygon, 300)

    # intersects nothing
    grade_c_4 = _create_grading(PublicTransportStopGrade.C, c_4_polygon, 750)

    return {1: [grade_a_1, grade_b_1], 2: [grade_a_2], 3: [grade_a_3], 4: [grade_c_4]}


def _create_grading(grade: PublicTransportStopGrade, points: List[List[float]], distance: int) -> Grading:
    isochrone = _create_isochrone(points, distance)
    return Grading(isochrone, grade)


def _create_isochrone(points: List[List[float]], distance: int) -> Isochrone:
    polygon = Polygon([point for point in points])
    return Isochrone(distance, polygon)


def _create_diff_of_gradings(a: Grading, b: Grading) -> Grading:
    diff = a.isochrone.polygon.difference(b.isochrone.polygon)
    return Grading(Isochrone(a.isochrone.distance, diff), a.grade)


def mock_output_config() -> dict:
    return {
        'output-directory': 'results/',
        'styling': {'opacity': 0.6,
                    'colors': {'A': '#700038',
                               'B': '#BC42FF',
                               'C': '#9966FF',
                               'D': '#00B000',
                               'E': '#B3FF40',
                               'F': '#DEF325'
                               }
                    }
    }


def mock_due_date_config() -> dict:
    return {
        'type-of-day': 'Working Day',
        'type-of-interval': 'Day',
        'due-date': datetime.datetime(2018, 11, 13, 0, 0),
        'lower-bound': '06:00',
        'upper-bound': '20:00'
    }