package credentials

import (
    "net/http"
    "time"
    "os"
)

const file_line_nums = 9
const reddit_lines = 5
const db_lines = 4

// FORMAT
// Line 0: Reddit Client ID
// Line 1: Reddit Client Secret
// Line 2: Reddit User Agent
// Line 3: Reddit Username
// Line 4: Reddit Password
// Line 5: Database IP
// Line 6: Database Username
// Line 7: Database Password
// Line 8: Databse Name

func MakeClient() *Client {
    c := &Client {
        Http_Client: &http.Client{ Timeout: time.Second * 10, },
    }


    setClientId(os.Getenv("REDDIT_CLIENT_ID"), c)
    setClientSecret(os.Getenv("REDDIT_CLIENT_SECRET"), c)
    setUserAgent(os.Getenv("REDDIT_USER_AGENT"), c)
    setUsername(os.Getenv("REDDIT_USERNAME"), c)
    setPassword(os.Getenv("REDDIT_PASSWORD"), c)

    return c
}

func MakeDbClient() *DbClient {
    c := &DbClient {
        Port: 5432,
    }

    setDbHost(os.Getenv("DB_HOSTNAME"), c)
    setDbUsername(os.Getenv("DB_USERNAME"), c)
    setDbPassword(os.Getenv("DB_PASSWORD"), c)
    setDbName(os.Getenv("DB_NAME"), c)

    return c
}
