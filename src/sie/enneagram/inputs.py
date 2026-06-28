"""Assessment input models including supplementary non-question data."""

from __future__ import annotations

from dataclasses import dataclass, field

from sie.enneagram.profile import EpisodeSample
from sie.enneagram.types import Center


@dataclass
class EpisodeInput:
    """Free-text episodes that refine type scoring."""

    recent_conflict: str = ""
    core_values: str = ""
    emotion_handling: str = ""


@dataclass
class BehaviorLog:
    """Multiple-choice behavior patterns."""

    work_role: int = 0
    relationship_tendency: int = 0
    stress_reaction: int = 0


@dataclass
class SelfOtherGap:
    """Gap between self-image and others' perception — key type indicator."""

    self_image: dict[str, int] = field(default_factory=dict)
    others_image: dict[str, int] = field(default_factory=dict)


@dataclass
class AssessmentInput:
    """All answers and supplementary data for a full assessment."""

    center_answers: dict[str, int] = field(default_factory=dict)
    center_tiebreak_answers: dict[str, int] = field(default_factory=dict)
    center_tiebreak_pair: tuple[Center, Center] | None = None
    type_answers: dict[str, int] = field(default_factory=dict)
    type_tiebreak_answers: dict[str, int] = field(default_factory=dict)
    type_tiebreak_pair: tuple[int, int] | None = None
    type_reconfirm_center: Center | None = None
    type_reconfirm_answers: dict[str, int] = field(default_factory=dict)
    type_reconfirm_tiebreak_answers: dict[str, int] = field(default_factory=dict)
    type_reconfirm_tiebreak_pair: tuple[int, int] | None = None
    wing_answers: dict[str, int] = field(default_factory=dict)
    instinct_answers: dict[str, int] = field(default_factory=dict)

    episodes: EpisodeInput = field(default_factory=EpisodeInput)
    behavior_log: BehaviorLog | None = None
    self_other_gap: SelfOtherGap | None = None
    episode_samples: list[EpisodeSample] = field(default_factory=list)
