package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"github.com/centrifugal/gocent"
	"github.com/spf13/viper"
	"github.com/synw/centcom"
	"github.com/synw/terr"
	"strconv"
	"time"
)

type Server struct {
	Addr    string
	Key     string
	Watch   string
	Publish string
	Freq    int
}

func main() {
	server, tr := getServer()
	if tr != nil {
		tr := terr.Add("initializing server", tr)
		tr.Fatal()
	}
	cli := centcom.New(server.Addr, server.Key)
	err := cli.CheckHttp()
	if err != nil {
		tr := terr.New("initializing websockets", err)
		tr.Fatal()
		return
	}
	msg := "Connection to " + server.Addr + " is ready"
	fmt.Println(msg)
	// connection is ok now, start working
	fmt.Println("Watching channel", server.Watch)
	msg = "Pushing presence info every " + strconv.Itoa(server.Freq) + " seconds to channel " + server.Publish
	fmt.Println(msg)
	// run
	push(cli, server)
	duration := time.Duration(server.Freq) * time.Second
	for _ = range time.Tick(duration) {
		push(cli, server)
	}
}

func push(cli *centcom.Cli, server *Server) {
	data, tr := getPresenceData(cli, server.Watch)
	if tr != nil {
		tr := terr.Pass("getting presence data", tr)
		tr.Formatc()
	}
	anonymous, users := getUsers(data)
	tr = publish(cli, server, users, anonymous)
	if tr != nil {
		tr.Print()
	}
	msg := formatMsg(users, anonymous)
	fmt.Println(msg)
}

func publish(cli *centcom.Cli, server *Server, users []string, anonymous int) *terr.Trace {
	data := make(map[string]interface{})
	data["event_class"] = "__presence__"
	payload := make(map[string]interface{})
	payload["anonymous"] = anonymous
	payload["users"] = users
	data["data"] = payload
	dataBytes, err := json.Marshal(data)
	if err != nil {
		tr := terr.New("publish:json.Marshal", err)
		return tr
	}
	_, err = cli.Http.Publish(server.Publish, dataBytes)
	if err != nil {
		tr := terr.New("publish:cli.Http.Publish", err)
		return tr
	}
	return nil
}

func getPresenceData(cli *centcom.Cli, channel string) (map[string]gocent.ClientInfo, *terr.Trace) {
	data, err := cli.Http.Presence(channel)
	if err != nil {
		tr := terr.New("getPresenceData", err)
		return data, tr
	}
	return data, nil
}

func getUsers(presence map[string]gocent.ClientInfo) (int, []string) {
	var users []string
	anonymous := 0
	for _, client := range presence {
		user := client.User
		if user == "anonymous" {
			anonymous = anonymous + 1
		} else {
			users = append(users, user)
		}
	}
	return anonymous, users
}

func getDistinctUsers(users []string) []string {
	u := []string{}
	for _, user := range users {
		isnew := true
		for _, uu := range u {
			if uu == user {
				isnew = false
				break
			}
		}
		if isnew == true {
			u = append(u, user)
		}
	}
	return u
}

func formatMsg(u []string, a int) string {
	users := getDistinctUsers(u)
	nu := strconv.Itoa(len(users))
	msg := "Users: " + nu + "  Anonymous : " + fmt.Sprintf("%d", a)
	return msg
}

func getServer() (*Server, *terr.Trace) {
	dwatch := "public"
	dpublish := "$presence"
	viper.SetConfigName("centpres_config")
	viper.AddConfigPath(".")
	viper.AddConfigPath("./etc/centpres")
	viper.AddConfigPath("$HOME/.centpres")
	viper.SetDefault("addr", "localhost:8001")
	viper.SetDefault("frequency", 10)
	viper.SetDefault("watch", dwatch)
	viper.SetDefault("publish", dpublish)
	err := viper.ReadInConfig()
	if err != nil {
		var server *Server
		switch err.(type) {
		case viper.ConfigParseError:
			tr := terr.New("getServer", err)
			return server, tr
		default:
			err := errors.New("Unable to locate config file")
			tr := terr.New("getServer", err)
			return server, tr
		}
	}
	addr := viper.Get("addr").(string)
	key := viper.Get("key").(string)
	watch := viper.Get("watch").(string)
	publish := viper.Get("publish").(string)
	freq := viper.GetInt("frequency")
	server := &Server{addr, key, watch, publish, freq}
	return server, nil
}
