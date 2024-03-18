from typing import NewType
from uuid import UUID


SeasonID = NewType("SeasonID", UUID)
TeamID = NewType("TeamID", UUID)
GameID = NewType("GameID", UUID)
