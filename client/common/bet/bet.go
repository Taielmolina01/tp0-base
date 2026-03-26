package bet

import (
	"fmt"
	"time"
)

type Bet struct {
	name      string
	lastName  string
	dni       int
	birthday  time.Time
	betNumber int
}

func CreateBet(
	name, lastName string,
	dni, betNumber int,
	birthday time.Time,
) Bet {
	return Bet{
		name:      name,
		lastName:  lastName,
		dni:       dni,
		birthday:  birthday,
		betNumber: betNumber,
	}
}

func (b Bet) String() string {
	return fmt.Sprintf(
		"%s,%s,%v,%v,%v",
		b.name,
		b.lastName,
		b.dni,
		b.birthday.Format("2006-01-02"),
		b.betNumber,
	)
}

func (b Bet) GetDNI() int {
	return b.dni
}

func (b Bet) GetBetNumber() int {
	return b.betNumber
}
