$(document).ready(function () {
    selectEmotion();
});

function selectEmotion() {

    $('.logo').on('click', function () {
        location.href = '../';
    });

    // heart 버튼 클릭
    $('#btn-heart').on('click', function () {
        // console.log('heart click');
        location.href = '/record/voice?' + $(this).attr('value');
    });

    // excited 버튼 클릭
    $('#btn-excited').on('click', function () {
        location.href = '/record/voice?' + $(this).attr('value');
    });

    // soso 버튼 클릭
    $('#btn-soso').on('click', function () {
        location.href = '/record/voice?' + $(this).attr('value');
    });

    // blue 버튼 클릭
    $('#btn-blue').on('click', function () {
        location.href = '/record/voice?' + $(this).attr('value');
    });

    // sad 버튼 클릭
    $('#btn-sad').on('click', function () {
        location.href = '/record/voice?' + $(this).attr('value');
    });

    // angry 버튼 클릭
    $('#btn-angry').on('click', function () {
        location.href = '/record/voice?' + $(this).attr('value');
    });
}