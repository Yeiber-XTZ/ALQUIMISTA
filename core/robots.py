from django.http import HttpResponse
from django.views.decorators.http import require_GET

@require_GET
def robots_txt(request):
    """Generate robots.txt file."""
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /staff/",
        "",
        "Sitemap: {}/sitemap.xml".format(request.build_absolute_uri('/').rstrip('/'))
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
