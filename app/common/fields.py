from django.db.models import ForeignKey, OneToOneField


class UidGetAttName(object):
    def get_attname(self):
        return f'{self.name}_uid'


class UidForeignKey(UidGetAttName, ForeignKey):
    pass


class UidOneToOneField(UidGetAttName, OneToOneField):
    pass