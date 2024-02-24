from django.views.generic import View, ListView, DetailView
from base.models import Order
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils import timezone


class ShippOrderIndexView(LoginRequiredMixin, ListView):

    template_name = 'pages/shipp.html'

    def get_queryset(self):
        return Order.objects.order_by('-canceled_at', '-shipped_at', 'created_at')

# class OrderDetailView(LoginRequiredMixin, DetailView):

#     template_name = 'pages/order.html'

#     def get_queryset(self):
#         return Order.objects.filter(user=self.request.user)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         obj = self.get_object()
#         # json to dict
#         context["items"] = json.loads(obj.items)
#         context["shipping"] = json.loads(obj.shipping)
#         return context


class OperationOrderCancelView(LoginRequiredMixin, View):
    
    def post(self, request):
        order_pk = request.POST.get('order_pk')
        model = Order.objects.get(id=order_pk)
        model.canceled_at = timezone.now()
        model.save()
        return redirect('/shipp/')

class ShippCompleteView(LoginRequiredMixin, View):
    
    def post(self, request):
        order_pk = request.POST.get('order_pk')
        model = Order.objects.get(id=order_pk)
        model.shipped_at = timezone.now()
        model.save()
        return redirect('/shipp/')