package protocol

import (
	"encoding/binary"

	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/common/bet"
	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/common/socket"
	"github.com/op/go-logging"
)

const (
	SEND_BET_CODE      = 0x01
	ACK_CODE           = 0x03
	FIN_CODE           = 0x05
	FIN_CHUNKS_CODE    = 0x10
	QUERY_WINNERS_CODE = 0x09
)

// Types and creation function of the protocol

type ClientProtocol interface {
	CreateClientSocket(int) error
	SendBets([]bet.BetDto) error
	ReceiveAckBet() (string, error)
	NotifyEndAndWaitWinners() ([]bet.DNI, error)
	Exit() error
}

type ClientProtocolImpl struct {
	serverAddress string
	socket        socket.Socket
}

func CreateClientProtocol(
	serverAddress string,
	logger *logging.Logger) ClientProtocol {
	return &ClientProtocolImpl{
		serverAddress: serverAddress,
	}
}

// CreateClientSocket Initializes client socket. In case of
// failure, error is printed in stdout/stderr and exit 1
// is returned
func (c *ClientProtocolImpl) CreateClientSocket(id int) error {
	socket, err := socket.CreateSocket(c.serverAddress) // handle error
	if err != nil {
		return err
	}
	c.socket = socket
	err = c.makeAppHandshake(id)
	if err != nil {
		return err
	}
	return nil
}

func (c *ClientProtocolImpl) SendBets(bets []bet.BetDto) error {
	err := c.socket.SendAll([]byte{SEND_BET_CODE})

	if err != nil {
		return err
	}

	err = c.sendBigEndianTwoBytesNumber(len(bets))
	if err != nil {
		return err
	}

	for _, bet := range bets {
		err = c.sendBet(bet)
		if err != nil {
			return err
		}
	}

	return nil
}

func (c *ClientProtocolImpl) ReceiveAckBet() (string, error) {
	data, err := c.socket.ReceiveAll(1)
	if err != nil {
		return "", err
	}
	return string(data), nil
}

func (c *ClientProtocolImpl) NotifyEndAndWaitWinners() ([]bet.DNI, error) {
	c.socket.SendAll([]byte{FIN_CHUNKS_CODE})
	c.socket.SendAll([]byte{QUERY_WINNERS_CODE})
	countWinners, err := c.receiveBigEndianTwoBytesNumber()
	if err != nil {
		return nil, err
	}
	winners := make([]bet.DNI, countWinners)
	for i := 0; i < countWinners; i++ {
		winner, err := c.receiveWinner()
		if err != nil {
			return winners, err
		}
		winners[i] = winner
	}
	return winners, err
}

func (c *ClientProtocolImpl) Exit() error {
	c.socket.SendAll([]byte{FIN_CODE})
	if err := c.socket.Close(); err != nil {
		return err
	}
	return nil
}

// Helpers

func (c *ClientProtocolImpl) makeAppHandshake(id int) error {
	return c.socket.SendAll([]byte{byte(id)})
}

func (c *ClientProtocolImpl) receiveWinner() (bet.DNI, error) {
	dni, err := c.receiveBigEndianFourBytesNumber()
	if err != nil {
		return 0, err
	}
	return bet.DNI(dni), err
}

func (c *ClientProtocolImpl) sendBet(bet bet.BetDto) error {
	err := c.sendBigEndianTwoBytesNumber(len(bet.String()))
	if err != nil {
		return err
	}
	err = c.socket.SendAll([]byte(bet.String()))
	if err != nil {
		return err
	}
	return nil
}

func (c *ClientProtocolImpl) receiveBigEndianFourBytesNumber() (int, error) {
	buf, err := c.socket.ReceiveAll(4)
	if err != nil {
		return -1, err
	}
	return int(binary.BigEndian.Uint32(buf)), nil
}

func (c *ClientProtocolImpl) sendBigEndianTwoBytesNumber(number int) error {
	lenBuf := make([]byte, 2)
	binary.BigEndian.PutUint16(lenBuf, uint16(number))
	return c.socket.SendAll(lenBuf)
}

func (c *ClientProtocolImpl) receiveBigEndianTwoBytesNumber() (int, error) {
	buf, err := c.socket.ReceiveAll(2)
	if err != nil {
		return -1, err
	}
	return int(binary.BigEndian.Uint16(buf)), nil
}
