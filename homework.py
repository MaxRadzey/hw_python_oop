from dataclasses import dataclass


@dataclass
class InfoMessage():
    """Информационное сообщение о тренировке."""
    message = ('Тип тренировки: {}; '
               'Длительность: {:.3f} ч.; '
               'Дистанция: {:.3f} км; '
               'Ср. скорость: {:.3f} км/ч; '
               'Потрачено ккал: {:.3f}.')
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return self.message.format(self.training_type,
                                   self.duration,
                                   self.distance,
                                   self.speed,
                                   self.calories)


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65  # Const for convert steps
    M_IN_KM = 1000  # Const for convert meters in kilometers
    H_IN_M = 60  # Const for convert hours in minutes

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,) -> None:
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

    CALORIES_MEAN_SPEED_MULTIPLIER = 18  # Const for convert calories
    CALORIES_MEAN_SPEED_SHIFT = 1.79  # Const for convert calories

    def get_distance(self):
        return super().get_distance()

    def get_mean_speed(self):
        return super().get_mean_speed()

    def get_spent_calories(self):
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / self.M_IN_KM
                * self.duration * self.H_IN_M)

    def show_training_info(self):
        return super().show_training_info().get_message()


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_MULTIPLIER = 0.035  # Const for get calories
    CALORIES_SHIFT = 0.029  # Const for get calories
    KMH_IN_MIM = 0.278  # Const for convert kmh in mpm
    SM_IN_M = 100  # Const for cobvert sm in m

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_distance(self):
        return super().get_distance()

    def get_mean_speed(self):
        return super().get_mean_speed()

    def get_spent_calories(self):
        return ((self.CALORIES_MULTIPLIER * self.weight
                + (((self.get_mean_speed() * self.KMH_IN_MIM)**2)
                   / (self.height / self.SM_IN_M)) * self.CALORIES_SHIFT
                * self.weight) * self.duration * self.H_IN_M)

    def show_training_info(self):
        return super().show_training_info().get_message()


class Swimming(Training):
    """Тренировка: плавание."""

    CALORIES_MULTIPLIER = 1.1  # Const for get calories
    CALORIES_SHIFT = 2  # Const for get calories
    LEN_STEP = 1.38  # Const for convert steps

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self):
        return super().get_distance()

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self):
        return ((self.get_mean_speed() + self.CALORIES_MULTIPLIER)
                * self.CALORIES_SHIFT * self.weight * self.duration)

    def show_training_info(self):
        return super().show_training_info().get_message()


classes_dict = {'SWM': Swimming,
                'RUN': Running,
                'WLK': SportsWalking
                }


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    for class_name in classes_dict.keys():
        if workout_type == class_name:
            return classes_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info)  # .get_message()
    return


if __name__ == '__main__':
    packages = [('SWM', [720, 1, 80, 25, 40]),
                ('RUN', [15000, 1, 75]),
                ('WLK', [9000, 1, 75, 180]),
                ]
    try:
        for workout_type, data in packages:
            training = read_package(workout_type, data)
            main(training)
    except ValueError:
        print('Error')
