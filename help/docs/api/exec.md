### POST /api/exec/name

**Description**: Execute application command.

Content-Type: *application/x-www-form-urlencoded*

URL args:

    name: string (app-status)

Args:

    session: string (abcdef123456)
    app:     string (app1)

### Status: 401 Unauthorized

**Reason**: Not logged in or invalid session.

Content-Type: *application/json*

`{}`

### Status: 400 Bad Request

**Reason**: Invalid or missing arguments; wrong request method.

Content-Type: *application/json*

`{}`

### Status: 500 Internal Server Error

**Reason**: Error dispatching command.

Content-Type: *application/json*

`{}`

### Status: 200 OK

Content-Type: *application/json*

    {
        "qid": ",123456abcdef"
    }
