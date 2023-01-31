API_BASE_URL="https://api.sampleapis.com/coffee";
const BASE_URL = "http://127.0.0.1:5000";


/****** given data about coffee list, and generate html */
//  function generateCoffeeHTML(all_data){
//     return `
//     <div data-cupcake-id=${all_data.id}>
//       <li>
//         ${all_data.title} / ${all_data.ingredients} / ${all_data.descript}
//         <button class="delete-button">X</button>
//       </li>
//       <img class="Coffee-img"
//             src="${all_data.image}"
//             alt="(no image provided)">
//     </div>
//   `;
// }
$('.detail').click(function(){
    const detailCup = await axios.get(`${BASE_URL}/hot/<int:id>`)
    const id = $(this).data('id')
    alert(id)
})