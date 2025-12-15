from typing import Dict, List
from django.db import transaction
from ..models import PlacementTest, PlacementTest_Question, PlacementTestResult, Level
from ..constants import LEVEL_WEIGHTS, LEVEL_THRESHOLDS


class PlacementTestService:
    """Сервис для работы с Placement тестами"""

    @staticmethod
    def get_placement_questions(
            test: PlacementTest,
            questions_per_level: int = 5
    ) -> List[PlacementTest_Question]:
        """
        Получить вопросы для Placement теста

        Args:
            test: Placement тест
            questions_per_level: Количество вопросов на уровень

        Returns:
            Список вопросов (перемешанный)
        """
        import random

        questions_qs = test.questions.all()
        levels = questions_qs.values_list('level_id', flat=True).distinct().order_by('level_id')

        selected = []

        for level_id in levels:
            level_questions = list(questions_qs.filter(level_id=level_id))

            if len(level_questions) <= questions_per_level:
                selected.extend(level_questions)
            else:
                selected.extend(random.sample(level_questions, questions_per_level))

        random.shuffle(selected)
        return selected

    @staticmethod
    def determine_level(level_results: Dict[str, int], total_questions: int) -> str:
        """
        Определить уровень пользователя по результатам

        Args:
            level_results: {'A1': 3, 'A2': 2, ...}
            total_questions: Общее количество вопросов

        Returns:
            Название уровня (например, 'B2')
        """
        # Рассчитываем взвешенный счет
        weighted_score = sum(
            level_results.get(level, 0) * weight
            for level, weight in LEVEL_WEIGHTS.items()
        )

        # Рассчитываем процент правильных ответов
        total_correct = sum(level_results.values())
        percentage = (total_correct / total_questions * 100) if total_questions > 0 else 0

        # Определяем уровень по порогам
        for level, threshold in sorted(LEVEL_THRESHOLDS.items(), key=lambda x: -x[1]):
            if percentage >= threshold:
                return level

        return 'A1'  # По умолчанию

    @staticmethod
    @transaction.atomic
    def check_placement_answers(
            test: PlacementTest,
            answers: Dict[int, str],
            user_name: str,
            user_email: str
    ) -> PlacementTestResult:
        """
        Проверка ответов Placement теста

        Args:
            test: Placement тест
            answers: {question_id: answer}
            user_name: Имя пользователя
            user_email: Email пользователя

        Returns:
            Результат Placement теста
        """
        questions = test.questions.filter(id__in=answers.keys()).select_related('level')

        level_results = {
            'A1': 0, 'A2': 0, 'B1': 0,
            'B2': 0, 'C1': 0, 'C2': 0
        }

        for question in questions:
            user_answer = answers.get(question.id, '')

            if question.is_correct(user_answer):
                level_title = question.level.title if question.level else 'A1'
                level_results[level_title] = level_results.get(level_title, 0) + 1

        total_questions = len(questions)

        determined_level_title = PlacementTestService.determine_level(
            level_results,
            total_questions
        )

        determined_level = Level.objects.filter(title=determined_level_title).first()

        result = PlacementTestResult.objects.create(
            test=test,
            name=user_name,
            email=user_email,
            total_questions=total_questions,
            level_a1_correct=level_results.get('A1', 0),
            level_a2_correct=level_results.get('A2', 0),
            level_b1_correct=level_results.get('B1', 0),
            level_b2_correct=level_results.get('B2', 0),
            level_c1_correct=level_results.get('C1', 0),
            level_c2_correct=level_results.get('C2', 0),
            level=determined_level
        )

        return result

    @staticmethod
    def get_level_breakdown(result: PlacementTestResult) -> Dict:
        return {
            'A1': {
                'correct': result.level_a1_correct,
                'weight': LEVEL_WEIGHTS['A1']
            },
            'A2': {
                'correct': result.level_a2_correct,
                'weight': LEVEL_WEIGHTS['A2']
            },
            'B1': {
                'correct': result.level_b1_correct,
                'weight': LEVEL_WEIGHTS['B1']
            },
            'B2': {
                'correct': result.level_b2_correct,
                'weight': LEVEL_WEIGHTS['B2']
            },
            'C1': {
                'correct': result.level_c1_correct,
                'weight': LEVEL_WEIGHTS['C1']
            },
            'C2': {
                'correct': result.level_c2_correct,
                'weight': LEVEL_WEIGHTS['C2']
            },
        }