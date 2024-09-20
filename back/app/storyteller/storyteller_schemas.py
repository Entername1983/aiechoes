from typing import Optional

from pydantic import BaseModel

from app.schemas.config import config


class Event(BaseModel):
    model_config = config
    event_id: str | None
    date: str | None
    time: str | None
    event: str | None


class Locations(BaseModel):
    model_config = config
    name: str | None
    description: str | None
    significance: str | None
    coordinates: dict
    history: list[str | None]
    builtYear: int | None
    currentCondition: str | None


class Settings(BaseModel):
    model_config = config
    timePeriod: str | None
    timeline: list[Event]
    locations: list[Locations]


class Background(BaseModel):
    model_config = config
    occupation: str | None
    hometown: str | None
    family: dict
    education: str | None
    history: str | None


class Relationship(BaseModel):
    model_config = config
    characterId: str | None
    relationshipType: str | None
    history: str | None
    currentStatus: str | None


class Character(BaseModel):
    model_config = config
    id: str | None
    firstName: str | None
    lastName: str | None
    nickname: str | None
    age: int
    background: Background | None
    traits: list[str | None]
    goals: list[str | None]
    relationships: list[Relationship] | None


class PlotPoint(BaseModel):
    model_config = config
    id: str | None
    title: str | None
    description: str | None
    status: str | None
    date: str | None
    charactersInvolved: list[str | None]
    dependencies: list[str | None]
    relatedSubplots: list[str | None]


class NarrationRules(BaseModel):
    model_config = config
    perspective: str | None
    access: str | None
    limitations: str | None
    tone: str | None
    style: str | None
    tense: str | None


class Narrator(BaseModel):
    model_config = config
    id: str | None
    characterId: str | None
    name: str | None
    rules: NarrationRules


class CurrentContext(BaseModel):
    model_config = config
    time: str | None
    location: str | None
    weather: str | None
    charactersPresent: list[str | None]
    summary: str | None
    characterStates: dict
    Narator: str | None
    mainPlot: str | None
    subPlot: str | None


class CurrentContextSummaryData(BaseModel):
    model_config = config
    mainPlot: PlotPoint | None
    subPlot: PlotPoint | None
    mainCharacters: list[Character | None]
    secondaryCharacters: list[Character | None]
    Narator: Narrator | None
    themes: list[str | None]
    location: str | None
    time: str | None
    weather: str | None


class Rules(BaseModel):
    model_config = config
    characterIntroduction: str | None
    locationDescription: str | None
    dialogue: str | None
    plotConsistency: str | None
    foreshadowing: str | None
    style: str | None


class AllCharacters(BaseModel):
    mainCharacters: list[Character | None] | None
    secondaryCharacters: list[Character | None] | None


class StoryContext(BaseModel):
    model_config = config
    settings: Optional[Settings] = None
    characters: Optional[AllCharacters] = None
    mainPlots: Optional[list[PlotPoint]] = None
    subPlots: Optional[list[PlotPoint]] = None
    themes: Optional[list[str]] = None
    narration: Optional[list[Narrator]] = None
    currentContext: Optional[CurrentContext] = None
    rules: Optional[Rules] = None
