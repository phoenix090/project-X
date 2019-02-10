package discordBot

import (
	"fmt"
	"log"
	"math/rand"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/bwmarrin/discordgo"
)

// Variables used for command line parameters
var (
	token = os.Getenv("TOKEN")
	dg    *discordgo.Session
)

// RunBot starts the bot
func RunBot() {
	// Create a new Discord session using the provided bot token.
	dg, err := discordgo.New("Bot " + token)
	if err != nil {
		fmt.Println("error creating Discord session,", err)
		return
	}

	// Register the messageCreate func as a callback for MessageCreate events.
	dg.AddHandler(messageCreate)

	// Open a websocket connection to Discord and begin listening.
	err = dg.Open()
	if err != nil {
		fmt.Println("error opening connection,", err)
		return
	}

	// Wait here until CTRL-C or other term signal is received.
	fmt.Println("Bot is now running.  Press CTRL-C to exit.")
	sc := make(chan os.Signal, 1)
	signal.Notify(sc, syscall.SIGINT, syscall.SIGTERM, os.Interrupt, os.Kill)
	<-sc

	// Cleanly close down the Discord session.
	dg.Close()
}

// This function will be called (due to AddHandler above) every time a new
// message is created on any channel that the autenticated bot has access to.
func messageCreate(s *discordgo.Session, m *discordgo.MessageCreate) {

	// Ignore all messages created by the bot itself
	// This isn't required in this specific example but it's a good practice.
	if m.Author.ID == s.State.User.ID {
		return
	}

	switch m.Content {
	case "greeting", "hi", "hello", "hey", "hei", "hola", "yo", "wassup", "sup":
		greeting(s, m)
	case "!author", "whoami", "myname":
		author(s, m)
	case "!calculate":
		calculate(s, m)
	case "!ping", "!pong":
		pingPong(s, m)

	//case "!apps":
	//	apps(s, m)
	default:
		fmt.Println(m.Content)
		s.ChannelMessageSend(m.ChannelID, "Say what?")
	}

}

func greeting(s *discordgo.Session, m *discordgo.MessageCreate) {
	answers := []string{"Salutations!", "Greetings!", "Hey there!", "Hello!", "Welcome back!", "Hola!", "Hi! :)", ":wave:"}
	sec := time.Now().Second()

	// Making greetings random
	rand.Seed(int64(sec))
	s.ChannelMessageSend(m.ChannelID, answers[rand.Intn(len(answers))])
}

func author(s *discordgo.Session, m *discordgo.MessageCreate) {
	s.ChannelMessageSend(m.ChannelID, m.Author.Mention())
}

func pingPong(s *discordgo.Session, m *discordgo.MessageCreate) {
	if m.Content == "!ping" {
		s.ChannelMessageSend(m.ChannelID, "Pong!")
	} else {
		s.ChannelMessageSend(m.ChannelID, "Ping!")
	}

}

func calculate(s *discordgo.Session, m *discordgo.MessageCreate) {

}

// fungerer ikke helt
func apps(s *discordgo.Session, m *discordgo.MessageCreate) {
	var myApps []*discordgo.Application
	var err error
	myApps, err = s.Applications()
	if err != nil {
		log.Fatalf("error getting apps, ", err)
	}
	for _, v := range myApps {
		fmt.Println(v)
		//s.ChannelMessageSend(m.ChannelID, string(v))
	}

}
