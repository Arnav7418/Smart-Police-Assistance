
const notifications = [
    "Notification 1",
    "Notification 2",
    "Notification 3"
];

const notificationsList = document.querySelector('.notifications');

notifications.forEach(notification => {
    const li = document.createElement('li');
    li.textContent = notification;
    notificationsList.appendChild(li);
});
