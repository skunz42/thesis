package scraper

import (
    "encoding/json"
)

type Listing struct {
	Kind string
	Data struct {
		Id        string
        Name      string
		Author    string
		Title     string
		Created   json.Number
	}
}

type Response struct {
	Type string
	Data struct {
		Children []Listing
	}
}
