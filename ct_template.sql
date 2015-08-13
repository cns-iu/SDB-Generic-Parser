USE clinical_trials;
BEGIN;
	INSERT INTO `ct_master` (`id`, `source_url`, `duplicate`) VALUES ('%pkey%', 'Blank', 1) ON DUPLICATE KEY UPDATE `duplicate`=1;
	DELETE FROM `ct_master` WHERE `id` = '%pkey%' AND `duplicate` = 1;
%data%
COMMIT;

