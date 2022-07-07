package main

import (
	"fmt"

	"fantasyData/dataHandler"

	"github.com/berkguzel/fpl-go/fpl"
)

func main() {

	//GetFixture(1)
	c := fpl.NewClient(nil)

	players, err := c.GetInfoOfPlayers()
	if err != nil {
		fmt.Println(err)
	}

	playerCode, err := dataHandler.GetCodeOfPlayer("Mohamed Salah", players)
	if err != nil {
		fmt.Println(err)
	}

	history, err := c.ListPlayerHistoryPast(playerCode)
	if err != nil {
		fmt.Println(err)
	}

	for _, v := range history {
		fmt.Printf("Season: %s ", v.SeasonName)
		fmt.Printf("Points: %d ", v.TotalPoints)
		fmt.Printf("Goals: %d", v.GoalsScored)
		fmt.Printf(" Assists: %d", v.Assists)
		fmt.Printf(" Clean sheets: %d", v.CleanSheets)
		fmt.Printf(" Yellow cards: %d", v.YellowCards)
		fmt.Printf(" Red cards: %d", v.RedCards)
		fmt.Printf(" Minutes played: %d", v.Minutes)
		fmt.Printf(" Bonus: %d", v.Bonus)

		fmt.Printf("\n")

	}
}
