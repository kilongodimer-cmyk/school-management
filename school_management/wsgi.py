"""
WSGI config for school_management project.
It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')

application = get_wsgi_application()

# Integrate WhiteNoise to serve static files and optionally media in production
try:
	from whitenoise import WhiteNoise
	from django.conf import settings

	static_root = getattr(settings, "STATIC_ROOT", None)
	static_url = getattr(settings, "STATIC_URL", "/static/")
	if static_root:
		application = WhiteNoise(application, root=static_root, prefix=static_url)

	# Serve media via WhiteNoise add_files (useful for small projects; for large media use S3)
	media_root = getattr(settings, "MEDIA_ROOT", None)
	media_url = getattr(settings, "MEDIA_URL", "/media/")
	if media_root:
		application.add_files(media_root, prefix=media_url)
except Exception:
	# If WhiteNoise is not installed or settings are not available, continue with default application
	pass
