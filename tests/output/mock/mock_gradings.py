import datetime
from typing import List
from shapely.geometry import Polygon

from generator.business.model.grading import Grading
from generator.business.model.isochrone import Isochrone
from generator.business.model.stop_grade import StopGrade

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
    ]
]

b_1_polygon = [
    [
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
    ]
]

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

b_5_polygon = [
    [
        9.51343059539795,
        46.86382963439154
    ],
    [
        9.509868621826172,
        46.861042005044446
    ],
    [
        9.51317310333252,
        46.85743254360235
    ],
    [
        9.520726203918455,
        46.85752058213418
    ],
    [
        9.522442817687988,
        46.86203969954759
    ],
    [
        9.51343059539795,
        46.86382963439154
    ]
]

a_5_polygon = [
    [
        9.513988494873045,
        46.862274448500976
    ],
    [
        9.512829780578613,
        46.860102981516896
    ],
    [
        9.516520500183105,
        46.85840095951342
    ],
    [
        9.524030685424805,
        46.86030839431691
    ],
    [
        9.5216703414917,
        46.861511510649535
    ],
    [
        9.513988494873045,
        46.862274448500976
    ]
]

c_6_polygon = [
    [
        9.520297050476074,
        46.865267407682865
    ],
    [
        9.518494606018066,
        46.861276758360205
    ],
    [
        9.524674415588377,
        46.85813684781527
    ],
    [
        9.53038215637207,
        46.862245104937955
    ],
    [
        9.526047706604004,
        46.8653847752311
    ],
    [
        9.520468711853027,
        46.865267407682865
    ],
    [
        9.520297050476074,
        46.865267407682865
    ]
]


c_7_polygon = [
    [
        9.509096145629881,
        46.85458588662081
    ],
    [
        9.50613498687744,
        46.85071184296253
    ],
    [
        9.51042652130127,
        46.847013631506876
    ],
    [
        9.516692161560059,
        46.85261955089992
    ],
    [
        9.509096145629881,
        46.85458588662081
    ]
]

d_8_polygon = [
    [
        9.509224891662598,
        46.852149967540875
    ],
    [
        9.506950378417969,
        46.85062379326795
    ],
    [
        9.509224891662598,
        46.849126926374936
    ],
    [
        9.51265811920166,
        46.85091729168854
    ],
    [
        9.509224891662598,
        46.852149967540875
    ]
]


def mock_gradings_non_intercepting():
    # intersects nothing
    grade_c_4 = _create_grading(StopGrade.C, c_4_polygon, 750)
    return {
        4: [grade_c_4]
    }


def mock_gradings_intercepting_same_grade():
    # intersects a_3_polygon of same grade
    grade_a_2 = _create_grading(StopGrade.A, a_2_polygon, 300)
    # intersects a_2_polygon of same grade
    grade_a_3 = _create_grading(StopGrade.A, a_3_polygon, 300)
    return {
        2: [grade_a_2],
        3: [grade_a_3]
    }


def mock_gradings_same_uic_ref_overlapping():
    # intersects b_1_polygon of lower grade with same uic_ref
    grade_a_1 = _create_grading(StopGrade.A, a_1_polygon, 300)
    # intersects a_1_polygon of higher grade with same uic_ref
    grade_b_1 = _create_grading(StopGrade.B, b_1_polygon, 500)
    return {
        1: [grade_a_1, grade_b_1]
    }


def mock_gradings_different_uic_ref_overlapping():
    # d_8_polygon is completely overlapped by c_7_polygon and thus will be deleted
    grade_c_7 = _create_grading(StopGrade.C, c_7_polygon, 750)
    grade_d_8 = _create_grading(StopGrade.D, d_8_polygon, 1000)
    return {
        7: [grade_c_7],
        8: [grade_d_8]
    }


def mock_gradings_different_uic_ref_and_grades():
    # a_5_polygon intersects b_5_polygon and c_6_polygon intersects a_5_polygon and b_5_polygon
    grade_a_5 = _create_grading(StopGrade.A, a_5_polygon, 300)
    grade_b_5 = _create_grading(StopGrade.B, b_5_polygon, 500)
    grade_c_6 = _create_grading(StopGrade.C, c_6_polygon, 750)
    return {
        5: [grade_a_5, grade_b_5],
        6: [grade_c_6]
    }


def _create_grading(grade: StopGrade, points: List[List[float]], distance: int) -> Grading:
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
