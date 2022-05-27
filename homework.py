from dataclasses import dataclass


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


@dataclass
class Training:
    '''Базовый класс тренировки.'''
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_H = 60
    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        '''Получить дистанцию в км.'''
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        '''Получить среднюю скорость движения.'''
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Внимание, ОШИБКА!')

    def show_training_info(self) -> InfoMessage:
        '''Вернуть информационное сообщение о выполненной тренировке.'''
        return (InfoMessage(self.__class__.__name__,
                            self.duration,
                            self.get_distance(),
                            self.get_mean_speed(),
                            self.get_spent_calories()))


@dataclass
class Running(Training):
    '''Тренировка: бег.'''
    COEFICIENT_CALL1 = 18
    COEFICIENT_CALL2 = 20
    MIN_IN_H = 60
    action: int
    duration: float
    weight: float

    def get_spent_calories(self) -> float:
        return ((self.COEFICIENT_CALL1 * self.get_mean_speed()
                - self.COEFICIENT_CALL2)
                * self.weight / self.M_IN_KM * self.duration * self.MIN_IN_H)


@dataclass
class SportsWalking(Training):
    '''Тренировка: спортивная ходьба.'''
    COEFICIENT_CALL1 = 0.035
    COEFICIENT_CALL2 = 0.029
    MIN_IN_H = 60
    action: int
    duration: float
    weight: float
    height: float

    def get_spent_calories(self):
        return ((self.COEFICIENT_CALL1 * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * self.COEFICIENT_CALL2 * self.weight) * (self.duration
                * self.MIN_IN_H))


@dataclass
class Swimming(Training):
    '''Тренировка: плавание.'''
    LEN_STEP = 1.38
    COEFICIENT_CALL1 = 1.1
    COEFICIENT_CALL2 = 2
    action: int
    duration: float
    weight: float
    length_pool: int
    count_pool: int

    def get_mean_speed(self) -> float:
        '''Получение средней скорости'''
        return (self.length_pool
                * self.count_pool / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.COEFICIENT_CALL1)
                * self.COEFICIENT_CALL2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    data_type = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    try:
        return data_type[workout_type](*data)
    except (KeyError, ValueError) as error:
        print(f'Ошибка {repr(error)}')
        raise error


def main(training: Training) -> None:
    '''Главная функция.'''
    info = Training.show_training_info(training)
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
