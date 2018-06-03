from generator.business.model.stop_grade import StopGrade
from .isochrone import Isochrone


class Grading:

    def __init__(self, isochrone: Isochrone, grade: StopGrade):
        self.isochrone: Isochrone = isochrone
        self.grade: StopGrade = grade

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
