"""Enneagram assessment result model for S.I.E."""

from __future__ import annotations

from dataclasses import dataclass, field
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
    reasoning: list[str] = field(default_factory=list)

    center_confidence: float = 0.0
    center_shares: dict[str, float] = field(default_factory=dict)
    center_low_confidence: bool = False

    type_confidence: float = 0.0
    type_question_confidence: float = 0.0
    type_shares_in_center: dict[int, float] = field(default_factory=dict)
    type_share_order: tuple[int, ...] = ()
    type_low_confidence: bool = False

    wing_confidence: float = 0.0
    wing_shares: dict[int, float] = field(default_factory=dict)
    wing_share_order: tuple[int, ...] = ()
    wing_low_confidence: bool = False

    center_changed_for_type: bool = False
    type_reconfirmed: bool = False
    type_supplemental_only: bool = False
