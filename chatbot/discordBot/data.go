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

// CurrentSongWrapper contains Response obj
type CurrentSongWrapper struct {
	Response CurrentSong `json:"response"`
}

// Device obj containing spotify device info
type Device struct {
	Name string `json:"name"`
	//ID            string `json:"id"`
	//Restricted    bool   `json:"is_restricted"`
	//Private       bool   `json:"is_private_session"`
	IsActive      bool   `json:"is_active"`
	Type          string `json:"type"`
	VolumePercent int    `json:"volume_percent"`
}

// DeviceResp Wrapper for all the devices
type DeviceResp struct {
	StatusCode int      `json:"error_code"`
	Devices    []Device `json:"devices"`
}

// Response obj
type Response struct {
	Response DeviceResp `json:"response"`
}
