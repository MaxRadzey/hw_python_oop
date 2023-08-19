from dataclasses import dataclass, asdict


@dataclass
class InfoMessage():
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE = ('Тип тренировки: {training_type}; '
               'Длительность: {duration:.3f} ч.; '
               'Дистанция: {distance:.3f} км; '
               'Ср. скорость: {speed:.3f} км/ч; '
               'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65  # Const for convert steps
    M_IN_KM: int = 1000  # Const for convert meters in kilometers
    MIN_IN_H: int = 60  # Const for convert hours in minutes

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18  # Const for convert calories
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79  # Const for convert calories

    def get_spent_calories(self):
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_MULTIPLIER: float = 0.035  # Const for get calories
    CALORIES_SHIFT: float = 0.029  # Const for get calories
    KMH_IN_MIM: float = 0.278  # Const for convert kmh in mpm
    CM_IN_M: int = 100  # Const for convert cm in m

    def __init__(self,
                 action: int,
                 duration: int,
                 weight: int,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        return ((self.CALORIES_MULTIPLIER * self.weight
                 + (((self.get_mean_speed() * self.KMH_IN_MIM)**2)
                    / (self.height / self.CM_IN_M)) * self.CALORIES_SHIFT
                 * self.weight) * self.duration * self.MIN_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""

    CALORIES_MULTIPLIER: float = 1.1  # Const for get calories
    CALORIES_SHIFT: float = 2  # Const for get calories
    LEN_STEP: float = 1.38  # Const for convert steps

    def __init__(self,
                 action: int,
                 duration: int,
                 weight: int,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self):
        return ((self.get_mean_speed() + self.CALORIES_MULTIPLIER)
                * self.CALORIES_SHIFT * self.weight * self.duration)


classes: dict[str, type[Training]] = {'SWM': Swimming,
                                      'RUN': Running,
                                      'WLK': SportsWalking}


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in classes:
        raise NotImplementedError('Получены неверные данные!')
    return classes[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info().get_message()
    print(info)
    return


if __name__ == '__main__':
    packages = [('SWM', [720, 1, 80, 25, 40]),
                ('RUN', [15000, 1, 75]),
                ('WLK', [9000, 1, 75, 180])]
    try:
        for workout_type, data in packages:
            training = read_package(workout_type, data)
            main(training)
    except (ValueError, NotImplementedError):
        print('Ошибка, получены неверные данные!')
