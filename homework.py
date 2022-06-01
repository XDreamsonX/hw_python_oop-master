from dataclasses import dataclass
from typing import Dict, List, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    '''Базовый класс тренировки.'''
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        '''Получить дистанцию в км.'''
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        '''Получить среднюю скорость движения.'''
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(f'Класс: {self.__class__.__name__} должен'
                                  'реализовывать метод get_spent_calories')

    def show_training_info(self) -> InfoMessage:
        '''Вернуть информационное сообщение о выполненной тренировке.'''
        return (InfoMessage(self.__class__.__name__,
                            self.duration,
                            self.get_distance(),
                            self.get_mean_speed(),
                            self.get_spent_calories()))


class Running(Training):
    '''Тренировка: бег.'''
    МНОЖИТЕЛЬ_СКОРОСТИ: int = 18
    УМЕНЬШИТЕЛЬ_СКОРОСТИ: int = 20

    def get_spent_calories(self) -> float:
        return ((self.МНОЖИТЕЛЬ_СКОРОСТИ * self.get_mean_speed()
                - self.УМЕНЬШИТЕЛЬ_СКОРОСТИ)
                * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_H)


class SportsWalking(Training):
    '''Тренировка: спортивная ходьба.'''
    CALORIES_FIRST: int = 0.035
    CALORIES_SECOND: int = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        return ((self.CALORIES_FIRST * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.CALORIES_SECOND * self.weight) * (self.duration
                * self.MIN_IN_H))


class Swimming(Training):
    '''Тренировка: плавание.'''
    LEN_STEP: float = 1.38
    CALORIES_FIRST: float = 1.1
    CALORIES_SECOND: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        '''Получение средней скорости'''
        return (self.length_pool
                * self.count_pool / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.CALORIES_FIRST)
                * self.CALORIES_SECOND * self.weight)


def read_package(workout_type: str, data: List[int]) -> Training:
    '''Прочитать данные полученные от датчиков.'''
    data_type: Dict[str, Type[Training]] = {'SWM': Swimming, 'RUN': Running,
                                            'WLK': SportsWalking}
    if workout_type in data_type:
        return data_type[workout_type](*data)
    raise ValueError('Неизвестный тип тренировки {workout_type}')


def main(training: Training) -> None:
    '''Главная функция.'''
    info = training.show_training_info()
    print(InfoMessage.get_message(info))


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
