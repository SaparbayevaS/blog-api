# Verification HW4

# 1. Admin acces via nginx
curl -I http://localhost/admin/login/

Expected: 
- 200 OK
- Server: nginx

# 2. Static files served by nginx with cachig
curl -I http://localhost/static/admin/css/base.css

Expected: 
- 200 OK
- Cache-Control: max-age=2592000

# 3. API works
curl http://localhost.api.posts/

Expecetd:
- JSON list of posts

# 4. 502 Bad Gateway checks
docker compose stop web

curl -I http://localhost/api/posts/

Expedted:
- 502 Bad Gateway (returned by nginx)

docker compose start web

# 5. Port 8000 is not accessible
curl http://localhost:8000/

Expected:
- connnection refused

# 6. WebSocket works

Connect
npx wscat -c "ws://localhost/ws/posts/<slug>/comments/?token=<jwt>"

Expected:
- Connected
- 101 Switching Protocols

When posting a comment via the REST API, a message is received through WebSocket.