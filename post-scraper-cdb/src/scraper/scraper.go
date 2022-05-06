package scraper

import (
    "net/http"
    "net/url"
    "io/ioutil"
    "encoding/json"
    "skunz42/post-scraper/src/credentials"
    "skunz42/post-scraper/src/database"
    "log"
    "fmt"
)

// Get 50 most recent posts for all subs
// Return a list of ids and a list of json blobs
func GetSubPosts(c *credentials.Client, d *credentials.DbClient) ([]database.Post, []database.Author) {

    user_posts := make([]database.Post, 0)
    authors := make([]database.Author, 0)

    for city := range(ALL_SUBS) {
        fmt.Println("-----------------------------------------------------------------------------")
        log.Println("Fetching: " + ALL_SUBS[city])
        sub_endpoint_url := "https://oauth.reddit.com/r/" + ALL_SUBS[city] + "/new"

        last_post_id, err := database.GetLatestPost(d, ALL_SUBS[city])
        if err != nil {
            last_post_id = ""
            log.Println(err)
        }

        log.Println("LAST POST ID: " + last_post_id)

        url_params := url.Values{}
        url_params.Add("limit", "50")
        url_params.Add("before", last_post_id)

        req, _ := http.NewRequest("GET", sub_endpoint_url + "?" + url_params.Encode(), nil)
        req.Header.Set("Authorization", "bearer " + c.Access_Token)
        req.Header.Set("User-Agent", c.User_Agent)

        res, _ := c.Http_Client.Do(req)
        if res == nil {
            log.Println("DID NOT RECEIVE A RESPONSE FROM REDDIT")
            continue
        }
        log.Println("StatusCode:", res.StatusCode)
        defer res.Body.Close()

        if res.StatusCode != 200 {
            log.Println("(WARNING) Bad Status Code")
            continue
        }

        body, _ := ioutil.ReadAll(res.Body)

        var rr map[string]interface{}

        json.Unmarshal(body, &rr)

        if rr == nil {
            log.Println("(WARNING) BAD REDDIT RESPONSE")
            continue
        }

        data_map, dm_ok := rr["data"].(map[string]interface{})
        if !dm_ok {
            log.Println("(WARNING) REDDIT RESPONSE ERROR - data")
            continue
        }
        posts, child_ok := data_map["children"].([]interface{})
        if !child_ok {
            log.Println("(WARNING) REDDIT RESPONSE ERROR - children")
            continue
        }

        for i := range(posts) {
            data, err := json.Marshal(posts[i].(map[string]interface{})["data"])
            if err != nil {
                log.Println("(WARNING) Error marshalling data")
                continue
            }

            author_fullname, author_fn_ok := posts[i].(map[string]interface{})["data"].(map[string]interface{})["author_fullname"]
            if !author_fn_ok {
                log.Println("(WARNING) REDDIT RESPONSE ERROR - author fullname (deleted)")
                continue
            }

            author, author_ok := posts[i].(map[string]interface{})["data"].(map[string]interface{})["author"]
            if !author_ok {
                log.Println("(WARNING) REDDIT RESPONSE ERROR - author")
                continue
            }

            post_id, post_ok := posts[i].(map[string]interface{})["data"].(map[string]interface{})["id"]
            if !post_ok {
                log.Println("(WARNING) REDDIT RESPONSE ERROR - posts")
                continue
            }
            log.Println(post_id)

            post_id_str, ok1 := post_id.(string)
            author_str, ok2 := author.(string)
            author_fullname_str, ok3 := author_fullname.(string)

            if i == 0 {
                post_fullname := "t3_"+post_id_str
                err = database.UpdateMRP(d, post_fullname, ALL_SUBS[city])
                if err != nil {
                    log.Println("On DB Update:", err)
                }
            }

            if ok1 && ok2 && ok3 {
                post_struct := database.Post{Id: post_id_str, Blob: data}
                author_struct := database.Author{Username: author_str, Fullname: author_fullname_str}

                user_posts = append(user_posts, post_struct)
                authors = append(authors, author_struct)
            } else {
                log.Println("INVALID FORMATTING")
            }
        }
        fmt.Println("-----------------------------------------------------------------------------")
    }

    log.Println("Done scraping :^)")

    return user_posts, authors
}
