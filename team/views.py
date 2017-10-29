from django.shortcuts import render

def index(request):
    return render(request, 'team_list.html', {})

def add(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/profiles/login')
    if request.method == 'POST':
        new_member = request.POST['new_member']

        # TO BE REMOVED, DATA to be saved in DB
        print(new_member)

        return render(request, 'team_list.html', {})

        # choose where to redirect the user after successul data addition
        # render(request, 'team_list.html', {})
def delete(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/profiles/login')
    if request.method == 'POST':
        member_id = request.POST['member_id']

        # TO BE REMOVED, DATA to be saved in DB
        print(member_id)

        return render(request, 'team_list.html', {})

        # choose where to redirect the user after successul data addition
        # render(request, 'team_list.html', {})
