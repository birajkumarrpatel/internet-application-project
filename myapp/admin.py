from django.contrib import admin
from .models import Topic, Course, Student, Order


class CourseAdmin(admin.ModelAdmin):
    fields = [('title', 'topic'), ('price', 'num_reviews')]
    list_display = ('title', 'topic', 'price', 'num_reviews')


class OrderAdmin(admin.ModelAdmin):

    def id(self):
        return self

    fields = [('student', 'order_status'), 'total_items', 'order_date']
    list_display = ('id', 'student', 'order_status', 'total_items', 'order_date')


# Register your models here.
admin.site.register(Topic)
admin.site.register(Course, CourseAdmin)
admin.site.register(Student)
admin.site.register(Order, OrderAdmin)
