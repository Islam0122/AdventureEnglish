from typing import Dict, List, Optional
from django.db import transaction
from django.db.models import QuerySet
from ..models import Test, Question, ResultsTest


class TestService:
    """Сервис для работы с обычными тестами"""

    @staticmethod
    def get_test_questions(
            test: Test,
            randomize: bool = True,
            limit: Optional[int] = None
    ) -> List[Question]:
        """
        Получить вопросы теста

        Args:
            test: Тест
            randomize: Перемешать вопросы
            limit: Ограничить количество вопросов

        Returns:
            Список вопросов
        """
        questions = test.questions.filter(is_active=True)

        if randomize:
            questions = questions.order_by('?')
        else:
            questions = questions.order_by('order', 'id')

        if limit:
            questions = questions[:limit]

        return list(questions)

    @staticmethod
    @transaction.atomic
    def check_answers(
            test: Test,
            answers: Dict[int, str],
            user_name: str,
            user_email: str
    ) -> ResultsTest:
        """
        Проверка ответов и создание результата

        Args:
            test: Тест
            answers: {question_id: answer}
            user_name: Имя пользователя
            user_email: Email пользователя

        Returns:
            Результат теста
        """
        questions = test.questions.filter(id__in=answers.keys())

        correct_count = 0
        total_score = 0
        max_score = 0

        for question in questions:
            max_score += question.points
            user_answer = answers.get(question.id, '')

            if question.is_correct(user_answer):
                correct_count += 1
                total_score += question.points

        total_questions = len(questions)
        wrong_count = total_questions - correct_count

        # Расчет процента
        percentage = round((correct_count / total_questions) * 100, 2) if total_questions > 0 else 0

        # Создание результата
        result = ResultsTest.objects.create(
            test=test,
            name=user_name,
            email=user_email,
            total_questions=total_questions,
            correct_answers=correct_count,
            wrong_answers=wrong_count,
            score=total_score,
            percentage=percentage
        )

        return result

    @staticmethod
    def get_user_attempts(test: Test, user_email: str) -> QuerySet:
        """Получить попытки пользователя для теста"""
        return ResultsTest.objects.filter(
            test=test,
            email=user_email
        ).order_by('-created_at')

    @staticmethod
    def calculate_statistics(test: Test) -> Dict:
        """Рассчитать статистику теста"""
        results = ResultsTest.objects.filter(test=test)

        if not results.exists():
            return {
                'total_attempts': 0,
                'average_score': 0,
                'pass_rate': 0,
                'average_time': 0,
            }

        from django.db.models import Avg, Count

        stats = results.aggregate(
            total=Count('id'),
            avg_score=Avg('percentage')
        )

        passed = results.filter(percentage__gte=test.passing_score).count()

        return {
            'total_attempts': stats['total'],
            'average_score': round(stats['avg_score'] or 0, 2),
            'pass_rate': round((passed / stats['total']) * 100, 2) if stats['total'] > 0 else 0,
        }