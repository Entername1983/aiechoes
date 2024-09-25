from typing import Optional

from pydantic import BaseModel

from app.schemas.config import config


class Event(BaseModel):
    model_config = config
    id: str
    date: str
    time: Optional[str] = None
    event: str


class Locations(BaseModel):
    model_config = config
    id: str
    name: str
    description: Optional[str] = None
    significance: Optional[str] = None
    coordinates: Optional[dict] = None
    history: Optional[list[str]] = None
    builtYear: Optional[int] = None
    currentCondition: Optional[str] = None


class Setting(BaseModel):
    model_config = config
    timePeriod: str
    timeline: list[Event]
    locations: list[Locations]


class Background(BaseModel):
    model_config = config
    occupation: str
    hometown: str
    family: dict
    education: str
    history: str


class Relationship(BaseModel):
    model_config = config
    characterId: str
    relationshipType: str
    history: str
    currentStatus: str


class Character(BaseModel):
    model_config = config
    id: str
    firstName: str
    lastName: Optional[str] = None
    nickname: Optional[str] = None
    age: int
    background: Optional[Background] = None
    traits: list[str]
    goals: list[str]
    relationships: list[Relationship]


class PlotPoint(BaseModel):
    model_config = config
    id: str
    title: str
    description: str
    status: str
    date: str
    charactersInvolved: list[str]
    dependencies: list[str]
    relatedSubplots: list[str]


class NarrationRules(BaseModel):
    model_config = config
    perspective: str | None = None
    access: str | None = None
    limitations: str | None = None
    tone: str | None = None
    style: str | None = None
    tense: str | None = None


class Narrator(BaseModel):
    model_config = config
    id: str
    characterId: str
    name: str
    rules: NarrationRules


class CharacterNameAndId(BaseModel):
    model_config = config
    characterId: str
    name: str


class LocationNameAndId(BaseModel):
    model_config = config
    locationId: str
    name: str
    details: str


class CurrentContext(BaseModel):
    model_config = config
    time: str
    location: LocationNameAndId
    weather: str
    charactersPresent: list[CharacterNameAndId]
    summary: str
    characterStates: dict
    narrator: str
    mainPlot: str
    subPlot: str


class Rules(BaseModel):
    model_config = config
    characterIntroduction: str
    locationDescription: str
    dialogue: str
    plotConsistency: str
    foreshadowing: str
    style: str


class AllCharacters(BaseModel):
    model_config = config
    mainCharacters: list[Character]
    secondaryCharacters: list[Character]


class Narration(BaseModel):
    model_config = config
    narrators: list[Narrator]
    narrationRules: NarrationRules
    currentNarrator: str


class StoryContext(BaseModel):
    model_config = config
    setting: Optional[Setting] = None
    characters: Optional[AllCharacters] = None
    mainPlots: Optional[list[PlotPoint]] = None
    subPlots: Optional[list[PlotPoint]] = None
    themes: Optional[list[str]] = None
    narration: Optional[Narration] = None
    currentContext: Optional[CurrentContext] = None
    rules: Optional[Rules] = None


#### llm_response_models


class CharacterEnteringLeavingResponse(BaseModel):
    model_config = config
    characters: list[CharacterNameAndId]
    leaving: bool
    entering: bool


class CharactersToUpdateResponse(BaseModel):
    model_config = config
    characterId: list[CharacterNameAndId]
    updated: bool


class CharacterUpdateResponse(BaseModel):
    model_config = config
    characer: Character


class LocationChangedResponse(BaseModel):
    model_config = config
    changed: bool


class AddNewLocationResponse(BaseModel):
    model_config = config
    location: Locations


class CurrentContextSummaryData(BaseModel):
    model_config = config
    mainPlot: Optional[PlotPoint] = None
    subPlot: Optional[PlotPoint] = None
    mainCharacters: list[Character]
    secondaryCharacters: list[Character]
    narrator: Optional[Narrator] = None
    themes: list[str]
    location: Optional[LocationNameAndId] = None
    time: Optional[str] = None
    weather: Optional[str] = None


class EnteringCharacterResponse(BaseModel):
    model_config = config
    existing_characters: list[CharacterNameAndId]
    new_characters: list[CharacterNameAndId]


class ChangingCharacter(BaseModel):
    characterId: str
    name: str
    changes: str


class ListOfChangingCharactersResponse(BaseModel):
    charactersChanged: bool
    changes: list[ChangingCharacter]
