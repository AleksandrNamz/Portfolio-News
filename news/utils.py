class MyMixin(object):

    def get_lower(self, s):
        # приходит либо строка, либо обьект, тк lower() только для строк(для обьектов выдает ошибку).Выясняем строка
        # ли это, если нет, подразумеваем что обьект, тогда вызываем его метод тайтл, и приводим в верхний регистр.
        if isinstance(s, str):
            return s.lower()
        else:
            return s.title.lower()