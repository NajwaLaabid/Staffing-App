from django.shortcuts import render

def index(request):
    return render(request, 'team_list.html', {})

def create(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/profiles/login')
    #if request.method == 'POST':
        # project_title = request.POST['project_title']
        # estimate_hours = request.POST['estimate_hours']
        # team_names = request.POST.getlist('team_names')

        # TO BE REMOVED, DATA to be saved in DB
        # print(project_title)
        # print(estimate_hours)
        # print(team_names)

        # choose where to redirect the user after successul data addition
        #return HttpResponseRedirect('/dashboard')
    return render(request, 'team_list.html', {})
