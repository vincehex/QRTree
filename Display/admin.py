from django.contrib import admin

from .models import TreeType, User, TreeInformation, Record

admin.site.site_header = "QR后台管理系统"
admin.site.site_title = 'QR后台'


@admin.register(TreeType)
class TreeTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'growthHabit']
    list_display_links = ['id', 'name']
    ordering = ['-id']
    actions_on_bottom = True

    def func(self, request, queryset):
        pass

    func.short_description = '批量导出'
    actions = [func]
    search_fields = ['name']
    list_filter = ['name']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'sex', 'phone']
    list_display_links = ['id', 'username']
    search_fields = ['username']
    fieldsets = [['基础', {'fields': ['username', 'password', 'sex', 'phone']}],
                 ['高级', {'fields': ['is_staff', 'is_superuser']}],
                 ['扩展', {'fields': ['email', 'birthdate', 'IDCard', 'first_name', 'last_name', ]}],
                 ]


@admin.register(TreeInformation)
class TreeInformationAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'age', 'height', 'width', 'date', 'user']
    list_display_links = ['id']
    search_fields = ['age', 'height', 'width']
    list_filter = ['type']
    # date_hierarchy = ['date']
    fieldsets = [["基础", {'fields': ['type', 'age', 'height', 'width', 'img']}],
                 ["选填", {'fields': ['date', 'user']}]]

    def preview(self, obj):
        return '<img src="/statics/upload/%s" />' % obj.img

    preview.allow_tags = True
    preview.short_description = "图片"
    readonly_fields = ['preview']


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'dateTime', 'method', 'user']
    list_display_links = ['id']
    fields = ['dateTime', 'method', 'user']
