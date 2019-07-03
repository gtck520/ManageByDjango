import xadmin

from .models import UserComments, UserInteractives, UserFavorite, UserSnap


class UserCommentsAdmin(object):
    list_display = ['user', 'comment_id', 'comments', 'comment_type', 'has_read', 'snap_nums', 'add_time']
    search_fields = ['comments']
    list_filter = ['user', 'comment_type', 'add_time', 'has_read']
    model_icon = 'fa fa-comment'


class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user']
    list_filter = ['user', 'fav_type', 'add_time']
    model_icon = 'fa fa-heart'


class UserSnapAdmin(object):
    list_display = ['user', 'snap_id', 'snap_type', 'add_time']
    search_fields = ['user']
    list_filter = ['user', 'snap_type', 'add_time']
    model_icon = 'fa fa-thumbs-up'


class UserInteractivesAdmin(object):
    list_display = ['user', 'interactive', 'has_read', 'add_time']
    search_fields = ['user', 'interactive']
    list_filter = ['user', 'interactive', 'has_read', 'add_time']


xadmin.site.register(UserComments, UserCommentsAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserSnap, UserSnapAdmin)
xadmin.site.register(UserInteractives, UserInteractivesAdmin)