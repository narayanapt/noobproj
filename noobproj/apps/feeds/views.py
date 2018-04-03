from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from .forms import CreateFeedForm
from django.views.generic import CreateView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
#from bootcamp.decorators import ajax_required
from django.template.context_processors import csrf
from django.template.loader import render_to_string
from django.contrib import messages

from .models import Feed

max_feeds = 10

# Create your views here.
def return_html(last_feed, user, csrf_token, feed_source='all'):
	feeds = Feed.get_feeds_after(last_feed)
	html = ''
	if feed_source!='all':
		feeds = feeds.filter(user__id=feed_source)
	for feed in feeds:
		html = '{0}{1}'.format(html,
							   render_to_string('feeds/partial_feed.html',
												{
													'feed': feed,
													'user': user,
													'csrf_token': csrf_token
													}))
	return html



@login_required
def FeedDislay(request):
	all_feeds = Feed.get_feeds()
	user =  request.user
	last_page = user.profile.lastpage
	#print(last_page)
	page = request.GET.get('page')
	refresh = request.GET.get('refresh')
	if page:
		if refresh:
			pageval = 1
		else:
			pageval = page
		user.profile.lastpage = pageval

		user.profile.save()
	else:
		page = last_page
	feeds_paginator = Paginator(all_feeds, max_feeds)
	initial_feeds = feeds_paginator.page(page)
	start_feed = -1
	if initial_feeds:
		start_feed = initial_feeds[0].id

	return render(request, 'feeds/feeds.html', {
		'feeds' : initial_feeds,
		'start_feed' : start_feed,
		'page' : 1,
		})


#@ajax_required
@login_required
def CreateNewFeed(request):
	last_feed = request.POST.get('last_feed')
	csrf_token = (csrf(request)['csrf_token'])
	feed = Feed()
	user = request.user
	feed.user = user
	post = request.POST['post']
	post = post.strip()

	if len(post) > 0:
		feed.post = post[:255]
		feed.save()
	if(feed.parent == None):
		messages.success(request, "New post is")

 
	return HttpResponse(return_html(last_feed, user, csrf_token))

@login_required
def RemoveFeed(request):
	try:
		feed = request.POST.get('feed')
		feed_db = Feed.objects.get(pk=feed)
		if request.user == feed_db.user:
			parent = feed_db.parent
			feed_db.delete()
			if parent:
				parent.comments_count()
			return HttpResponse()
		else:
			return HttpResponseForbidden
	except Exception:
		return HttpResponseBadRequest()


@login_required
def show_comments(request):
	if request.method == 'POST':
		feed_id = request.POST['feed']
		feed = Feed.objects.get(pk=feed_id)
		post = request.POST['post']
		post = post.strip()
		if len(post) > 0:
			post = post[:255]
			user = request.user
			feed.post_comment(user=user, post=post)
		return render(request, 'feeds/partial_feed_comment.html',
					  {'feed': feed})

	else:
		feed_id = request.GET.get('feed')
		feed = Feed.objects.get(pk=feed_id)
		return render(request, 'feeds/partial_feed_comment.html',
					  {'feed': feed})
