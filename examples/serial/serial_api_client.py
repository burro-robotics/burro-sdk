#!/usr/bin/env python

"""
A script to interact with a serial device. It sends data entered by the user and
displays the response from the device.
"""

import serial
import time
import argparse
import logging
import sys


def setup_logging():
    """ Set up the logging format. """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def parse_arguments():
    """ Parse command line arguments. """
    parser = argparse.ArgumentParser(description="Interact with a serial device.")
    parser.add_argument("--port", default="/dev/pts/5", help="Serial port to connect to.")
    parser.add_argument("--baud", type=int, default=115200, help="Baud rate for the serial connection.")
    parser.add_argument("--timeout", type=float, default=0.5, help="Read timeout for the serial connection.")
    parser.add_argument("--cmd", type=str, default=None, help="Command to send to the device.")
    return parser.parse_args()


def main():
    """ Main function to run the script. """
    setup_logging()

    args = parse_arguments()

    try:
        # Initialize the serial connection
        device = serial.Serial(args.port, args.baud, timeout=args.timeout)
    except serial.SerialException as e:
        logging.error(f"Failed to open serial port: {e}")
        sys.exit(1)

    logging.info(f"Open serial device: port={args.port}, baud={args.baud}, timeout={args.timeout}")

    while True:
        try:
            # Get user input
            if args.cmd is None:
                data_to_send = input("Enter data to send: ")
            else:
                data_to_send = args.cmd
                logging.info(f"Sending: {args.cmd}")

            # Send data
            device.write((data_to_send + '\r').encode())
            tic = time.time()

            # Read response
            incoming_data = device.read_until(b'\r').decode().strip()
            toc = time.time()

            logging.info(f"Received: {incoming_data} ({1000*(toc-tic):.3f}ms)")

            time.sleep(0.5)
        except KeyboardInterrupt:
            logging.info("Exiting...")
            break
        except Exception as e:
            logging.error(f"Error: {e}")


if __name__ == "__main__":
    main()
