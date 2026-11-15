"""The investigator's Funding opportunities page and the letter page (MW 2026-11-10).

A person sees only their own matches, letters, and suggestions. People entering for someone see that
person's page, the same as on Publications, talks, and grants.
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from apps.audit.models import AuditLog, record_event
from apps.common import prototype
from apps.outcomes import funding
from apps.outcomes import services as os
from apps.outcomes.models import FundingFollowUp, FundingSuggestion
from apps.people.models import Person


def _owner(request):
    """Whose page: the person, or someone who asked them to enter for them."""
    me = getattr(request.user, "person", None)
    if not me:
        raise PermissionDenied("The funding page belongs to CNAP members.")
    owners = os.owners_for(me) or [me]
    pk = request.GET.get("for") or request.POST.get("for")
    if pk:
        owner = get_object_or_404(Person, pk=pk)
        if os.can_act_for(request.user, owner):
            return owner, owners
    return (me if me in owners else owners[0]), owners


def _merge_repeats(groups):
    """Show a repeating event once, with its other dates listed under it (MW 2026-11-15: less to read).
    Display only. Nothing is stored or changed."""
    def merge(items):
        out, seen = [], {}
        for e in items:
            key = (e.title, e.place, e.time_text, e.host, e.summary, e.ends_on is None)
            if key in seen and e.ends_on is None:
                seen[key].also.append(e)
                continue
            e.also = []
            seen[key] = e
            out.append(e)
        return out

    loose, issues = groups
    return merge(loose), [{**g, "items": merge(g["items"])} for g in issues]


@login_required
def page(request, part="opportunities"):
    owner, owners = _owner(request)
    picked = funding.picked_for(owner)
    everyone = funding.for_everyone()
    news = funding.news()
    events = funding.upcoming_events()
    sugs = list(FundingSuggestion.objects.filter(person=owner).select_related("opportunity"))
    letters = funding.letters_for(owner)
    nxt = funding.next_deadline(picked + everyone)
    tpl = prototype.template(request, "funding", "proto/portal/funding.html")
    if part != "opportunities" and not tpl.startswith("hub/"):
        # Separate pages exist only in the Member Hub design (MW 2026-11-14). With the switch off, the one page keeps every section.
        anchor = {"resources": "s-before", "news": "s-news"}[part]
        q = f"?for={owner.pk}" if owner.pk != request.user.person.pk else ""
        return redirect(f"{reverse('portal:funding')}{q}#{anchor}")
    chrome = {}
    if tpl.startswith("hub/"):
        from . import hub

        chrome = hub.chrome(request)  # the Hub header (MW 2026-11-14)
    return render(
        request,
        tpl,
        {
            **chrome,
            "part": part,
            "owner": owner,
            "owners": owners,
            "acting_for_other": owner.pk != request.user.person.pk,
            "questions": funding.questions(),
            "picked": picked,
            "picked_next": funding.next_deadline(picked),
            "everyone": everyone,
            "everyone_next": funding.next_deadline(everyone),
            "next_deadline": nxt,
            "news": news,
            "news_groups": funding.grouped(news),
            "events": events,
            "event_groups": _merge_repeats(funding.grouped(events)),
            "n_pinned": sum(1 for n in news if n.pinned),
            "letters": letters,
            "suggestions": sugs,
            "from_not_funded": request.GET.get("from") == "not_funded",
            "ever_matched": owner.funding_matches.exists(),
        },
    )


@login_required
@require_POST
def suggest(request):
    owner, _ = _owner(request)
    name = request.POST.get("name", "").strip()[:300]
    back = f"{reverse('portal:funding')}?for={owner.pk}#s-suggest"
    if not name:
        messages.error(
            request, "Add the opportunity’s name, then select Send the suggestion again."
        )
        return redirect(back)
    url = request.POST.get("url", "").strip()[:500]
    if url and not url.startswith(("http://", "https://")):
        url = "https://" + url
    s = FundingSuggestion.objects.create(
        person=owner,
        name=name,
        sponsor=request.POST.get("sponsor", "").strip()[:300],
        url=url,
        deadline_text=request.POST.get("deadline_text", "").strip()[:200],
        why=request.POST.get("why", "").strip()[:4000],
        for_everyone=bool(request.POST.get("for_everyone")),
    )
    record_event(request.user, AuditLog.Action.CREATE, s, new={"name": name})
    messages.success(request, "Sent. The CNAP team will review the suggestion.")
    return redirect(back)


@login_required
def letter(request, pk):
    f = get_object_or_404(FundingFollowUp.objects.select_related("grant", "person"), pk=pk)
    if not funding.can_read_letter(request.user, f):
        raise PermissionDenied(
            "Each letter is visible only to the person it was written for and the CNAP office."
        )
    tpl = prototype.template(request, "funding_letter", "proto/portal/funding_letter.html")
    return render(
        request,
        tpl,
        {**funding.letter_parts(f), "preview": f.status != FundingFollowUp.Status.SENT},
    )
