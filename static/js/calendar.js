initCalendar();

function initCalendar() {

    let monthList = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

    // 날짜 정보
    let date = new Date(); // 현재 날짜(로컬 기준) 가져오기
    let utc = date.getTime() + (date.getTimezoneOffset() * 60 * 1000); // uct 표준시 도출
    let kstGap = 9 * 60 * 60 * 1000; // 한국 kst 기준시간 더하기
    let today = new Date(utc + kstGap); // 한국 시간으로 date 객체 만들기(오늘)

    let thisMonth = new Date(today.getFullYear(), today.getMonth(), today.getDate());

    let currentYear = thisMonth.getFullYear();
    let currentMonth = thisMonth.getMonth();
    let currentDate = thisMonth.getDate();

    // kst 기준 현재시간
    // console.log(thisMonth);

    // 캘린더 렌더링
    renderCalender(thisMonth);

    function renderCalender(thisMonth) {

        // 렌더링을 위한 데이터
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

        // 현재 월 표기
        month = document.querySelector('.year-month')
        month.innerHTML = monthList[currentMonth]

        // 렌더링 html 요소 생성
        calendar = document.querySelector('.dates')
        calendar.innerHTML = '';

        // 이번 달 시작 날의 위치를 잡기 위해 지난 달로 채우기
        for (let i = prevDate - prevDay; i <= prevDate; i++) {
            calendar.innerHTML = calendar.innerHTML + '<div class="day prev disable">' + i + '</div>'
        }
        // 이번달
        for (let i = 1; i <= nextDate; i++) {
            calendar.innerHTML = calendar.innerHTML + '<div class="day current">' + i + '</div>'
        }

        // 오늘 날짜 표기
        if (today.getMonth() === currentMonth) {
            todayDate = today.getDate();
            let currentMonthDate = document.querySelectorAll('.dates .current');
            currentMonthDate[todayDate - 1].classList.add('today');
        }

        // // 이전달로 이동
        // $('.go-prev').on('click', function () {
        //     thisMonth = new Date(currentYear, currentMonth - 1, 1);
        //     renderCalender(thisMonth);
        // });
        //
        // // 다음달로 이동
        // $('.go-next').on('click', function () {
        //     thisMonth = new Date(currentYear, currentMonth + 1, 1);
        //     renderCalender(thisMonth);
        // });
    }
}