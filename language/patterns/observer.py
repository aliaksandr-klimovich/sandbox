# https://en.wikipedia.org/wiki/Observer_pattern


class Observable:
    def __init__(self):
        self.__observers = []

    def register_observer(self, observer):
        self.__observers.append(observer)

    def notify_observers(self, *args, **kwargs):
        for observer in self.__observers:
            observer.notify(self, *args, **kwargs)


class Observer:
    def __init__(self, observable):
        observable.register_observer(self)

    def notify(self, observable, *args, **kwargs):
        print('Got', args, kwargs, 'from', observable, 'to', self)


subject = Observable()
observers = (Observer(subject), Observer(subject), Observer(subject))
subject.notify_observers('test')
