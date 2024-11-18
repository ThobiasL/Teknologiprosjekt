import socket
import threading

class Wireless_communication:
    def __init__(self, esp32_ip="", esp32_port=12345, listen_port=54321, timeout=5, max_retries=3):
        self.esp32_ip = esp32_ip
        self.esp32_port = esp32_port
        self.listen_port = listen_port
        self.timeout = timeout  # Seconds to wait for confirmation
        self.max_retries = max_retries
        self.buffer_size = 1024
        # self.listen_for_confirmations_and_signals = listen_for_confirmations_and_signals
        # self.sock= sock

        # Setup UDP socket for sending commands
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Setup UDP socket for receiving confirmations and signals
        self.recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.recv_socket.bind(('', self.listen_port))  # Bind to all interfaces on listen_port
        self.recv_socket.settimeout(1)  # Non-blocking with timeout for the listener thread

        # To handle received signals
        self.accepted_signals = (
            "door_is_locked",
            "door_is_unlocked",
            "fall_detected",
            "false_alarm",
            "Pills_Dispens"
        )

        # For correlating commands and confirmations
        #self.command_lock = threading.Lock()
        #self.pending_commands = {}

        # Store the last receiveed message
        self.last_received_message = None
        #self.message_event = threading.Event()

        # Start the listening thread
        self.listening = True
        self.listener_thread = threading.Thread(target=self.readSignalFromESP32, daemon=True)
        self.listener_thread.start()

    def readSignalFromESP32(self):
        print(f"Listening for confirmations and signals on port {self.listen_port}...")
        while self.listening:
            try:
                data, addr = self.recv_socket.recvfrom(self.buffer_size)
                message = data.decode('utf-8').strip()
                if message not in self.accepted_signals:
                    print(f"Unrecognized message: '{message}' from {addr}")
                    message = None
                if message in self.accepted_signals:
                    self.last_received_message = message
            except socket.timeout:
                continue  # No data received, continue listening
            except Exception as e:
                print(f"Error receiving message: {e}")


    def getMessage(self):
        if self.last_received_message:
            message = self.last_received_message
            self.last_received_message = None  # Nullstill etter å ha hentet meldingen
            print(message)
            return message
        return ""

        

    def sendSignalToESP32(self, esp32_ip, message, esp32_port=12345):
        try:
            self.send_socket.sendto(message, (esp32_ip, esp32_port))
            print(f"Message sent to ESP32 at {esp32_ip}:{esp32_port}")
        finally:
            self.send_socket.close()

    def lockDoor(self):
        self.sendSignalToESP32("192.168.1.79", b"lock door")

    def unlockDoor(self):
        self.sendSignalToESP32("192.168.1.79", b"unlock door")

    def pillDispensation(self):
        self.sendSignalToESP32("192.168.1.240", b"Dispens Pills")
