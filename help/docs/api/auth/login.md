### POST /api/auth/login

Description: User login.

Content-Type: *application/x-www-form-urlencoded*

Args:

    username: string (user@example.com)
    password: string (not123456)

### Status: 400 Bad Request

Reason: invalid or missing arguments, wrong request method.

Content-Type: *application/json*

Content: `{}`

### Status: 200 OK

Content-Type: *application/json*

Content:

    {
      "uid": "7044e95f-e20e-54be-9ce1-efa08e2b5a11",
      "name": "uwsdev",
      "username": "uwsdev@uwsapp.local",
      "is_operator": false,
      "is_admin": true,
      "apps": {
        "build": {
          "app1": "App1 description",
          "app2": "App2 description",
          "app3": "App3 description"
        },
        "deploy": {
          "app1-east": "App1 east cluster",
          "app1-west": "App1 west cluster",
          "app2": "App2 prod",
          "app3": "App3 prod",
          "app3-test": "App3 test"
        }
      },
      "session": "9em9sz2ekm8h1hq01g8ga3prh7qehn0a"
    }
