from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.core import serializers

from .forms import MakeMultipleChoiceQuestionForm, MakeTrueFalseQuestionForm, MakeTestForm
from .models import QuestionModel, QuestionCategory, TestModel

import json

# Create your views here.


def make_mulitple_choice_question_view(request, id=None):

    if request.method == 'POST':

        # check to see if we are editing an existing model
        if id:
            form = MakeMultipleChoiceQuestionForm(request.POST, instance=QuestionModel.objects.get(id=id))

        # new
        else:
            form = MakeMultipleChoiceQuestionForm(request.POST)

        if form.is_valid():

            cd = form.cleaned_data
            question = form.save(commit=False)
            question.answer = int(cd['answer'])
            question.save()

            return HttpResponseRedirect(reverse('maker:home'))


    else:
        form = MakeMultipleChoiceQuestionForm()

        # render form with fields if editing a model
        if id is not None:
            question = QuestionModel.objects.get(id=id)
            form.fields['question'].initial = question.question
            form.fields['answer'].initial = question.answer
            form.fields['choice_1'].initial = question.choice_1
            form.fields['choice_2'].initial = question.choice_2
            form.fields['choice_3'].initial = question.choice_3
            form.fields['choice_4'].initial = question.choice_4
            form.fields['choice_5'].initial = question.choice_5
            form.fields['choice_6'].initial = question.choice_6


    return render(request, 'make_multiple_choice_question.html', {'form': form})


def make_true_false_question_view(request, id=None):

    if request.method == 'POST':

        # check to see if we are editing an existing model
        if id:
            form = MakeTrueFalseQuestionForm(request.POST, instance=QuestionModel.objects.get(id=id))
        else:
            form = MakeTrueFalseQuestionForm(request.POST)

        if form.is_valid():

            cd = form.cleaned_data
            question = form.save(commit=False)
            question.answer = int(cd['answer'])
            question.save()

            return HttpResponseRedirect(reverse('maker:home'))

    else:
        form = MakeTrueFalseQuestionForm()

        # edit an existing model
        if id is not None:
            question = QuestionModel.objects.get(id=id)
            form.fields['question'].initial = question.question
            form.fields['answer'].initial = question.answer


    return render(request, 'make_true_false_question.html', {'form': form})


def delete_question(request, id):

    q = QuestionModel.objects.get(id=id)
    q.delete()
    return HttpResponseRedirect(reverse('maker:home'))


def delete_popup(request, id):

    q = QuestionModel.objects.get(id=id)

    return render(request, 'delete_popup.html', {'q': q})


def make_home_view(request):

    t = TestModel.objects.all()

    q = QuestionModel.objects.all()

    return render(request, 'make_home.html', context =  {'q': q, 't': t})


def multiple_choice_preview_view(request):

    return render(request, 'view_multiple_choice.html')


def make_test_view(request):

    q = QuestionModel.objects.all()


    return render(request, 'make_test.html', {'q': q})

@require_GET
def get_question(request, id):
    # serialize requires iterator even though get returns a single object always
    # serializer returns an array but we always will return a single question, so return dict instead
    q = json.loads(serializers.serialize('json', [QuestionModel.objects.get(id=id)]))[0]

    # look up category to return as string, and return all the fields of the model
    q['fields']['category'] = QuestionCategory.objects.get(id=q['fields']['category']).name
    q['fields']['id'] = q['pk']
    return JsonResponse(q['fields'])

@require_POST
def make_test(request):

    # TODO: check for no questions sent in
    # JavaScript is sending in an array of question IDs and name of test
    q_ids = json.loads(request.POST.get('questions'))
    name = request.POST.get('name')

    # get questions user selected by ID
    questions = QuestionModel.objects.filter(id__in=q_ids)

    # create test model, save, associate questions, save  <-- needs to be done in this order, how Django works i guess
    test = TestModel(name=name)
    test.save()
    test.question.set(questions)
    test.save()

    # go back to create home
    return HttpResponse()

