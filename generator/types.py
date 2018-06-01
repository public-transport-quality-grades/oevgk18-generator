from typing import List, Dict, Optional

from .business.model.public_transport_group import PublicTransportGroup
from .business.model.stop_category import StopCategory
from .business.model.transport_stop import TransportStop
from .business.model.stop_grade import StopGrade
from .business.model.grading import Grading
from .business.model.isochrone import Isochrone

TransportGroups = Dict[TransportStop, PublicTransportGroup]
TransportStopCategories = Dict[int, StopCategory]
TransportStopGradings = Dict[int, List[Grading]]

DistanceGradeMapping = Dict[float, StopGrade]
Intervals = Dict[TransportStop, Optional[float]]
Isochrones = Dict[int, List[Isochrone]]
