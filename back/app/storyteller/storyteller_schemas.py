from pydantic import BaseModel

from app.schemas.config import config


class Event(BaseModel):
    model_config = config
    event_id: str
    date: str
    time: str
    event: str


class Locations(BaseModel):
    model_config = config
    locationId: str
    name: str
    description: str
    significance: str
    coordinates: dict
    history: list[str]
    builtYear: int
    currentCondition: str


class Settings(BaseModel):
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
    lastName: str
    nickname: str
    age: int
    background: Background
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
    perspective: str
    access: str
    limitations: str
    tone: str
    style: str
    tense: str


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
    Narator: str
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


class StoryContext(BaseModel):
    model_config = config
    settings: Settings
    characters: AllCharacters
    mainPlots: list[PlotPoint]
    subPlots: list[PlotPoint]
    themes: list[str]
    narration: list[Narrator]
    currentContext: CurrentContext
    rules: Rules


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
    mainPlot: PlotPoint
    subPlot: PlotPoint
    mainCharacters: list[Character]
    secondaryCharacters: list[Character]
    Narator: Narrator
    themes: list[str]
    location: LocationNameAndId
    time: str
    weather: str


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
