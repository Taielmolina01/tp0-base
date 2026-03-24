package bet

import "fmt"

type BetDto struct {
	agencyNumber int
	bet          Bet
}

func (b *BetDto) String() string {
	return fmt.Sprintf("%d,%s", b.agencyNumber, b.bet.String())
}
