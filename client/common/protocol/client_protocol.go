package protocol

import (
	"encoding/binary"

	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/common/bet"
	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/common/socket"
	"github.com/op/go-logging"
)

const (
	SEND_BET_CODE = 0x01
	ACK_CODE      = 0x03
	FIN_CODE      = 0x05
)

// Types and creation function of the protocol

type ClientProtocol interface {
	CreateClientSocket() error
	SendBets([]bet.BetDto) error
	ReceiveAckBet() (string, error)
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
func (c *ClientProtocolImpl) CreateClientSocket() error {
	socket, err := socket.CreateSocket(c.serverAddress) // handle error
	if err != nil {
		return err
	}
	c.socket = socket
	return nil
}

func (c *ClientProtocolImpl) SendBets(bets []bet.BetDto) error {
	err := c.socket.SendAll([]byte{SEND_BET_CODE})

	if err != nil {
		return err
	}

	err = c.sendBigEndianNumber(len(bets))
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

func (c *ClientProtocolImpl) sendBet(bet bet.BetDto) error {
	err := c.sendBigEndianNumber(len(bet.String()))
	if err != nil {
		return err
	}
	err = c.socket.SendAll([]byte(bet.String()))
	if err != nil {
		return err
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

func (c *ClientProtocolImpl) sendBigEndianNumber(number int) error {
	lenBuf := make([]byte, 2)
	binary.BigEndian.PutUint16(lenBuf, uint16(number))
	return c.socket.SendAll(lenBuf)
}

func (c *ClientProtocolImpl) Exit() error {
	c.socket.SendAll([]byte{FIN_CODE})
	if err := c.socket.Close(); err != nil {
		return err
	}
	return nil
}
