// $(document).ready(function () {
//     show_review();
// });
//
// // 리뷰 페이지 로딩시 리뷰 목록 보여주기
// function show_review() {
//     $('#card-box').empty()
//     $.ajax({
//         type: "GET",
//         url: "/review",
//         data: {},
//         success: function (response) {
//             let rows = response['reviews']
//             for (let i = 0 ; i < rows.length; i++) {
//                 let store = rows[i]['store']
//                 let distance = rows[i]['distance']
//                 let waiting = rows[i]['waiting']
//                 let taste = rows[i]['taste']
//                 let taste_image = '❤️'.repeat(taste)
//                 let star = rows[i]['star']
//                 let comment = rows[i]['comment']
//                 let star_image = '⭐️'.repeat(star)
//                 let num = rows[i]['num']
//
//                 let temp_html = ''
//
//                 temp_html = `<div class="card">
//                                     <div class="card-body">
//                                         <blockquote class="blockquote mb-0">
//                                             <p>가게명 : ${store}</p>
//                                             <p>거리 : ${distance}</p>
//                                             <p>웨이팅 : ${waiting}</p>
//                                             <p>음식 맛 : ${taste_image}</p>
//                                             <p>총점 : ${star_image}</p>
//                                             <p>리뷰 : ${comment}</p>
//                                             <button onclick="delete_review(${num})" type="button" class="btn btn-danger" style="float: right; margin-left: 10px",>삭제</button>
//
//                                   <button onclick="to_index()" type="button" class="btn btn-warning" style="float: right">홈</button>
//                                         </blockquote>
//                                     </div>
//                                 </div>`
//
//
//                 $('#card-box').append(temp_html)
//             }
//         }
//     })
// }
//리뷰 입력 받아서 데이터 저장하기
function save_review() {
    let store = $('#store').val()
    let star = $('#star').val()
    let comment = $('#comment').val()
    let distance = $('#distance').val()
    let waiting = $('#waiting').val()
    let taste = $('#taste').val()

    if (store == '') {
        alert('가게를 입력하세요,');
        return;
    }
    if (comment == '') {
        alert('코멘트를 입력하세요.');
        return;
    }

    let form_date = new FormData();

    form_date.append('store', store);
    form_date.append('star', star);
    form_date.append('comment', comment);
    form_date.append('distance', distance);
    form_date.append('waiting', waiting);
    form_date.append('taste', taste);


    $.ajax({
        type: "POST",
        url: "/review",
        data: form_date,
        contentType: false,
        processData: false,
        success: function (response) {
            alert(response["msg"])
            window.location.href = '/review'
        }
    });
}

// 리뷰 삭제 버튼 클릭시 데이터 삭제
function delete_review(num) {

    $.ajax({
        type: "POST",
        url: "/review/delete",
        data: {'num': num},
        success: function (response) {
            alert(response['msg'])
            window.location.href = '/review'
        }
    });
}


function open_box() {
    $('#post-box').show()
}

//닫기 누르면 리뷰박스 숨기기
function close_box() {
    $('#post-box').hide()
}

function to_index() {
    window.location.href = "/"
}
