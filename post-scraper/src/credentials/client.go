package credentials

import (
    "net/http"
)

type Client struct {
    Client_Id string
    client_secret string
    Access_Token string
    Reddit_Username string
    reddit_password string
    Http_Client *http.Client
    User_Agent string
}

type TokenStruct struct {
    Scope string
    AccessToken string `json:"access_token"`
    ExpiresIn int `json:"expires_in"`
}

func setClientId(s string, c *Client) {
    c.Client_Id = s
}

func setClientSecret(s string, c *Client) {
    c.client_secret = s
}

func setUsername(s string, c *Client) {
    c.Reddit_Username = s
}

func setPassword(s string, c *Client) {
    c.reddit_password = s
}

func setUserAgent(s string, c *Client) {
    c.User_Agent = s
}
