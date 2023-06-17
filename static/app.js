

const $cc_list = $('#cc-list');
const $cc_form = $('#new-cc-form')
const $flavor = $('#form-flavor')
const $size = $('#form-size')
const $rating = $('#form-rating')
const $image = $('#form-image')
const BASE_URL = 'http://localhost:5000/api/cupcakes';

async function fillList(){
    $cc_list.empty();
    const response = await axios.get(BASE_URL);
    for (let ccData of response.data.cupcakes){
        let ccHTML = $(ccDataToHTML(ccData));
        $cc_list.append(ccHTML);
    }
}

function ccDataToHTML(cc){
    return `
        <div data-cc-id=${cc.id}>
            <li>
                ${cc.flavor} - ${cc.size} - ${cc.rating}
                <button class="del-button">Delete</button>
                <img src="${cc.image}" alt="No image" style="width:200px;height:200px">
            </li>
        </div>
    `;
}

$cc_form.on("submit", async function(evt){
    evt.preventDefault();
    let flavor = $flavor.val();
    let size = $size.val();
    let rating = $rating.val();
    let image = $image.val();

    const resp = await axios.post(BASE_URL,{
        flavor,
        size,
        rating,
        image
    });
    let newCC = $(ccDataToHTML(resp.data.cupcake));
    $cc_list.append(newCC);
    $cc_form.trigger('reset');
});

$cc_list.on('click', '.del-button', async function(evt){
    evt.preventDefault();
    let $cc = $(evt.target).closest('div');
    let ccID = $cc.attr('data-cc-id');
    await axios.delete(`${BASE_URL}/${ccID}`);
    $cc.remove();
});

$(fillList);