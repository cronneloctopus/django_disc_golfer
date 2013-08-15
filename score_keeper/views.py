from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages

from .models import Course, ScoreCard
from .forms import ScoreModelForm


def get_score_data(all_scores):
    data = {'nine_sum': 0, 'eighteen_sum': 0}
    nine_count = 0
    eighteen_count = 0
    nine_scores = []
    eighteen_scores = []

    if all_scores:
        # get data of last round
        data['last_round'] = all_scores[0]

        for card in all_scores:
            if card.baskets == 9 and card.score:
                nine_count += 1
                nine_scores.append((card.created, card.score))
                data['nine_sum'] += card.score
            elif card.baskets == 18 and card.score:
                eighteen_count += 1
                eighteen_scores.append((card.created, card.score))
                data['eighteen_sum'] += card.score

        data['nine_scores'] = nine_scores
        data['eighteen_scores'] = eighteen_scores

        # get avgs
        if data['nine_sum']:
            data['nine_avg'] = data['nine_sum'] / len(nine_scores)
        if data['eighteen_sum']:
            data['eighteen_avg'] = data['eighteen_sum'] / len(eighteen_scores)

        # get min, max
        if len(nine_scores) > 0:
            data['nine_max'] = map(max, zip(*nine_scores))
            data['nine_min'] = map(min, zip(*nine_scores))
        if len(eighteen_scores) > 0:
            data['eighteen_max'] = map(max, zip(*eighteen_scores))
            data['eighteen_min'] = map(min, zip(*eighteen_scores))

    return data


def Index(request, template_name='index.html'):
    courses = Course.objects.all()

    return render_to_response(template_name, {
        'title': 'Disc Golf - Home',
        'courses': courses
    }, RequestContext(request))


def CourseDetail(request, slug, template_name='course_detail.html'):
    all_scores = None
    data = None
    # check for map variable
    if request.GET.get('map'):
        request.session['map_provider'] = request.GET.get('map')
    course = Course.objects.get(slug=slug)
    # score form
    form = ScoreModelForm(request.POST or None)
    # validate and submit form data
    if form.is_valid():
        updated = ScoreCard.objects.filter(
            created=form.cleaned_data['created'],
            course=course,
            user=request.user,
            baskets=form.cleaned_data['baskets']
        ).update(**form.cleaned_data)

        if updated == 0:
            score = form.save(commit=False)
            score.course = course
            score.user = request.user
            score.save()

            messages.add_message(
                request, messages.INFO, 'Thanks for submitting a score!'
            )

        # TODO: send email to user
        # TODO: use celery to offload to queue
        """
        send_mail(
            to_address=g.user.email,
            from_address='discgolf-app@gmail.com',
            subject='New Dsic Golf Scorecard Score.',
            plaintext='You just recorded a new score for ' + course.name,
            html='You just recorded a new score for <b>' + course.name + '</b>'
        )
        """

    # get course data
    if request.user.is_authenticated():
        all_scores = ScoreCard.objects.all().filter(course=course).filter(
            user=request.user
        ).order_by('-created')

        # get all the score data we need!
        if len(all_scores) > 0:
            data = get_score_data(all_scores)

    return render_to_response(template_name, {
        'title': 'Course Detail -' + course.name,
        'course': course,
        'form': form,
        'data': data,
        'all_scores': all_scores,
    }, RequestContext(request))
