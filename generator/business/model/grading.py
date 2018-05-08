from .isochrone import Isochrone
from ..util.public_transport_stop_grade import PublicTransportStopGrade


class Grading:

    def __init__(self, isochrone: Isochrone, grade: PublicTransportStopGrade):
        self.isochrone: Isochrone = isochrone
        self.grade: PublicTransportStopGrade = grade

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__