package dataHandler

import (
	"errors"
	"fmt"
	"strings"

	"github.com/berkguzel/fpl-go/fpl"
)

var (
	home        string
	away        string
	kickoffTime string
)

//GetTeam gets the team name according to its code
func getTeam(home int, away int) (string, string) {
	return data.codeOfTeam[home], data.codeOfTeam[away]
}

func GetFixture(gameWeek int) string {

	c := fpl.NewClient(nil)

	fixture, err := c.GetFixture()
	if err != nil {
		fmt.Println(err)
	}

	var message string
	for i := 0; i < len(fixture); i++ {
		for _, v := range fixture[i] {
			if v.Event == float64(gameWeek) {
				home, away = getTeam(v.TeamH, v.TeamA)
				kickoffTime = fmt.Sprintf("%v", v.KickoffTime)
				message = message + "\n" + home + " " + "-" + " " + away + "  " +
					"time:" + " " + kickoffTime
				fmt.Println(message)

			}
		}
	}
	return message
}

func GetCodeOfPlayer(name string, playerData []fpl.PlayerDeailtedInfo) (int, error) {

	firstName := strings.Split(name, " ")[0]
	secondName := strings.Split(name, " ")[1]

	for _, v := range playerData {
		if strings.Contains(v.FirstName, firstName) && strings.Contains(v.SecondName, secondName) {
			return v.ID, nil
		}
	}

	return 0, errors.New("Could not find footballer")

}
