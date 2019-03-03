package discordBot

// Joke used norris jokes
type Joke struct {
	Value string `json:"value"`
}

// TJoke Trump joke
type TJoke struct {
	Value string `json:"haha_joke"`
}

// CurrentSong from spotify
type CurrentSong struct {
	Error       bool     `json:"error"`
	ErrorCode   int      `json:"error_code"`
	Name        string   `json:"name"`
	ReleaseDate string   `json:"release_date"`
	Artists     []string `json:"artists"`
	IsPlaying   bool     `json:"is_playing"`
}

// CurrentSongWrapper
type CurrentSongWrapper struct {
	Response CurrentSong `json:"response"`
}
