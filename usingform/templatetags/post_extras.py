# templates 태그 새로 만들어서 적용하기
from django import template
from usingform.models import Profile, CommentLike
register = template.Library()

@register.filter
def _checking(obj, user):
    getProfile = Profile.objects.get(user__username=user) #안됬는데 보니깐 슈퍼유저는 Profile이 안만들어져서 찾지를 못하는 것이였음
    try:
        CommentLike.objects.get(post=obj, author=getProfile)
        return "좋아요 취소"
    except:
        return "좋아요"