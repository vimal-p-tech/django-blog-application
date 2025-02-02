import os 

from channels.auth import AuthMiddlewareStack 
from channels.routing import ProtocolTypeRouter, URLRouter 
from django.core.asgi import get_asgi_application 
import blog.routing


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_app.settings") 

application = ProtocolTypeRouter({ 
"http": get_asgi_application(), 
"websocket": AuthMiddlewareStack( 
		URLRouter( 
			blog.routing.websocket_urlpatterns 
		) 
	), 
}) 
