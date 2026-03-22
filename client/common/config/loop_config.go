package config

import "time"

type ClientLoopConfig struct {
	LoopAmount int
	LoopPeriod time.Duration
}
