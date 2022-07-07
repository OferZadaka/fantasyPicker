package data

var CodeOfTeam = map[int]string{
	1:  "Arsenal",
	2:  "Aston Villa",
	3:  "Brentford",
	4:  "Brighton and Hove Albion",
	5:  "Burnley",
	6:  "Chelsea",
	7:  "Crystal Palace",
	8:  "Everton",
	9:  "Leicestser United",
	10: "Leeds United",
	11: "Liverpool",
	12: "Manchester City",
	13: "Manchester United",
	14: "Newcastle United",
	15: "Norwich City",
	16: "Southampton",
	17: "Totthenham Hotspur",
	18: "Watford",
	19: "West Ham United",
	20: "Wolverhampton Wanderers",
}

var Points struct {
	Goal              int
	Assist            int
	CleanSheet        int
	YellowCard        int
	RedCard           int
	UnderSixtyMinutes int
	UpSixtyMinutes    int
	ThreeSaves        int
	PenaltySave       int
	PenaltyMiss       int
	OwnGoal           int
	Bonus             Bonus
}

type Bonus struct {
	PenaltySave       int
	PenaltyMiss       int
	Goal              int
	Assist            int
	ThreeSaves        int
	OwnGoal           int
	UnderSixtyMinutes int
	UpSixtyMinutes    int
	RedCard           int
	YellowCard        int
	CleanSheet        int
	Save              int
	CreatingBigChance int
	BigChanceMissed   int
}
