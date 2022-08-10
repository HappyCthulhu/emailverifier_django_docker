from django.contrib import admin


class OrderedAdmin(admin.ModelAdmin):
    actions = ['to_up', 'to_down', 'to_top', 'to_bottom']

    def to_up(self, request, qs):
        for obj in qs:
            obj.up()

    def to_down(self, request, qs):
        for obj in qs:
            obj.down()

    def to_top(self, request, qs):
        for obj in qs:
            obj.top()

    def to_bottom(self, request, qs):
        for obj in qs:
            obj.bottom()

    to_up.short_description = "Поднять на строчку выше"
    to_down.short_description = "Опустить на строчку ниже"
    to_top.short_description = "Поднять на самый верх"
    to_bottom.short_description = "Опустить в самый низ"
