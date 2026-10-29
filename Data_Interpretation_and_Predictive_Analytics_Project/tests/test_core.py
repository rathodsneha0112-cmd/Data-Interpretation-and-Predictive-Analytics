"""Core data and scoring sanity checks; uses only the Python standard library."""
import unittest
from questions import MODULES, QUESTIONS
from quiz_engine import Quiz


class QuestionBankTests(unittest.TestCase):
    def test_expected_module_and_question_counts(self):
        self.assertEqual(len(MODULES), 6)
        self.assertEqual(len(QUESTIONS), 90)
        self.assertEqual(set(q["module"] for q in QUESTIONS), set(MODULES))

    def test_question_schema_and_answer_indexes(self):
        for q in QUESTIONS:
            with self.subTest(question=q["question"]):
                self.assertTrue(q["question"])
                self.assertEqual(len(q["options"]), 4)
                self.assertIsInstance(q["answer"], int)
                self.assertGreaterEqual(q["answer"], 0)
                self.assertLess(q["answer"], len(q["options"]))
                self.assertTrue(q["explanation"])

    def test_every_module_has_fifteen_questions(self):
        for module in MODULES:
            with self.subTest(module=module):
                self.assertEqual(sum(q["module"] == module for q in QUESTIONS), 15)

    def test_every_module_has_five_questions_per_level(self):
        for module in MODULES:
            for level in ("Easy", "Medium", "Hard"):
                with self.subTest(module=module, level=level):
                    self.assertEqual(sum(q["module"] == module and q["level"] == level for q in QUESTIONS), 5)

    def test_quiz_score_and_module_breakdown(self):
        quiz = Quiz("Clock", 10)
        self.assertEqual(len(quiz.qs), 10)
        for i, question in enumerate(quiz.qs):
            quiz.answer(i, question["answer"])
        self.assertEqual(quiz.score(), 10)
        self.assertEqual(quiz.by_module()["Clock"], [10, 10])


if __name__ == "__main__":
    unittest.main()
