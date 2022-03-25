package scraper

import (
    "net/http"
    "net/url"
    "io/ioutil"
    "encoding/json"
    "skunz42/post-scraper/src/credentials"
    "skunz42/post-scraper/src/database"
    "fmt"
)

// Get 50 most recent posts for all subs
// Return a list of ids and a list of json blobs
func GetSubPosts(c *credentials.Client) ([]database.Post, []database.Author) {

    posts := make([]database.Post, 0)
    authors := make([]database.Author, 0)

    //TODO remove
    return posts, authors

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

            author_fullname := posts[i].(map[string]interface{})["data"].(map[string]interface{})["author_fullname"]
            author := posts[i].(map[string]interface{})["data"].(map[string]interface{})["author"]
            post_id := posts[i].(map[string]interface{})["data"].(map[string]interface{})["id"]

            post_struct := database.Post{Id: post_id.(string), Blob: data}
            author_struct := database.Author{Username: author.(string), Fullname: author_fullname.(string)}

            posts = append(posts, post_struct)
            authors = append(authors, author_struct)
        }

    }
    return posts, authors
}
