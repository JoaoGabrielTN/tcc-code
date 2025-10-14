import socket
import cv2
import numpy as np
import struct
import threading

def video_server(port=5000):
    """Simple video server"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('192.168.0.2', port))
    server_socket.listen(1)
    print(f"Server started on port {port}")
    
    conn, addr = server_socket.accept()
    print(f"Connected to {addr}")
    
    data = b""
    payload_size = struct.calcsize(">L")
    cv2.namedWindow('Video Stream', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Video Stream', 800, 600)

    try:
        while True:
            # Get message length
            while len(data) < payload_size:
                data += conn.recv(4096)
            
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]
            
            # Get frame data
            while len(data) < msg_size:
                data += conn.recv(4096)
            
            frame_data = data[:msg_size]
            data = data[msg_size:]
            
            # Decode and display frame
            frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)
            #if frame is not None:
            #    cv2.resizeWindow('Video Stream', 800, 600)
            #    cv2.imshow('Video Stream', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    finally:
        cv2.destroyAllWindows()
        conn.close()
        server_socket.close()

def video_client(server_host='192.168.0.2', server_port=5000, video_path=0):
    """Simple video client (0 for webcam, or video file path)"""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))
    
    cap = cv2.VideoCapture(video_path)
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Encode frame
            ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            if ret:
                frame_data = buffer.tobytes()
                # Send frame size and data
                message = struct.pack(">L", len(frame_data)) + frame_data
                client_socket.sendall(message)
            
            # For webcam, show local preview
            if video_path == 0:
                cv2.imshow('Local Webcam', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    finally:
        cap.release()
        cv2.destroyAllWindows()
        client_socket.close()

# Usage example
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "server":
        video_server()
    else:
        # Use webcam (0) or provide video file path
        video_client(video_path="./car_crash.mp4")  # Change to video file path for pre-recorded video
