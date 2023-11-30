from reversion.admin import VersionAdmin


class BaseAdmin(VersionAdmin):
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'user', None) is None:
            obj.user = request.user
        obj.save()
