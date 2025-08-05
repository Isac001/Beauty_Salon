from django.shortcuts import render
from django.core.paginator import Paginator
from django.views import View

# Importe os seletores do seu app de agendamento
from apps.scheduling.logic import selectors

class HomeView(View):
    def get(self, request):
        # 1. Busca a lista de agendamentos (Agendados e Cancelados) para o primeiro card
        scheduled_list = selectors.list_scheduled_and_canceled()
        
        # 2. Busca a lista de acompanhamento (Concluídos e Executando) para o segundo card
        active_list = selectors.list_completed_and_executing()

        # 3. Paginação para a primeira lista (parâmetro 'page')
        paginator_scheduled = Paginator(scheduled_list, 3) # 5 itens por página
        page_number_scheduled = request.GET.get('page')
        page_obj = paginator_scheduled.get_page(page_number_scheduled)

        # 4. Paginação para a segunda lista (parâmetro 'completed_page')
        paginator_active = Paginator(active_list, 3) # 5 itens por página
        page_number_active = request.GET.get('completed_page')
        completed_page_obj = paginator_active.get_page(page_number_active)

        context = {
            'page_obj': page_obj,
            'completed_page_obj': completed_page_obj,
        }
        
        return render(request, 'home/home.html', context)

