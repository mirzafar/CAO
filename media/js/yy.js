$(document).ready(function(){
  $("#validation-form").validate({
    rules: {
      validationField: {
        number: true,
        required: true,
      }
    },
    messages: {
      validationField: {
        number: "Enter an integer value.",
        required: "Required Field",
      }
    },
    errorClass: 'invalid',
    validClass: 'valid',
    highlight: function(element, errorClass, validClass) {
      $(element).removeClass(validClass).addClass(errorClass).
      next('label').removeAttr('data-success').attr('data-error', 'Incorrect!');
    },
    unhighlight: function(element, errorClass, validClass) {
      $(element).removeClass(errorClass).addClass(validClass).
      next('label').removeAttr('data-error').attr('data-success', 'Correct!');
    },
    errorPlacement: function() {
    	// Done in highlight/unhighlight
    },
    submitHandler: function(form) {
    	alert('Submitted');
    }
  });
});
