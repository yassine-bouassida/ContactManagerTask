from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from contacts.forms.contact_form import ContactForm


@require_http_methods(["POST"])
def contact_create(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        new_contact = form.save()
        if request.htmx:
            return render(
                request, "contacts/partials/contact_card.html", {"c": new_contact}
            )
        return redirect("contacts:list")

    if request.htmx:
        return render(
            request,
            "contacts/partials/contact_form_errors.html",
            {"form": form},
            status=200,  # for some reason when I used status != 200 it didn't replace
        )
    return redirect("contacts:list")
