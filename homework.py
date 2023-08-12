class InfoMessage():
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
    LEN_STEP = 0.65
    M_IN_KM = 1000
    CH_IN_M = 60

    def get_distance(self, LEN_STEP=0.65) -> float:
        """Получить дистанцию в км."""
        return self.action * LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(Training.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories)


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79
    name = 'Бег'

    def get_distance(self):
        return super().get_distance(LEN_STEP=0.65)

    def get_mean_speed(self):
        return super().get_mean_speed()

    def get_spent_calories(self):
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / self.M_IN_KM
                * self.duration * self.CH_IN_M)

    def show_training_info(self):
        return (InfoMessage(Running.__name__, self.duration,
                            self.get_distance(), self.get_mean_speed(),
                            self.get_spent_calories()))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height
    KOEF_1 = 0.035
    KOEF_2 = 0.029
    KMH_IN_MIM = 0.278
    SM_IN_M = 100

    def get_distance(self):
        return super().get_distance(LEN_STEP=0.65)

    def get_mean_speed(self):
        return super().get_mean_speed()

    def get_spent_calories(self):
        return ((self.KOEF_1 * self.weight + (((self.get_mean_speed()
                 * self.KMH_IN_MIM)**2) / (self.height / self.SM_IN_M))
                 * self.KOEF_2 * self.weight) * self.duration * self.CH_IN_M)

    def show_training_info(self):
        return InfoMessage(SportsWalking.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Swimming(Training):
    """Тренировка: плавание."""
    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
    KONST1 = 1.1
    KONST2 = 2  # Пришлось дописать везде константы из-за pytest
    LEN_STEP = 1.38  # Зачем так делать, если проще сделать, как у меня

    def get_distance(self):
        return super().get_distance(LEN_STEP=1.38)  # Тут указывается константа

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self):
        return ((self.get_mean_speed() + self.KONST1) * self.KONST2
                * self.weight * self.duration)

    def show_training_info(self):
        return InfoMessage(Swimming.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


def read_package(workout_type: str, data: list) -> Training:  # Реализовать
    """Прочитать данные полученные от датчиков."""            # через словарь?
    if workout_type == 'SWM':
        action, duration, weight, length_pool, count_pool = data
        return Swimming(action, duration, weight, length_pool, count_pool)
    elif workout_type == 'RUN':
        action, duration, weight = data
        return Running(action, duration, weight)
    elif workout_type == 'WLK':
        action, duration, weight, height = data
        return SportsWalking(action, duration, weight, height)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())
    return


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
