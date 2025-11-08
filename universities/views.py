from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Q, Avg
from .models import UniversityProgram


class UniversityListView(ListView):
    model = UniversityProgram
    template_name = 'universities/list.html'
    context_object_name = 'programs'
    paginate_by = 20

    def get_queryset(self):
        queryset = UniversityProgram.objects.annotate(
            avg_rating=Avg('reviews__rating')
        )

        # Search
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(university_name__icontains=search) | Q(program_name__icontains=search)
            )

        # Discipline filter
        discipline = self.request.GET.get('discipline', '')
        if discipline:
            queryset = queryset.filter(discipline=discipline)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'University Programs - engg.pk'
        context['meta_description'] = 'Honest reviews and comprehensive information about engineering programs across Pakistan.'
        context['disciplines'] = UniversityProgram.objects.values_list('discipline', flat=True).distinct()
        context['selected_discipline'] = self.request.GET.get('discipline', '')
        context['search_query'] = self.request.GET.get('search', '')
        return context


class UniversityProgramDetailView(DetailView):
    model = UniversityProgram
    template_name = 'universities/detail.html'
    context_object_name = 'program'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'{self.object.program_name} - {self.object.university_name} - engg.pk'
        context['meta_description'] = self.object.overview[:155]
        context['reviews'] = self.object.reviews.select_related('author', 'author__profile')
        return context
