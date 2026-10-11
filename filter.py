from config.config import POSITIVE_KEYWORDS, NEGATIVE_KEYWORDS


class LeadFilter:
    """Фильтр для классификации сообщений на релевантные лиды"""

    def __init__(self):
        self.positive = [kw.lower() for kw in POSITIVE_KEYWORDS]
        self.negative = [kw.lower() for kw in NEGATIVE_KEYWORDS]

    def is_relevant(self, text: str) -> bool:
        """
        Проверяет, является ли сообщение релевантным лидом

        Args:
            text: Текст сообщения

        Returns:
            True если сообщение релевантно, False в противном случае
        """
        if not text:
            return False

        text_lower = text.lower()

        # Проверка на минус-слова
        for negative_kw in self.negative:
            if negative_kw in text_lower:
                return False

        # Проверка на наличие хотя бы одного позитивного ключевого слова
        for positive_kw in self.positive:
            if positive_kw in text_lower:
                return True

        return False

    def get_category(self, text: str) -> str:
        """
        Определяет категорию лида

        Args:
            text: Текст сообщения

        Returns:
            Категория лида
        """
        if not text:
            return "Разработка"

        text_lower = text.lower()

        design_keywords = ["дизайн", "ui/ux", "ui ux", "figma", "дизайнер"]
        frontend_keywords = ["верстка", "верстальщик", "frontend", "фронтенд", "html", "css", "react"]

        for kw in design_keywords:
            if kw in text_lower:
                return "Веб-дизайн"

        for kw in frontend_keywords:
            if kw in text_lower:
                return "Верстка / Frontend"

        return "Разработка сайтов"
