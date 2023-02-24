from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.utils import timezone

from .models import Choice, Question

#Presente un error al intentar aplicar estas vistas dinamicas y estuvo en no cambiar las instancias en el archivo urls.py revisar eso
class IndexView(ListView):
    #Esta línea hará que la vista nos devuelva en la variable de contexto todos los registros del modelo question, sin embargo nosotros personalizamos eso por lo tanto no va esta línea.
    #model = Question
    
    template_name = 'polls/index.html' #Este será el nombre de plantilla a renderizar
    
    #Este va a ser el nombre asignado a lo que django envía por defecto a la template como contexto, y será una lista del objeto tratado en esta vista, en el caso de no hacer esto la manera de referenciar el contexto será 'objects_list'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        preguntas = Question.objects.filter(choice__isnull=False).distinct()
        return preguntas.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        preguntas = Question.objects.filter(choice__isnull=False).distinct()
        return preguntas.filter(pub_date__lte=timezone.now())

class ResultsView(DetailView):
    model = Question
    template_name = 'polls/results.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        preguntas = Question.objects.filter(choice__isnull=False).distinct()
        return preguntas.filter(pub_date__lte=timezone.now())

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You have not selected an option",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))