from typing import List, Dict, Union, Optional
from dataclasses import dataclass, field
from enum import Enum, auto
import random
import math

class DifficultyLevel(Enum):
    """
    Cognitive complexity levels for adaptive learning.
    """
    BEGINNER = auto()
    INTERMEDIATE = auto()
    ADVANCED = auto()
    EXPERT = auto()

@dataclass
class LearningState:
    """
    Represents a learner's cognitive state and progression.
    """
    difficulty_level: DifficultyLevel = DifficultyLevel.BEGINNER
    completed_challenges: List[Dict] = field(default_factory=list)
    cognitive_profile: Dict = field(default_factory=dict)

    # Cognitive tracking metrics
    time_to_solve: List[float] = field(default_factory=list)
    error_rates: List[float] = field(default_factory=list)

    def update_profile(self, challenge_result: Dict) -> None:
        """
        Update learner's cognitive profile based on challenge performance.

        Args:
            challenge_result (Dict): Results of a completed challenge
        """
        self.completed_challenges.append(challenge_result)

        # Track solving time
        self.time_to_solve.append(challenge_result.get('solving_time', 0))

        # Track error rates
        self.error_rates.append(challenge_result.get('error_rate', 0))

        # Dynamically adjust difficulty
        self._adjust_difficulty()

    def _adjust_difficulty(self) -> None:
        """
        Dynamically adjust difficulty based on cognitive performance.
        """
        # If no data points, do nothing
        if not self.time_to_solve or not self.error_rates:
            return

        # Get the most recent performance metrics
        current_solving_time = self.time_to_solve[-1]
        current_error_rate = self.error_rates[-1]

        # Cognitive complexity heuristics
        if current_solving_time < 30 and current_error_rate < 0.1:
            self._increase_difficulty()
        elif current_solving_time > 120 or current_error_rate > 0.3:
            # For poor performance, always return to BEGINNER
            self.difficulty_level = DifficultyLevel.BEGINNER
            # Clear performance metrics to start fresh
            self.time_to_solve.clear()
            self.error_rates.clear()

    def _increase_difficulty(self) -> None:
        """Increase cognitive challenge level."""
        difficulty_mapping = {
            DifficultyLevel.BEGINNER: DifficultyLevel.INTERMEDIATE,
            DifficultyLevel.INTERMEDIATE: DifficultyLevel.ADVANCED,
            DifficultyLevel.ADVANCED: DifficultyLevel.EXPERT
        }
        self.difficulty_level = difficulty_mapping.get(
            self.difficulty_level,
            DifficultyLevel.EXPERT
        )

    def _decrease_difficulty(self) -> None:
        """Decrease cognitive challenge level."""
        difficulty_mapping = {
            DifficultyLevel.EXPERT: DifficultyLevel.ADVANCED,
            DifficultyLevel.ADVANCED: DifficultyLevel.INTERMEDIATE,
            DifficultyLevel.INTERMEDIATE: DifficultyLevel.BEGINNER
        }
        self.difficulty_level = difficulty_mapping.get(
            self.difficulty_level,
            DifficultyLevel.BEGINNER
        )

class AdaptiveLearningPathway:
    """
    Generates adaptive, personalized learning challenges for number system conversions.
    """

    def __init__(
        self,
        initial_state: Optional[LearningState] = None,
        min_base: int = 2,
        max_base: int = 36
    ):
        """
        Initialize adaptive learning pathway.

        Args:
            initial_state (Optional[LearningState]): Starting learner state
            min_base (int): Minimum base for challenges
            max_base (int): Maximum base for challenges
        """
        self.learning_state = initial_state or LearningState()
        self.min_base = min_base
        self.max_base = max_base

    def generate_challenge(self) -> Dict:
        """
        Generate a personalized number conversion challenge.

        Returns:
            Dict: Challenge specification with cognitive complexity metrics
        """
        # Dynamically select bases based on difficulty
        base_complexity_map = {
            DifficultyLevel.BEGINNER: (2, 10),
            DifficultyLevel.INTERMEDIATE: (2, 16),
            DifficultyLevel.ADVANCED: (2, 36),
            DifficultyLevel.EXPERT: (2, 36)
        }

        min_base, max_base = base_complexity_map[self.learning_state.difficulty_level]

        source_base = random.randint(min_base, max_base)
        target_base = random.randint(min_base, max_base)

        # Generate challenge value with complexity based on difficulty
        value_complexity = {
            DifficultyLevel.BEGINNER: (0, 100),
            DifficultyLevel.INTERMEDIATE: (0, 1000),
            DifficultyLevel.ADVANCED: (0, 10000),
            DifficultyLevel.EXPERT: (0, 1000000)
        }

        min_value, max_value = value_complexity[self.learning_state.difficulty_level]

        # Include possibility of fractional values at higher difficulties
        is_fractional = (
            self.learning_state.difficulty_level in
            [DifficultyLevel.ADVANCED, DifficultyLevel.EXPERT]
        ) and random.random() < 0.3

        if is_fractional:
            integer_part = random.randint(min_value, max_value)
            fractional_part = round(random.random(), 3)
            value = integer_part + fractional_part
        else:
            value = random.randint(min_value, max_value)

        # Generate cognitive complexity metrics
        challenge = {
            "source_base": source_base,
            "target_base": target_base,
            "value": value,
            "difficulty_level": self.learning_state.difficulty_level.name,
            "cognitive_complexity": self._calculate_challenge_complexity(
                source_base,
                target_base,
                value
            )
        }

        return challenge

    def _calculate_challenge_complexity(
        self,
        source_base: int,
        target_base: int,
        value: Union[int, float]
    ) -> float:
        """
        Calculate cognitive complexity of a challenge.

        Args:
            source_base (int): Source base
            target_base (int): Target base
            value (Union[int, float]): Challenge value

        Returns:
            float: Cognitive complexity score
        """
        base_difference = abs(source_base - target_base)
        value_magnitude = abs(value)

        complexity = (
            base_difference *
            (1 + math.log(value_magnitude + 1)) /
            math.log(max(source_base, target_base))
        )

        return min(complexity, 10.0)  # Cap complexity

    def submit_challenge_result(self, result: Dict) -> None:
        """
        Submit challenge result and update learning state.

        Args:
            result (Dict): Challenge result with solving metrics
        """
        # Validate result structure
        required_keys = ['solving_time', 'error_rate', 'challenge']
        if not all(key in result for key in required_keys):
            raise ValueError("Invalid challenge result structure")

        # Update learning state based on performance
        self.learning_state.update_profile(result)
