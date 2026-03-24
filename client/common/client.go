package common

import (
	"time"

	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/common/bet"
	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/common/config"
	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/common/protocol"
	"github.com/op/go-logging"
)

// Client Entity that encapsulates how
type Client struct {
	loopConfig config.ClientLoopConfig
	id         int
	protocol   protocol.ClientProtocol
	logger     *logging.Logger
}

// NewClient Initializes a new client receiving the configuration
// as a parameter
func NewClient(
	clientServerConfig config.ClientServerConfig,
	clientLoopConfig config.ClientLoopConfig,
) *Client {
	logger := logging.MustGetLogger("log")
	client := &Client{
		loopConfig: clientLoopConfig,
		id:         clientServerConfig.ID,
		protocol:   protocol.CreateClientProtocol(clientServerConfig.ServerAddress, logger),
		logger:     logger,
	}
	return client
}

// StartClientLoop Send messages to the client until some time threshold is met
func (c *Client) StartClientLoop() {
	// There is an autoincremental msgID to identify every message sent
	// Messages if the message amount threshold has not been surpassed

	err := c.protocol.CreateClientSocket(c.id)
	if err != nil {
		c.logger.Criticalf(
			"action: create_socket | result: fail | client_id: %v | error: %v",
			c.id,
			err,
		)
		return
	}

	reader, err := bet.CreateBetsReader(c.id)

	if err != nil {
		c.logger.Criticalf(
			"action: open_csv | result: fail | client_id: %v | error: %v",
			c.id,
			err,
		)
		return
	}

	for msgID := 1; msgID <= c.loopConfig.LoopAmount; msgID++ {

		bets, err := reader.ReadChunk()

		if err != nil {
			c.logger.Criticalf(
				"action: read_csv | result: fail | client_id: %v | error: %v",
				c.id,
				err,
			)
			break
		}

		if len(bets) == 0 {
			break
		}

		err = c.protocol.SendBets(bets)

		if err != nil {
			c.logger.Criticalf(
				"action: send_bet | result: fail | client_id: %v | error: %v",
				c.id,
				err,
			)
		}

		_, err = c.protocol.ReceiveAckBet()

		if err != nil {
			c.logger.Criticalf(
				"action: receive_bet_ack | result: fail | client_id: %v | error: %v",
				c.id,
				err,
			)
		}

		// c.logger.Infof("action: receive_message | result: success | client_id: %v | msg: %v",
		// 	c.id,
		// 	msg,
		// )

		// Wait a time between sending one message and the next one
		time.Sleep(c.loopConfig.LoopPeriod)

	}

	winners, err := c.protocol.NotifyEndAndWaitWinners()

	if err != nil {
		c.logger.Criticalf(
			"action: consulta_ganadores | result: fail | client_id: %v | error: %v",
			c.id,
			err,
		)
	}

	c.logger.Infof(
		"action: consulta_ganadores | result: success | cant_ganadores: %v",
		len(winners),
	)

	err = c.protocol.Exit()

	if err != nil {
		c.logger.Criticalf(
			"action: exit_protocol | result: fail | client_id: %v | error: %v",
			c.id,
			err,
		)
	}

	c.logger.Infof("action: loop_finished | result: success | client_id: %v", c.id)
}

func (c *Client) CloseGracefully() {
	err := c.protocol.Exit()
	if err != nil {
		c.logger.Criticalf(
			"action: close_socket | result: fail | client_id: %v | error: %v",
			c.id,
			err,
		)
	}
	c.logger.Info(
		"action: close_socket | result: fail | client_id: %v",
		c.id,
	)
}
