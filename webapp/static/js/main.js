const chat = document.querySelector('.chat');
const roomSelect = document.getElementById('room-select');
const datesContainer = document.getElementById('date-sort');


//get all messages from all rooms
//sort them into different rooms (1 object for each room)
//sort the messages in each room by date
//display each room with them messages contained inside it (by order)
//be able to filter rooms that 


async function displayAllMessagesByRoom (){
  let sortedRoomList = {}
const messagesArr = await getAllMessages('messages')
console.log(messagesArr);
message.messagesArr.forEach((message)=>{
  const currentRoom = sortedRoomList[message.room]
  if (currentRoom){
    // currentRoom.
  }
  return sortedRoomList
})  

// const formattedMessages = await messageFormat(messagesArr);
// Promise.all(formattedMessages).then((values)=>{values.forEach(displayMessages)})
// messageDateFilter()
}
// async function displayAllMessagesByRoom (){
// const messagesArr = await getAllMessagesSortedByDate('messages')
// const formattedMessages = await messageFormat(messagesArr);
// Promise.all(formattedMessages).then((values)=>{values.forEach(displayMessages)})
// messageDateFilter()
// }

displayAllMessagesByRoom()
 
//takes messages from all rooms, extracts the dates from them and creates a set of unique dates 
//which are then shown on the select drop down list for selection.
async function messageDateFilter(){
  const messages = await getAllMessagesSortedByDate()
  console.log(messages);
  const dateList = messages.map(message => {
    let createdDate = message.created_at;
    let formattedDate = createdDate.slice(0,10);
    return formattedDate})
  const uniqueDates = [...new Set(dateList)];
  uniqueDates.map((date)=>{
    const dateObject = new Date(date)
    console.log(dateObject);
    const newDate = dateObject.toLocaleString().slice(0, 10);
    let dateOption = document.createElement('date-option')
    dateOption = `<option class="dateSelection" value="${newDate}">${newDate}</option>`;
    return datesContainer.insertAdjacentHTML("afterbegin",dateOption)  
  }) 
}

//changes displays messages in room from a selected date
datesContainer.onchange= function displayMessagesFromDate(){
  const selectedDate = datesContainer.value;
  // const relevantRooms = 
}

//gets all messages from all rooms and sorts them in asc order
// async function getAllMessagesSortedByDate() {
//     const response = await fetch(`http://127.0.0.1:8000/api/messages/`)
//     data = await response.json();
//     let sortedMessagesByDate = data.sort((a,b)=>{
//       return new Date(a.created_at) - new Date(b.created_at)
//     })
//     return sortedMessagesByDate;
// }
async function getAllMessages() {
    const response = await fetch(`http://127.0.0.1:8000/api/messages/`)
    data = await response.json();
    // let sortedMessagesByDate = data.sort((a,b)=>{
    //   return new Date(a.created_at) - new Date(b.created_at)
    // })
    return data;
}

// functionality for getting messages from a specific room .
async function proccessMessages (wantedRoom) {
  chat.innerHTML = '' 
  let messages = await getMessagesFromRoom(wantedRoom);
  const formattedMessages = messageFormat(messages);
  Promise.all(formattedMessages).then((values)=>{values.forEach(displayMessages)})
      }

      //gets all messages from a room
      const getMessagesFromRoom = async (wantedRoom) => {
        const response = await fetch(`http://127.0.0.1:8000/api/messages/`);
        data = await response.json();
        const selectedRoom = data.filter(message => message.room.includes(wantedRoom));  
        return selectedRoom
      }
  
      //creates one html message out of a message object
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

      //inserts the messages into a div and addes that div to the chat window.
      function displayMessages(message){
        const messageDiv = document.createElement('div');
          messageDiv.innerHTML = message;
          return chat.appendChild(messageDiv);
      }
 


