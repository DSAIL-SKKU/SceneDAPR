import strawberry
from typing import List, Optional

@strawberry.type
class Manager:
    id: int
    name: str
    email: str
    password: str
    role: str


@strawberry.type
class Sketch:
    id: int
    strokes: Optional[str] = None
    survey: Optional[str] = None
    image: Optional[str] = None
    imagePath: Optional[str] = None
    allowToPublic: bool
    startedAt: str
    endedAt: str


@strawberry.type
class Participant:
    id: int
    name: Optional[str] = None
    age: int
    gender:  str
    metaInfo: Optional[str] = None
    sketch: Optional[List[Sketch]] = None
    manager: Optional[Manager] = None
    managerId: Optional[int] = None


@strawberry.type
class SketchInfo:
    id: int
    sketchId: int
    categoryId: Optional[str] = None
    bbox: Optional[str] = None
    confidence: Optional[str] = None
    detectImagePath: Optional[str] = None
    stressScore: Optional[str] = None
    resourceScore: Optional[str] = None
    drawWequence: Optional[str] = None
    totalStroke: Optional[int] = None
    averageStrokeLength: Optional[float] = None
    rainArea: Optional[float] = None
    personArea: Optional[float] = None
    rainPersonDist: Optional[float] = None
    centerPersonDist: Optional[float] = None
    note: Optional[str] = None
    createdAt: str
    updatedAt: Optional[str] = None
    participant: Participant
    sketch: Sketch


@strawberry.type
class SketchCollectResult(Sketch):
    participant: Participant
    sketchInfo: Optional[SketchInfo] = None


@strawberry.type
class SketchDetect:
    id: int
    sketch: Sketch
    categoryId: str
    bbox: str
    confidence: str
    detectImagePath: str


"""
Input Types
- ParticipantInput
- SketchInput
- SketchInfoInput
"""


@strawberry.input
class ManagerInput:
    name: str
    email: str
    password: str


@strawberry.input
class ParticipantInput:
    name: str
    age: int
    gender:  str


@strawberry.input
class SketchInput:
    participantId: int
    strokes: str
    image: str
    allowToPublic: bool
    startedAt: str
    endedAt: str


@strawberry.input
class SketchSurveyInput:
    id: int
    survey: str

