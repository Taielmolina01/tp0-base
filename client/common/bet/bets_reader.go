package bet

import (
	"encoding/csv"
	"fmt"
	"io"
	"os"
)

const (
	_CHUNK_SIZE = 8000
)

type BetsReader interface {
	ReadChunk() ([]Bet, error)
}

type betsReaderImpl struct {
	reader *csv.Reader
}

func CreateBetsReader(
	fileName string,
	agencyNumber int,
) (BetsReader, error) {
	file, err := os.Open(fmt.Sprintf("../../../.data/agency-%d.csv", agencyNumber))
	if err != nil {
		return nil, err
	}

	reader := csv.NewReader(file)

	return &betsReaderImpl{reader: reader}, nil
}

func (b *betsReaderImpl) ReadChunk() ([]Bet, error) {
	result := []Bet{}
	read := 0
	for read := 0; read < _CHUNK_SIZE; {
		record, err := reader.Read()

		// Check for the end of the file
		if err == io.EOF {
			break // Exit the loop when no more data is available
		}

	}
	return nil, nil
}
