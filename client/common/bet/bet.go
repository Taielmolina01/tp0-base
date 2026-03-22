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
		"{name: %s, lastName: %s, dni: %v, birthday: %v, number: %v}",
		b.name,
		b.lastName,
		b.dni,
		b.birthday,
		b.betNumber,
	)
}
