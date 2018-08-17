from django.contrib import admin
from django.contrib.auth.models import User
from .models import Post, PostLike, PostComment
  
class PostAdmin(admin.ModelAdmin):
	model = Post
	list_display = ('user','content','created','visible')
	search_fields = ['id','content','user__username','user__first_name','user__last_name','user__email']
	list_filter = ('visible',)

admin.site.register(Post, PostAdmin)

class PostLikeAdmin(admin.ModelAdmin):
	model = PostLike
	list_display = ('user','post','created')
	search_fields = ['post__content','post__id','user__username','user__first_name','user__last_name','user__email']

admin.site.register(PostLike, PostLikeAdmin)

class PostCommentAdmin(admin.ModelAdmin):
	model = PostComment
	list_display = ('user','post','comment','created','visible')
	search_fields = ['comment','post__content','post__id','user__username','user__first_name','user__last_name','user__email']
	list_filter = ('visible',)

admin.site.register(PostComment, PostCommentAdmin)
