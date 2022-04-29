package credentials

import (
    "net/http"
    "time"
    "os"
    "strconv"
)

func MakeClient() *Client {
    c := &Client {
        Http_Client: &http.Client{ Timeout: time.Second * 10, },
    }


    setClientId(os.Getenv("REDDIT_CLIENT_ID"), c)
    setClientSecret(os.Getenv("REDDIT_CLIENT_SECRET"), c)
    setUserAgent(os.Getenv("REDDIT_USER_AGENT"), c)
    setUsername(os.Getenv("REDDIT_USER_NAME"), c)
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
    port, _ := strconv.Atoi(os.Getenv("DB_PORT"))
    setDbPort(port, c)

    return c
}
