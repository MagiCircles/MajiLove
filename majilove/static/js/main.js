// Your functions or code that should load on all pages goes here.

function loadPhoto() {
    $('[data-open-tab]').each(function() {
	$(this).unbind('click');
	$(this).click(function(e) {
	    $('[data-tabs="' + $(this).closest('.btn-group').data('control-tabs') + '"] .tab-pane').removeClass('active');
	    $('[data-tab="' + $(this).data('open-tab') + '"]').addClass('active');
	    $(this).blur();
	});
    });
}

function loadPhotoForm() {
	function onRarityChange(form, animation) {
		let rarity = form.find('#id_i_rarity').val();
		if (rarity == 0) {
			['dance', 'vocal', 'charm'].forEach(function(k) {
				form.find('#id_' + k + '_max_copy_max').closest('.form-group').hide(animation);
			});
		} else {
			['dance', 'vocal', 'charm'].forEach(function(k) {
				form.find('#id_' + k + '_max_copy_max').closest('.form-group').show(animation);
			});
		}
	}
	var form = $('[data-form-name="edit_photo"], [data-form-name="add_photo"]');
	onRarityChange(form, 'slow');
	form.find('#id_i_rarity').change(function () { onRarityChange(form, 'slow'); });
}