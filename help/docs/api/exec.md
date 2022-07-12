### POST /api/exec/name

Description: Execute application command.

Content-Type: *application/x-www-form-urlencoded*

URL args:

    name: string (app-status)

Args:

    session: string (abcdef123456)
    app:     string (cs)

### Status: 401 Unauthorized

Reason: not logged in or invalid session.

Content-Type: *application/json*

Content: `{}`

### Status: 400 Bad Request

Reason: invalid or missing arguments, wrong request method.

Content-Type: *application/json*

Content: `{}`

### Status: 500 Internal Server Error

Reason: error dispatching command.

Content-Type: *application/json*

Content: `{}`

### Status: 200 OK

Content-Type: *application/json*

Content:

    {
        "qid": ",123456abcdef"
    }
