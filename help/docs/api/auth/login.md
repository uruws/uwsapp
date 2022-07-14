### POST /api/auth/login

**Description**: User login.

Content-Type: *application/x-www-form-urlencoded*

Args:

    username: string (user@example.com)
    password: string (not123456)

### Status: 400 Bad Request

**Reason**: Invalid or missing arguments, wrong request method.

Content-Type: *application/json*

`{}`

### Status: 200 OK

Content-Type: *application/json*

    {
      "uid": "abcdef-123456",
      "name": "richard",
      "username": "richard@uwsapp.docs",
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
      "session": "abcdef123456"
    }
