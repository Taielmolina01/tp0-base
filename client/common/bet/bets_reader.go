package bet

import (
	"encoding/csv"
	"fmt"
	"io"
	"os"
	"strconv"
	"time"
)

const (
	_CHUNK_SIZE            = 8000
	_NAME_FIELD_INDEX      = 0
	_LAST_NAME_FIELD_INDEX = 1
	_DNI_FIELD_INDEX       = 2
	_BIRTHDATE_FIELD_INDEX = 3
	_BETNUMBER_FIELD_INDEX = 4
	_DATA_FILEPATH         = ".data/agency-%d.csv"
)

type BetsReader interface {
	ReadChunk() ([]BetDto, error)
}

type betsReaderImpl struct {
	reader         *csv.Reader
	buffered       []BetDto
	agencyNumber   int
	maxBatchAmount int
}

func CreateBetsReader(
	agencyNumber, maxBatchAmount int,
) (BetsReader, error) {
	file, err := os.Open(fmt.Sprintf(_DATA_FILEPATH, agencyNumber))
	if err != nil {
		return nil, err
	}

	reader := csv.NewReader(file)

	return &betsReaderImpl{
		reader:         reader,
		agencyNumber:   agencyNumber,
		maxBatchAmount: maxBatchAmount,
	}, nil
}

func (b *betsReaderImpl) ReadChunk() ([]BetDto, error) {
	result := []BetDto{}
	if len(b.buffered) > 0 {
		result = append(result, b.buffered...)
		b.buffered = b.buffered[:0]
	}
	for read := 0; read < _CHUNK_SIZE; {
		actualRow, err := b.reader.Read()

		if err != nil {
			if err == io.EOF {
				break
			}
			return nil, err
		}

		name, lastName := actualRow[_NAME_FIELD_INDEX], actualRow[_LAST_NAME_FIELD_INDEX]
		birthdateStr := actualRow[_BIRTHDATE_FIELD_INDEX]
		dniStr, betNumberStr := actualRow[_DNI_FIELD_INDEX], actualRow[_BETNUMBER_FIELD_INDEX]

		dni, err := strconv.Atoi(dniStr)
		if err != nil {
			return nil, fmt.Errorf("invalid dni %q: %w", dniStr, err)
		}

		betNumber, err := strconv.Atoi(betNumberStr)
		if err != nil {
			return nil, fmt.Errorf("invalid bet number %q: %w", betNumberStr, err)
		}

		birthdate, err := time.Parse("2006-01-02", birthdateStr)
		if err != nil {
			return nil, fmt.Errorf("invalid birthdate %q: %w", birthdateStr, err)
		}

		actualBet := BetDto{
			b.agencyNumber,
			CreateBet(
				name,
				lastName,
				dni,
				betNumber,
				birthdate,
			),
		}

		if read+len([]byte(actualBet.String())) > _CHUNK_SIZE {
			b.buffered = append(b.buffered, actualBet)
			break
		}

		result = append(result, actualBet)

		if len(result) == b.maxBatchAmount {
			break
		}

		read += len([]byte(actualBet.String()))
	}
	return result, nil
}
