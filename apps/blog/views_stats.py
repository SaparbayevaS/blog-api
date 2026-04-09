from asyncio import gather, run
import httpx
from .models import Post, Comment
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response

User = get_user_model

class StatsAPIView(APIView):
    async def get_exchange_rates(self):
        url = "https://open.er-api.com/v6/latest/USD"
        async with httpx.AsyncClient() as client:
            r = await client.get(url)
            data = r.json()
            rates = data.get("rates", {})
            return {
                "KZT": rates.get("KZT"),
                "RUB": rates.get("RUB"),
                "EUR": rates.get("EUR")
            }
        
    async def get_almaty_time(self):
        url = "https://timeapi.io/api/time/current/zone?timeZone=Asia/Almaty"
        async with httpx.AsyncClient() as client:
            r = await client.get(url)
            data = r.json()
            return data.get("dataTime")
        
    async def get_async_data(self):
        return await gather(
            self.get_exchange_rates(),
            self.get_almaty_time()
        )
    
    def get(self, request):
        exchange, almaty_time = run(self.get_async_data())
        blog_stats = {
            "total_posts": Post.objects.count(),
            "total_comments": Comment.objects.count(),
            "total_users": User.objects.count(),
        }

        return Response({
            "blog": blog_stats,
            "exchange_rates": exchange,
            "current_time": almaty_time
        })
