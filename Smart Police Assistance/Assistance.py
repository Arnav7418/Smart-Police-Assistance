import cv2
import mediapipe as mp
import time
import requests
import datetime
import threading
import mysql.connector

# Connect to MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    port="3300",  # Specify the port here
    user="root",
    password="1234",
    database="name"
)

# Function to send a Telegram message with fixed location and screen image
def send_telegram_message(screen_image, timestamp, location, location_map_link):
    print("Sending Message")
    current_time = datetime.datetime.now()
    message = f"Assistance needed. Assistance asked at {current_time} at location {location_map_link}"

    # Save the screen image temporarily
    image_path = "screen_image.jpg"
    cv2.imwrite(image_path, screen_image)

    try:
        # Send the Telegram message with the image as the main photo and the message in the caption
        url = "https://api.telegram.org/bot6946164042:AAEBr0QZZj2uhpJ8kAAtnqo78e2eEEVC5Rs/sendPhoto"
        data = {"chat_id": "1996378953", "caption": message}
        files = {"photo": open(image_path, "rb")}
        response = requests.post(url, data=data, files=files)
        print("Message sent successfully")

        # Save distress signal information to database
        save_to_database(timestamp, location, "Pending")

    except Exception as e:
        print("Error sending message:", e)

# Function to save distress signal information to database
def save_to_database(timestamp, location, status):
    try:
        cursor = db_connection.cursor()

        # Insert distress signal information into the database
        query = "INSERT INTO distress_signals (timestamp, location, status) VALUES (%s, %s, %s)"
        cursor.execute(query, (timestamp, location, status))
        db_connection.commit()

        print("Distress signal information saved to database")

    except Exception as e:
        print("Error saving to database:", e)

    finally:
        cursor.close()



# Function to detect distress signal
def distress_signal_detected(frame):
    # Placeholder: Simulate distress signal detection based on some condition
    return False

# Initialize MediaPipe Hands module
mp_hands = mp.solutions.hands

# Initialize the webcam (change the index to match your USB webcam)
cap = cv2.VideoCapture("http://192.168.203.151:8080/video")  # Use 0 for the default webcam, 1 for the second webcam, and so on

# Create a Hands Detection object
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Initialize variables for gesture timing
thumbs_down_start_time = None
thumbs_down_duration = 0

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # Detect thumbs-down gesture
    results_hands = hands.process(frame)

    if results_hands.multi_hand_landmarks:
        for landmarks in results_hands.multi_hand_landmarks:
            thumb_tip = landmarks.landmark[4]
            index_tip = landmarks.landmark[8]
            distance = ((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2) ** 0.5
            thumb_down_threshold = 0.15

            if distance > thumb_down_threshold:
                if thumbs_down_start_time is None:
                    thumbs_down_start_time = time.time()
                else:
                    thumbs_down_duration = time.time() - thumbs_down_start_time
                    if thumbs_down_duration >= 2:
                        # Start a thread to send a Telegram message with fixed location and screen image
                        timestamp = datetime.datetime.now()
                        location = "Dayananda Sagar Academy Of Technology and Management"  # Placeholder for location
                        location_map_link = 'https://maps.app.goo.gl/VkYcM33XBkL2JU6Q6'  # Fixed location link
                        threading.Thread(target=send_telegram_message, args=(frame.copy(), timestamp, location, location_map_link)).start()
                        thumbs_down_start_time = None
                        thumbs_down_duration = 0

                cv2.putText(frame, "Thumbs-Down", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                thumbs_down_start_time = None
                thumbs_down_duration = 0

            mp.solutions.drawing_utils.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Assistance Request", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close the database connection when finished
db_connection.close()
