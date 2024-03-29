from django import template
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import Group

from apps.article_review.models import Review
from apps.reviewer_assignment.models import Assignment

register = template.Library()


@register.filter
def to_and(value):
    print(value)
    print('1 minutos' in value)
    if '1 minutos' in value:
        value = value.replace('minutes', '1 minuto')
    else:
        value = value.replace("minutes", "minutos")
    lista = value.split(",")
    if len(lista) == 1:
        return value
    elif len(lista) > 1:
        return "".join(lista[:-1]) + ", " + lista[-1]


@register.filter
def minutes(value):
    # extract the minutes from the string
    minutes = value.split("\xa0")[0]

    return int(minutes)

# @register.filter
# def has_notis(value):
#     notis = Notification.objects.filter(actor_object_id=value.id, verb='message', unread=True)
#     if notis:
#         return True
#     return False


# * Filters for notis


# @register.simple_tag
# def register_notify_callbacks_notis(notis_badge_class,
#                                     message_badge_class='live_notify_badge',  # pylint: disable=too-many-arguments,missing-docstring
#                                     menu_class='live_notify_list',
#                                     refresh_period=15,
#                                     callbacks='',
#                                     api_name='list',
#                                     fetch=5):
#     refresh_period = int(refresh_period) * 1000

#     if api_name == 'list':
#         api_url = reverse('notifications:live_unread_notification_list')
#     elif api_name == 'count':
#         api_url = reverse('notifications:live_unread_notification_count')
#     else:
#         return ""
#     definitions = """
#         notify_notis_badge_class='{notis_badge_class}';
#         notify_message_badge_class='{message_badge_class}';
#         notify_menu_class='{menu_class}';
#         notify_api_url='{api_url}';
#         notify_fetch_count='{fetch_count}';
#         notify_unread_url='{unread_url}';
#         notify_mark_all_unread_url='{mark_all_unread_url}';
#         notify_refresh_period={refresh};
#     """.format(
#         notis_badge_class=notis_badge_class,
#         message_badge_class=message_badge_class,
#         menu_class=menu_class,
#         refresh=refresh_period,
#         api_url=api_url,
#         unread_url=reverse('notifications:unread'),
#         mark_all_unread_url=reverse('notifications:mark_all_as_read'),
#         fetch_count=fetch
#     )

#     script = "<script>" + definitions
#     for callback in callbacks.split(','):
#         script += "register_notifier(" + callback + ");"
#     script += "</script>"
#     return format_html(script)


# @register.simple_tag(takes_context=True)
# def live_notify_badge_notis(context, badge_class='live_notify_badge'):
#     user = user_context(context)
#     if not user:
#         return ''

#     if 'notis' in badge_class:
#         html = "<span class='{badge_class}'>{unread}</span>".format(
#             badge_class=badge_class, unread=user.notifications.unread().count()
#         )
#     else:
#         messages_unread = user.notifications.unread().filter(verb="message").count()
#         html = "<span class='{badge_class}'>{unread}</span>".format(
#             badge_class=badge_class, unread=messages_unread)

#     return format_html(html)


@register.simple_tag
def live_notify_list_notis(list_class='live_notify_list'):
    # * bootstrap dropdown menu
    html = "<ul class='{list_class}'></ul>".format(list_class=list_class)
    # html = "<ul class='{list_class}'></ul>".format(list_class=list_class)
    return format_html(html)


def user_context(context):
    if 'user' not in context:
        return None

    request = context['request']
    user = request.user
    try:
        user_is_anonymous = user.is_anonymous()
    except TypeError:  # Django >= 1.11
        user_is_anonymous = user.is_anonymous

    if user_is_anonymous:
        return None
    return user


@register.filter(name='has_group')
def has_group(user, group_name):
    try:

        group = Group.objects.get(name=group_name)
        return True if group in user.groups.all() else False
    except:
        return False


@register.filter(name='is_assigned')
def is_assigned(article):
    # * check for assignment with article
    try:
        if article.assignment.referees.all().count() > 0:
            return True
    except:
        return False


@register.filter(name="get_review_id")
def get_review_id(assignment, user):
    try:
        review = Review.objects.filter(assignment=assignment, referee = user.profile)
        return review[0].id
    except:
        return False

# * get sent revies

@register.filter(name="get_sent_reviews")
def get_sent_reviews(assignment):
    # * count enviado = True reviews
    return Review.objects.get_sent_reviews(assignment)

# * get is sent

@register.filter(name="get_is_sent")
def get_is_sent(assignment, user):
    # * get is sent
    return Review.objects.get_is_sent(assignment, user)

# * has notes

@register.filter(name="has_notes")
def has_notes(assignment, user):
    # * get is sent
    return Review.objects.has_notes(assignment, user)

# * get reported reviews

@register.filter(name="get_reported_reviews")
def get_reported_reviews(assignment):
    # * count enviado = True reviews
    return Review.objects.get_reported_reviews(assignment)

@register.filter(name="get_assignments_by_pub")
def get_assignments_by_pub(referee, publication):
    return Assignment.objects.get_assignments_by_pub(referee.profile, publication)
# * get is reported

@register.filter(name="get_is_reported")
def get_is_reported(assignment, user):
    # * get is sent
    return Review.objects.get_is_reported(assignment, user)

# * ordeanar por fecha

@register.filter(name="order_by_date")
def order_by_date(queryset):
    # * order by date
    print(queryset)
    print(queryset.order_by('modified'))
    return queryset.order_by('modified').reverse()