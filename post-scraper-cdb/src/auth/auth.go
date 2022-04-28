package auth

import (
    "net/http"
    "net/url"
    "encoding/json"
    "strings"
    "skunz42/post-scraper/src/credentials"
)

type TokenStruct struct {
    Scope string
    AccessToken string `json:"access_token"`
    ExpiresIn int `json:"expires_in"`
}

func GetToken(c *credentials.Client) error {
    endpoint_url := "https://www.reddit.com/api/v1/access_token"
    form := url.Values {
        "grant_type": {"password"},
        "username": {c.Reddit_Username},
        "password": {c.Reddit_Password},
    }

    req, err := http.NewRequest("POST", endpoint_url, strings.NewReader(form.Encode()))
    if err != nil {
        return err
    }

    req.SetBasicAuth(c.Client_Id, c.Client_Secret)
    req.Header.Set("User-Agent", c.User_Agent)
    res, err := c.Http_Client.Do(req)
    if err != nil {
        return err
    }

    defer res.Body.Close()

    token_struct := TokenStruct{}
    decoder := json.NewDecoder(res.Body)

    err = decoder.Decode(&token_struct)
    if err != nil {
        return err
    }

    c.Access_Token = token_struct.AccessToken

    return nil
}
