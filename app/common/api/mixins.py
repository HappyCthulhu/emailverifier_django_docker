from django.core.cache import cache
from rest_framework.fields import DateTimeField


class CachedModelSerializerMixin(object):
    """
    Кэширование сериализованного объекта
    """

    _modify_field = 'modified'
    _pk_field = 'pk'
    _cache = cache

    def invalidate_cache(self, instance):
        """
        Принудительная инвалидация кэша
        """
        if instance and getattr(instance, self._pk_field):
            cache_id = self.get_cache_id(instance)
            cache.delete(cache_id)

    def is_invalide_cache(self, instance, cached_data):
        """
        Проверка на валидность экземпляра в кэше
        """

        return bool(cached_data
                    and getattr(instance, self._modify_field)
                    and DateTimeField().to_representation(getattr(instance, self._modify_field)) != cached_data['modified']
                    or not cached_data)

    @property
    def cache(self):
        return cache

    def get_cache_id(self, instance):
        """
        Получение идентификатора экземпляра в кэше
        """
        return f'{self.Meta.model.__module__}.{self.Meta.model.__name__}-{getattr(instance, self._pk_field)}'

    def to_representation(self, instance):
        """
        Берётся либо из кэша, либо из базы и кэшируется
        """
        if instance and getattr(instance, self._pk_field) and getattr(instance, self._modify_field):
            cache_id = self.get_cache_id(instance)
            cached_data = self.cache.get(cache_id)
            if self.is_invalide_cache(instance, cached_data):
                cached_data = super().to_representation(instance)
                self.cache.set(cache_id, cached_data)
            return cached_data
        else:
            return super().to_representation(instance)