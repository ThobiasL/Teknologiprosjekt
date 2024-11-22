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
        self.lock = threading.Lock()


        # Setup UDP kontakt for å sende kommandoer
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Sett opp UDP-kontakt for mottak av bekreftelser og signaler
        self.recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.recv_socket.bind(('', self.listen_port))  # Bind til alle grensesnitt på listen_port
        self.recv_socket.settimeout(1)  # Ikke-blokkerende med tidsavbrudd for mottak

        # Define accepted signals
        self.accepted_signals = (
            "door_is_locked",
            "door_is_unlocked",
            "fall_detected",
            "false_alarm",
            "Pills_Dispens"
        )

        # Store the last receiveed message
        self.last_received_message = None


        # starter en tråd for å lytte etter bekreftelser og signaler
        self.listening = True
        self.listener_thread = threading.Thread(target=self.readSignalFromESP32, daemon=True)
        self.listener_thread.start()

    def readSignalFromESP32(self):
        # Lytter etter bekreftelser og signaler fra ESP32
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
                continue
            except Exception as e:
                print(f"Error receiving message: {e}")


    def getMessage(self):
        # Hent siste mottatte melding
        if self.last_received_message:
            message = self.last_received_message
            self.last_received_message = None  # Nullstill etter å ha hentet meldingen
            print(message)
            return message
        return ""

        

    def sendSignalToESP32(self, esp32_ip, message, esp32_port=12345):
        #esp32_ip (str): IP-adressen til ESP32.
        #message (bytes): Melding er i bytes-format fordi arduino behandler Strings på en annen måte enn python.
        #esp32_port (int): Porten ESP32 lytter på. Standard er 12345.
        with self.lock:
            if self.send_socket.fileno() == -1:
                print("[ERROR] Send socket is closed or invalid.")
                return
            try:
                self.send_socket.sendto(message, (esp32_ip, esp32_port))
                print(f"Message sent to ESP32 at {esp32_ip}:{esp32_port}")
            except Exception as e:
                print(f"[ERROR] Error sending message to ESP32: {e}")

    def lockDoor(self):
        self.sendSignalToESP32("192.168.1.79", b"lock door")

    def unlockDoor(self):
        self.sendSignalToESP32("192.168.1.79", b"unlock door")

    def pillDispensation(self):
        self.sendSignalToESP32("192.168.1.240", b"Dispens Pills")

    def close_sockets(self):
        # Lukk UDP-kontakter
        if self.recv_socket:
            self.recv_socket.close()
            print("Recv socket closed.")
        if self.send_socket:
            self.send_socket.close()
            print("Send socket closed.")
