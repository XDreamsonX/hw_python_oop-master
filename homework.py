class InfoMessage:
    '''Информационное сообщение о тренировке.'''
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
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
    '''Базовый класс тренировки.'''
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

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
        '''Получить количество затраченных калорий.'''
        pass

    def show_training_info(self) -> InfoMessage:
        '''Вернуть информационное сообщение о выполненной тренировке.'''
        return (InfoMessage(self.__class__.__name__,
                            self.duration,
                            self.get_distance(),
                            self.get_mean_speed(),
                            self.get_spent_calories()))


class Running(Training):
    '''Тренировка: бег.'''
    coeff_calorie_1 = 18
    coeff_calorie_2 = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float):
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_spent_calories(self) -> float:
        return ((self.coeff_calorie_1 * Training.get_mean_speed(self)
                - self.coeff_calorie_2)
                * self.weight / self.M_IN_KM * self.duration * 60)


class SportsWalking(Training):
    '''Тренировка: спортивная ходьба.'''
    coeff_calorie_1: float = 0.035
    coeff_calorie_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float):
        self.action = action
        self.duration = duration
        self.weight = weight
        self.height = height

    def get_spent_calories(self):
        return ((self.coeff_calorie_1 * self.weight
                + (Training.get_mean_speed(self)**2 // self.height)
                * self.coeff_calorie_2 * self.weight) * (self.duration * 60))


class Swimming(Training):
    '''Тренировка: плавание.'''
    LEN_STEP = 1.38
    coeff_call_1 = 1.1
    coeff_call_2 = 2

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: int, count_pool: int):
        self.action = action
        self.duration = duration
        self.weight = weight
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        '''Получение средней скорости'''
        return (self.length_pool
                * self.count_pool / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((Swimming.get_mean_speed(self) + self.coeff_call_1)
                * self.coeff_call_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    '''Прочитать данные полученные от датчиков.'''
    type_training = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    return type_training[workout_type](*data)


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