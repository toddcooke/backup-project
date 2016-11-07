
// Todo ensure at least one dow box is checked
$('#reg_bup_submit').click(function () {
    if ($('#dow').find(':checkbox:checked').length === 0) {
        alert('Must check at least one box')
    }
});