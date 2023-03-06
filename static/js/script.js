// Show and hide qa form

const toggleFreshBtn = document.querySelector('#fresh-btn')
const toggleFreshBox = document.querySelector('#fresh-box')

toggleFreshBtn.addEventListener('click', function () {
  toggleFreshBox.classList.toggle('show')
})

// Submit q-a pair

const form = document.getElementById('qa-form')
const questionInput = document.getElementById('question')
const answerInput = document.getElementById('answer')
const submitButton = document.getElementById('freshup')

form.addEventListener('submit', (event) => {
  event.preventDefault() // prevent default form submission behavior

  // get the values from the form inputs
  const question = questionInput.value
  const answer = answerInput.value

  // send a POST request to your Flask route to save the values to a CSV file
  fetch('/save-csv', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: question + answer }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log('CSV saved:', data)
      // optionally, show a success message to the user
    })
    .catch((error) => {
      console.error('Error saving CSV:', error)
      // optionally, show an error message to the user
    })

  // clear the form inputs
  questionInput.value = ''
  answerInput.value = ''

  // close the form
  toggleFreshBox.classList.toggle('show')
})
