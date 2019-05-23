window.onscroll = function () {
    myFunction()
};
var header = document.getElementById("id_header");
var sticky = header.offsetTop;

function myFunction() {
    if (window.pageYOffset > sticky) {
        header.classList.add("sticky");
    } else {
        header.classList.remove("sticky");
    }
}

function show_comments_form(parent_comment_id) {
    if (parent_comment_id === 'write_comment') {
        $("#id_parent_comment").val('')
    } else {
        $("#id_parent_comment").val(parent_comment_id);
    }
    $("#comment_form").insertAfter("#" + parent_comment_id);
}

function show_post_comments_form(parent_comment_id) {
    if (parent_comment_id === 'write_comment') {
        $("#id_parent_comment").val('')
    } else {
        $("#id_parent_comment").val(parent_comment_id);
    }
    $("#comment_form").insertAfter("#" + parent_comment_id);
}

function viewDiv() {
    document.getElementById("div1").style.display = "block";
}

$(document).ready(function () {

    $(document).on("change", "#customToggle1", function (e) {
        e.preventDefault();
        const id = $('#user_id_el').val();
        $.ajax({
            type: 'POST',
            url: `/user/${id}/`,
            dataType: 'html',
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            success: changer,
        });
    });
});

function changer(data) {
    const f = $('#customToggle1').prop('checked');
    $('#customToggle1').prop('checked', f);
}
