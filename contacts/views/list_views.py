from django.shortcuts import render
from contacts.models.contact import Contact


def contact_list(request):
    qs = Contact.objects.all()
    q = request.GET.get("search", "").strip()
    if q:
        qs = qs.filter(name__icontains=q) | qs.filter(email__icontains=q)
    ctx = {"contacts": qs, "search": q}

    if request.htmx:
        return render(request, "contacts/partials/contact_items.html", ctx)
    return render(request, "contacts/contacts_list.html", ctx)
