package socket

import "net"

type Socket interface {
	SendAll([]byte) error
	ReceiveAll(uint) ([]byte, error)
	Close() error
}

type SocketImpl struct {
	conn net.Conn
}

func CreateSocket(address string) (Socket, error) {
	conn, err := net.Dial("tcp", address)

	if err != nil {
		return nil, err
	}

	return &SocketImpl{
		conn: conn,
	}, nil
}

func (s *SocketImpl) SendAll(data []byte) error {
	for sent := 0; sent < len(data); {
		n, err := s.conn.Write(data[sent:])
		if err != nil {
			return err
		}
		sent += n
	}
	return nil
}

func (s *SocketImpl) ReceiveAll(length uint) ([]byte, error) {
	data := []byte{}
	var received uint
	for received < length {
		n, err := s.conn.Read(data)
		if err != nil {
			return data, err
		}
		received += uint(n)
	}
	return data, nil
}

func (s *SocketImpl) Close() error {
	return s.conn.Close()
}
