"""DNSBL related views."""

from django.contrib.auth import mixins as auth_mixins
from django.utils.translation import gettext as _
from django.views import generic

from .. import models


class MXDomainDetailView(auth_mixins.PermissionRequiredMixin, generic.DetailView):
    """View to display MX records."""

    model = models.Domain
    permission_required = "admin.view_domain"
    template_name = "admin/mx_domain_detail.html"

    def get_queryset(self):
        """Add some prefetching."""
        return super().get_queryset().prefetch_related("mxrecord_set")

    def get_context_data(self, **kwargs):
        """Add extra variables."""
        context = super().get_context_data(**kwargs)
        context.update({"title": _("MX records of {}").format(self.object.name)})
        return context


class DNSBLDomainDetailView(auth_mixins.PermissionRequiredMixin, generic.DetailView):
    """View to display DNSBL summary."""

    model = models.Domain
    permission_required = "admin.view_domain"
    template_name = "admin/dnsbl_domain_detail.html"

    def get_queryset(self):
        """Add some prefetching."""
        return super().get_queryset().prefetch_related("dnsblresult_set")

    def get_context_data(self, **kwargs):
        """Add extra variables."""
        context = super().get_context_data(**kwargs)
        context.update({"title": _("DNSBL summary for {}").format(self.object.name)})
        return context
