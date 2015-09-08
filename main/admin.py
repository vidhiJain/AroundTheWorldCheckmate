from django.contrib import admin
from main.models import Question, Player, Attempt, Distance

class QuestionAdmin(admin.ModelAdmin):
	list_display = ('loc_name','rent','stipend','text','answer')

class PlayerAdmin(admin.ModelAdmin):
	list_display = ('user', 'score', 'arrival_time', 'curr_loc', 'ip_address')

class AttemptAdmin(admin.ModelAdmin):
	list_display = ('user', 'question', 'attempts', 'correct')

class DistanceAdmin(admin.ModelAdmin):
	list_display = ('source','dest','distance')

admin.site.register(Question, QuestionAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Attempt, AttemptAdmin)
admin.site.register(Distance, DistanceAdmin)

