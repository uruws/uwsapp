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
        "session": "9em9sz2ekm8h1hq01g8ga3prh7qehn0a"
    }
