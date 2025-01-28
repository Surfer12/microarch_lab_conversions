import unittest
from .learning_pathways import LearningState, AdaptiveLearningPathway, DifficultyLevel

class TestLearningPathways(unittest.TestCase):
    def setUp(self):
        self.learning_state = LearningState()
        self.learning_pathway = AdaptiveLearningPathway(initial_state=self.learning_state)

    def test_initialization(self):
        # Test default initialization
        self.assertEqual(self.learning_state.difficulty_level, DifficultyLevel.BEGINNER)
        self.assertEqual(len(self.learning_state.completed_challenges), 0)

    def test_difficulty_adjustment(self):
        # Simulate challenge results to test difficulty adjustment
        self.learning_state.update_profile({'solving_time': 20, 'error_rate': 0.05})
        self.assertEqual(self.learning_state.difficulty_level, DifficultyLevel.INTERMEDIATE)

        self.learning_state.update_profile({'solving_time': 130, 'error_rate': 0.35})
        self.assertEqual(self.learning_state.difficulty_level, DifficultyLevel.BEGINNER)

    def test_generate_challenge(self):
        # Test challenge generation
        challenge = self.learning_pathway.generate_challenge()
        self.assertIn('source_base', challenge)
        self.assertIn('target_base', challenge)
        self.assertIn('value', challenge)
        self.assertIn('difficulty_level', challenge)

    def test_submit_challenge_result(self):
        # Test submitting a challenge result
        challenge = self.learning_pathway.generate_challenge()
        result = {
            'solving_time': 50,
            'error_rate': 0.1,
            'challenge': challenge
        }
        self.learning_pathway.submit_challenge_result(result)
        self.assertEqual(len(self.learning_state.completed_challenges), 1)

if __name__ == '__main__':
    unittest.main()