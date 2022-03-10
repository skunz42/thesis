package scraper

import (
    "net/http"
    "net/url"
    "io/ioutil"
    "encoding/json"
    "skunz42/post-scraper/src/credentials"
    "fmt"
)

// Get 50 most recent posts for all subs
// Return a list of ids and a list of json blobs
func GetSubPosts(c *credentials.Client) ([]string, [][]byte) {

    ids := make([]string, 0)
    blobs := make([][]byte, 0)

    return ids, blobs

    for city := range(ALL_SUBS) {
        fmt.Println("Fetching: " + ALL_SUBS[city])
        sub_endpoint_url := "https://oauth.reddit.com/r/" + ALL_SUBS[city] + "/new"

        url_params := url.Values{}
        url_params.Add("limit", "50")

        req, _ := http.NewRequest("GET", sub_endpoint_url + "?" + url_params.Encode(), nil)
        req.Header.Set("Authorization", "bearer " + c.Access_Token)
        req.Header.Set("User-Agent", c.User_Agent)

        res, _ := c.Http_Client.Do(req)
        defer res.Body.Close()

        body, _ := ioutil.ReadAll(res.Body)

        var rr map[string]interface{}

        json.Unmarshal(body, &rr)

        posts := rr["data"].(map[string]interface{})["children"].([]interface{})
        for i := range(posts) {
            data, err := json.Marshal(posts[i].(map[string]interface{})["data"])
            if err != nil {
                continue
            }
            name := posts[i].(map[string]interface{})["data"].(map[string]interface{})["name"]
            ids = append(ids, name.(string))
            blobs = append(blobs, data)
        }

    }
    return ids, blobs
}
