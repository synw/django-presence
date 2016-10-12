package main

import (
	"fmt"
	"time"
	"strings"
	"github.com/spf13/viper"
	"github.com/centrifugal/gocent"
	)
	
func getConf() map[string]interface{} {
	default_chans := []string{"public"}
	viper.SetConfigName("centpres_config")
	viper.AddConfigPath(".")
	viper.AddConfigPath("./etc/centpres")
	viper.AddConfigPath("$HOME/.centpres")
	viper.SetDefault("centrifugo_host", "localhost")
	viper.SetDefault("centrifugo_port", "8001")
	viper.SetDefault("channels", default_chans)
	err := viper.ReadInConfig()
	if err != nil {
	    panic(fmt.Errorf("Fatal error config file: %s \n", err))
	}
	conf := make(map[string]interface{})
	conf["host"] = viper.Get("centrifugo_host")
	conf["port"] = viper.Get("centrifugo_port")
	conf["secret_key"] = viper.Get("centrifugo_secret_key")
	conf["channels"] = viper.GetStringSlice("channels")
	conf["frequency"] = viper.GetInt("frequency")
	return conf
}

func format_msg(presence map[string]gocent.ClientInfo) string {
	var users []string
	anonymous := 0
	for _, client := range presence {
		user := client.User
		if user == "" {
			anonymous = anonymous+1
		} else {
			users = append(users, user)
		}
	}
	msg := strings.Join(users, ",")+"/"+fmt.Sprintf("%d", anonymous)
	return msg
}

func push_presence_data(conf map[string]interface{}, channel string, c chan string) {
	var output string
	// gather config info
	secret := conf["secret_key"].(string)
	host := conf["host"].(string)
	port := conf["port"].(string)
	// connect to Centrifugo
	url := fmt.Sprintf("%s:%s", host, port)
	client := gocent.NewClient(url, secret, 5*time.Second)
	presence, _ := client.Presence(channel)
	msg := format_msg(presence)
	data := fmt.Sprintf("{\"message\": \"%s\",\"event_class\":\"__presence__\"}", msg)
	d := []byte(data)
	_, err := client.Publish(channel, d)
	 if err != nil {
	 	println(err.Error())
	 	return
	 }
	 t := time.Now()
	 tstr := fmt.Sprintf("%d:%d %ds", t.Hour(), t.Minute(), t.Second())
	 output = output+tstr+" Channel "+channel+" -> "+msg
	 c <- output
	 return
}

func push_all_data(conf map[string]interface{}, t time.Time) {
	channels := conf["channels"].([]string)
	c := make(chan string)
	for _, channel := range channels {
		go push_presence_data(conf, channel, c)
		//output := <- c
		//fmt.Println(output)
		}
	return
}

func main() {
	conf := getConf()
	frequency := conf["frequency"].(int)
	duration := time.Duration(frequency)*time.Second
	for x := range time.Tick(duration) {
		push_all_data(conf, x)
	}
}