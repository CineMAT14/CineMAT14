$(document).ready(function () {
            cinema_list()
        });
        // 극장 리스트 GET(보여주기)
        function cinema_list() {
            $.ajax({
                type: 'GET',
                url: '/main/cinema',
                data: {},
                success: function (response) {
                    let cinemas = response['cinema']

                    for (let i = 0; i < cinemas.length; i++) {
                        let cinema_name = cinemas[i]['cinema_name']
                        let cinema_location = cinemas[i]['cinema_location']
                        let cinema_img = cinemas[i]['cinema_img']
                        let temp_html = `
                                  <div class="col">
                                    <div class="card">
                                      <img src="${cinema_img}" class="card-header" alt="...">
                                      <div class="card-body">
                                        <h5 class="card-body-header">${cinema_name}</h5>
                                        <p class="card-body-description">${cinema_location}</p>
                                      </div>
                                    </div>
                                  </div>
                                  </div>
                                `
                        $("#cinema-box").append(temp_html)
                    }

                }
            });
        }
