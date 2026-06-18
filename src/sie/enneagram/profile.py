"""Enneagram assessment result model for S.I.E."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypedDict


InstinctualVariant = Literal["sp", "so", "sx"]


class EpisodeSample(TypedDict):
    event: str
    feeling: str
    action: str
    result: str


@dataclass
class EnneagramProfile:
    primary_type: int
    wing: int | None
    scores: dict[int, float]

    summary: str
    strengths: list[str]
    blind_spots: list[str]

    stress_pattern: int
    growth_pattern: int
    instinctual_variant: InstinctualVariant

    core_fear: str
    core_desire: str

    communication_style: str
    conflict_pattern: str
    relationship_needs: list[str]

    childhood_wound: str | None
    episode_samples: list[EpisodeSample]
