import unittest
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from educational.learning_pathways import LearningState, AdaptiveLearningPathway, DifficultyLevel
from core.conversion_engine import convert_number

class TestAdaptiveLearningPathway(unittest.TestCase):

    def setUp(self):
        self.pathway = AdaptiveLearningPathway()

    def test_initial_state(self):
        self.assertEqual(self.pathway.learning_state.difficulty_level, DifficultyLevel.BEGINNER)
        self.assertEqual(len(self.pathway.learning_state.completed_challenges), 0)

    def test_generate_challenge(self):
        challenge = self.pathway.generate_challenge()
        self.assertIn('source_base', challenge)
        self.assertIn('target_base', challenge)
        self.assertIn('value', challenge)
        self.assertIn('difficulty_level', challenge)
        self.assertIn('cognitive_complexity', challenge)

    def test_evaluate_correct_answer(self):
        challenge = self.pathway.generate_challenge()
        correct_answer = convert_number(
            challenge['value'],
            challenge['source_base'],
            challenge['target_base']
        )
        user_answer = str(correct_answer)
        result = self.pathway.evaluate_answer(challenge, user_answer)
        self.assertTrue(result['is_correct'])
        self.assertEqual(result['error_rate'], 0)

    def test_evaluate_incorrect_answer(self):
        challenge = self.pathway.generate_challenge()
        user_answer = "incorrect_answer"
        result = self.pathway.evaluate_answer(challenge, user_answer)
        self.assertFalse(result['is_correct'])
        self.assertEqual(result['error_rate'], 1)

    def test_submit_challenge_result_increases_difficulty(self):
        # Simulate correct answers to increase difficulty
        for _ in range(3):
            challenge = self.pathway.generate_challenge()
            correct_answer = convert_number(
                challenge['value'],
                challenge['source_base'],
                challenge['target_base']
            )
            result = {
                'challenge': challenge,
                'is_correct': True,
                'solving_time': 25.0,  # Fast solving time
                'error_rate': 0.0,
                'user_answer': str(correct_answer),
                'correct_answer': correct_answer
            }
            initial_level = self.pathway.learning_state.difficulty_level
            self.pathway.submit_challenge_result(result)
            if initial_level != DifficultyLevel.EXPERT:
                expected_level = DifficultyLevel(
                    list(DifficultyLevel)[list(DifficultyLevel).index(initial_level) + 1]
                )
                self.assertEqual(self.pathway.learning_state.difficulty_level, expected_level)
            else:
                self.assertEqual(self.pathway.learning_state.difficulty_level, DifficultyLevel.EXPERT)

if __name__ == '__main__':
    unittest.main()