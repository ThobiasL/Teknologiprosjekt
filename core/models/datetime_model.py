from time import strftime

class DateTimeModel:
    """Modell for dato- og tidsrelaterte funksjoner."""

    @staticmethod
    def get_datetime() -> str:
        """
        Henter nåværende dato og klokkeslett.
        :return: Streng med dato og klokkeslett i formatet 'DD.MM.YYYY HH:MM'.
        """
        return strftime("%d.%m.%Y %H:%M")

    @staticmethod
    def get_time() -> str:
        """
        Henter nåværende tid.
        :return: Streng med tid i formatet 'HH:MM:SS'.
        """
        return strftime("%H:%M:%S")