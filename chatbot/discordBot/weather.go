package discordBot

import (
	"encoding/xml"
	"fmt"
	"io/ioutil"
	"net/http"
	"strconv"
	"strings"
	"time"
)

type weather struct {
	Location loc       `xml:"location"`
	Details  []details `xml:"forecast>tabular>time"`
}

type loc struct {
	Name    string `xml:"name"`
	Country string `xml:"country"`
}

type details struct {
	From string `xml:"from,attr"`
	To   string `xml:"to,attr"`
	Temp temp   `xml:"temperature"`
}

type temp struct {
	Temp int `xml:"value,attr"`
}

// GetTemp henter nåværende temperatur fra yr.no
func GetTemp() (string, error) {
	resp, err := http.Get("https://www.yr.no/sted/Norge/Oslo/oslo/oslo/varsel.xml")
	if err != nil {
		fmt.Println("Got an error..", err)
	}

	defer resp.Body.Close()
	var w weather
	bytes, _ := ioutil.ReadAll(resp.Body)
	xml.Unmarshal(bytes, &w)

	now := time.Now()
	thisHour, _, _ := now.Clock()

	for _, times := range w.Details {
		n := strings.Split(times.From, "T")
		h := strings.Split(n[1], ":")
		hour, _ := strconv.Atoi(h[0])
		if thisHour <= hour {
			info := "Fra kl " + strconv.Itoa(hour) + ":00 vil temperaturen være " + strconv.Itoa(times.Temp.Temp) + " grader for " + w.Location.Name + "!"
			return info, nil
		}
	}
	return "", fmt.Errorf("Ingen tid matchet med nåværende tid..")
}
