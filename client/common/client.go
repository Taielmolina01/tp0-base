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
	id         string
	protocol   protocol.ClientProtocol
	betInfo    bet.Bet
	logger     *logging.Logger
}

// NewClient Initializes a new client receiving the configuration
// as a parameter
func NewClient(
	clientServerConfig config.ClientServerConfig,
	clientLoopConfig config.ClientLoopConfig,
	betInfo bet.Bet,
) *Client {
	logger := logging.MustGetLogger("log")
	client := &Client{
		loopConfig: clientLoopConfig,
		id:         clientServerConfig.ID,
		protocol:   protocol.CreateClientProtocol(clientServerConfig.ServerAddress, logger),
		betInfo:    betInfo,
		logger:     logger,
	}
	return client
}

// StartClientLoop Send messages to the client until some time threshold is met
func (c *Client) StartClientLoop() {
	// There is an autoincremental msgID to identify every message sent
	// Messages if the message amount threshold has not been surpassed

	for msgID := 1; msgID <= c.loopConfig.LoopAmount; msgID++ {
		// Create the connection the server in every loop iteration. Send an
		err := c.protocol.CreateClientSocket()
		if err != nil {
			c.logger.Criticalf(
				"action: create_socket | result: fail | client_id: %v | error: %v",
				c.id,
				err,
			)
		}

		err = c.protocol.SendBet(c.betInfo)

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

		c.logger.Infof(
			"action: apuesta_enviada | result: success | dni: %v | numero: %v",
			c.betInfo.GetDNI(),
			c.betInfo.GetBetNumber(),
		)

		// c.logger.Infof("action: receive_message | result: success | client_id: %v | msg: %v",
		// 	c.id,
		// 	msg,
		// )

		err = c.protocol.Exit()

		if err != nil {
			c.logger.Criticalf(
				"action: exit_protocol | result: fail | client_id: %v | error: %v",
				c.id,
				err,
			)
		}

		// Wait a time between sending one message and the next one
		time.Sleep(c.loopConfig.LoopPeriod)

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
