package credentials

import (
    "net/http"
)

type Client struct {
    Client_Id string
    Client_Secret string
    Access_Token string
    Reddit_Username string
    Reddit_Password string
    Http_Client *http.Client
    User_Agent string
}

func setClientId(s string, c *Client) {
    c.Client_Id = s
}

func setClientSecret(s string, c *Client) {
    c.Client_Secret = s
}

func setUsername(s string, c *Client) {
    c.Reddit_Username = s
}

func setPassword(s string, c *Client) {
    c.Reddit_Password = s
}

func setUserAgent(s string, c *Client) {
    c.User_Agent = s
}
