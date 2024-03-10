import strawberry
from fastapi import HTTPException
from typing import Optional
from .typeDefs import *
from context import db

"""
Query & Mutation
"""

api_url = 'http://115.145.36.151:8893'


@strawberry.type
class Query:
    """Strawberry always requires a Query type to be defined
    """
    @strawberry.field
    def info() -> str:
        return "This is the API of DAPR project"
    
    @strawberry.field
    def sketch(self, sketchId: int) -> SketchCollectResult:
        sketch = db.sketch.find_first(
            where={"id": sketchId},
            include={
                'participant': True,
                'sketchInfo': True,
            }
        )

        if not sketch:
            raise HTTPException(status_code=400, detail='No sketch found')

        return sketch

    @strawberry.field
    def getSketchCollectResultBySketchId(self,  sketch_id: int) -> Optional[SketchCollectResult]:
        return db.sketch.find_unique(where={"id": sketch_id}, include={"participant": True})


@strawberry.type
class Mutation:
    """Mutation about Manager
    """
    @strawberry.mutation
    async def createParticipant(self, input: ParticipantInput) -> Optional[Participant]:

        input_data = {
            'age': input.age,
            'gender': input.gender,
        }

        newParticpant = await db.participant.create(
            data=input_data
        )
        return newParticpant

    @strawberry.mutation
    async def createSketch(self, input: SketchInput) -> Optional[Sketch]:
        input_data = {
            'participantId': input.participantId,
            'strokes': input.strokes,
            'image': input.image,
            'allowToPublic': input.allowToPublic,
            'startedAt': input.startedAt,
            'endedAt': input.endedAt,
        }

        newSketch = await db.sketch.create(
            data=input_data
        )

        return newSketch

    @strawberry.mutation
    async def updateSketchSurvey(self, input: SketchSurveyInput) -> Optional[Sketch]:
        input_data = {
            'survey': input.survey,
        }

        updatedSketch = await db.sketch.update(
            data=input_data,
            where={
                'id': input.id
            }
        )
        return updatedSketch
    