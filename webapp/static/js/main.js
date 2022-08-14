const chat = document.querySelector('.chat');
const roomSelect = document.getElementById('room-select');

async function displayAllMessages (){
const messagesArr = await getAllMessagesSortedByDate('messages')
const formattedMessages = await messageFormat(messagesArr);
Promise.all(formattedMessages).then((values)=>{values.forEach(displayMessages)})
}

displayAllMessages()
 
console.log(allDates);
async function displayMessagesFromDate(date){


}



async function getAllMessagesSortedByDate() {
    const response = await fetch(`http://127.0.0.1:8000/api/messages/`)
    data = await response.json();
    let sortedMessagesByDate = data.sort((a,b)=>{
      return new Date(b.created_at) - new Date(a.created_at)
    })
    return sortedMessagesByDate;
}

// functionality for getting messages from a specific room .
async function proccessMessages (wantedRoom) {
  chat.innerHTML = '' 
  let messages = await getMessagesFromRoom(wantedRoom);
  const formattedMessages = messageFormat(messages);
  Promise.all(formattedMessages).then((values)=>{values.forEach(displayMessages)})
      }

      const getMessagesFromRoom = async (wantedRoom) => {
        const response = await fetch(`http://127.0.0.1:8000/api/messages/`);
        data = await response.json();
        const selectedRoom = data.filter(message => message.room.includes(wantedRoom));  
        return selectedRoom
      }
  
      async function messageFormat(messages)  {
        formattedMessagesArr = messages.map(async (message)=>{
          const userName = await getUserName(message.profile)
          const roomName = await getRoomName(message.room)
          const formatYmd = date => date.toLocalString().slice(0, 10);
          const formatHms = new Date(message.created_at)+"";
          const outputMessage = 
          `Room: ${roomName}<br>
          <p>Sent by: ${userName} , at: ${String(formatHms).slice(0,21)}</p>
          <p>${message.content}</p>

          <hr>`
          console.log();
          return outputMessage
          
        })
        return formattedMessagesArr;
      }

      async function getUserName(profileLink){
        const response = await fetch(`${profileLink}`)
        const data = await response.json()
        const userName = data.discord_name;
        return userName;
      }

      async function getRoomName(roomLink){
        const response = await fetch(`${roomLink}`)
        const data = await response.json()
        const roomName = data.__str__;
        return roomName;
      }

      function displayMessages(message){
        const messageDiv = document.createElement('div');
          messageDiv.innerHTML = message;
          return chat.appendChild(messageDiv);
      }
 


