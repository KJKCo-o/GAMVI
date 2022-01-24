$(document).ready(function () {
    initCalendar();
});

function initCalendar() {

    let monthList = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    let BaseURL = 'http://127.0.0.1:8000';

    /**** 날짜 계산 ****/
    let date = new Date(); // 현재 날짜(로컬 기준) 가져오기
    let utc = date.getTime() + (date.getTimezoneOffset() * 60 * 1000); // uct 표준시 도출
    let kstGap = 9 * 60 * 60 * 1000; // 한국 kst 기준시간 더하기
    let today = new Date(utc + kstGap); // 한국 시간으로 date 객체 만들기(오늘)

    let thisMonth = new Date(today.getFullYear(), today.getMonth(), today.getDate());

    let currentYear = thisMonth.getFullYear();
    let currentMonth = thisMonth.getMonth();
    let currentDate = thisMonth.getDate();

    // console.log(today);

    /**** 렌더링 ****/
    renderCalender(thisMonth);

    function renderCalender(thisMonth) {

        // console.log(thisMonth);

        // thisMonth를 기준으로 렌더링을 위한 데이터 리로드
        currentYear = thisMonth.getFullYear();
        currentMonth = thisMonth.getMonth();
        currentDate = thisMonth.getDate();

        let startDay = new Date(currentYear, currentMonth, 0); // 이전 달의 마지막 날짜(ex. Fri Dec 31 2021 00:00:00 GMT+0900)
        let prevDate = startDay.getDate(); // 이번 달의 마지막 날(31)
        let prevDay = startDay.getDay(); // 이번 달의 마지막 날의 요일(5==금)

        let endDay = new Date(currentYear, currentMonth + 1, 0); // 이번 달의 마지막 날짜(ex. Mon Jan 31 2022 00:00:00 GMT+0900)
        let nextDate = endDay.getDate(); // 이번 달의 마지막 날(31)
        let nextDay = endDay.getDay(); // 이번 달의 마지막 날의 요일(1==월)

        // console.log(prevDate, prevDay, nextDate, nextDay);

        // 달력 헤드에 현재 월 표기
        $('.year').text(currentYear);
        $('.month').text(monthList[currentMonth]);

        // 렌더링 html 요소 생성
        calendar = document.querySelector('.dates')
        calendar.innerHTML = '';

        // 달력 날짜 뿌리기
        // 이번 달 시작 날의 위치를 잡기 위해 지난 달로 채우기
        for (let i = prevDate - prevDay; i <= prevDate; i++) {
            calendar.innerHTML = calendar.innerHTML + '<div class="day prev disable">' + i + '</div>'
        }

        // 일기 리스트 받아오기(JSON)
        let queryParam = {'user_id': 'cyzhakt7', 'year': currentYear, 'month': currentMonth + 1};
        $.ajax({
            url: BaseURL + "/calendar",
            type: "get",
            data: queryParam,
            dataType: "json",
            success: function (data) {
                console.log(data.emotions);
                // 날짜 모두 렌더링
                for (let i = 1; i <= nextDate; i++) {
                    calendar.innerHTML = calendar.innerHTML + '<button class="day current" disabled="disabled">' + i + '</button>'
                }

                let _currentMonthDates = document.querySelectorAll('.dates .current');

                // 일기 리스트를 기반으로 감정이모지 표시
                for (let idx in data.emotions) {
                    _currentMonthDates[data.emotions[idx].date - 1].classList.add('recorded', data.emotions[idx].emotion);
                    _currentMonthDates[data.emotions[idx].date - 1].id = data.emotions[idx].calendar_id;
                    $('.day.current.' + data.emotions[idx].emotion).text('').attr('disabled', false);
                }

                // 오늘 날짜 표시
                if (today.getFullYear() === currentYear && today.getMonth() === currentMonth) {
                    let todayDate = today.getDate();
                    _currentMonthDates[todayDate - 1].classList.add('today');
                }
            },
            error: function (request, status, error) {
                console.log('통신 실패');
            }
        });

    }

    // 이전 달로 이동
    $('.go-prev').on('click', function () {
        thisMonth = new Date(currentYear, currentMonth - 1, 1);
        renderCalender(thisMonth);
    });

    // 다음 달로 이동
    $('.go-next').on('click', function () {
        thisMonth = new Date(currentYear, currentMonth + 1, 1);
        renderCalender(thisMonth);
        console.log('ab');
    });

    $(document).on('click', '.recorded', function () {
        // console.log($(this).attr('id'));
        location.href = 'calendar/' + $(this).attr('id');
    })
}
