from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from contacts.models.contact import Contact


@require_http_methods(["DELETE"])
def contact_delete(request, pk):
    c = get_object_or_404(Contact, pk=pk)
    c.delete()
    return render(request, "contacts/contact_deleted.html")
