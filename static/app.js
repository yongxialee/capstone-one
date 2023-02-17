$('.delete-coffee').click(deleteCoffee)

async function deleteCoffee() {
  const id = $(this).data('id')
  await axios.delete(`/api/coffee/${id}`)
  $(this).parent().remove()
}
